#!/bin/bash

#SBATCH --qos=priority
#SBATCH --job-name=Variance
#SBATCH --output=variance%j.out
#SBATCH --error=variance%j.err
#SBATCH --time=12:00:00
#SBATCH --cpus-per-task=10
#SBATCH --mem=60gb
#SBATCH --nodes=1
#SBATCH --export=NONE
#SBATCH --get-user-env=L

usage() {
    echo "Usage: $0 [-h] -i [SAMPLE] -g [GENE NAME] -o [OUTPUT FOLDER] -u [CUSTOM_UNIREF] [-s] [-t NUMBER OF THREADS] [-d]"
}

help() {
        echo
        echo "Mandatory arguments:"
        echo
        echo "-i <input file>
        File to be used as input. It should be a file in bam format containing the reads."
        echo
        echo "-g <gene name>
        The name of the gene of which we want to check the variation.
        If the name has more than one word the words should be separated by _"
        echo
        echo "-o <output folder>
        The folder where the output must be stored."
        echo
        echo "-u <custom uniref>
        The folder containing the UniRef database."
        echo
        echo
        echo "Optional arguments:"
        echo
        echo "-h
        Display this help"
        echo
        echo "-s
        Bypass HUMAnN2. The results of HUMAnN2 must be in the folder indicated with the -o option"
        echo
        echo "-t
        Number of threads to use. DEFAULT: 1"
        echo
        echo "-d
        Setup the UniRef databse to be used in DIAMOND.
        If it has not been configured before and HUMAnN2 must run, this option must be selected"
        echo
}


exit_missing() {
    usage
    exit 1
}

exit_help() {
	usage
	help
	exit 1
}

parsearg() {
    iflag=0
    gflag=0
    oflag=0
    uflag=false
    hflag=false
    dflag=false
    threads=1

    while getopts ':i:g:o:u:st:hd' options; do
        case "${options}" in
            i )
                sample=${calling_path}/${OPTARG}
                iflag=1
                ;;
            g )
                gene=${OPTARG}
                gflag=1
                ;;
            o )
                outfolder=${calling_path}/${OPTARG}
                oflag=1
                ;;
            s )
                hflag=true
                ;;
            u )
                unir=${calling_path}/${OPTARG}
                uflag=true
                ;;
            t )
                threads=${OPTARG}
                ;;
            d )
                dflag=true
                ;;
            h )
                exit_help
                ;;
            : )
                echo "Error: -${OPTARG} requires an argument"
                exit_missing
                ;;
            * )
                exit_missing
                ;;
        esac
    done
}

calling_path=$(pwd)
call=${0:1}
parent_path=${calling_path}${call%/*}

parsearg $@

if [ $iflag -ne 1 ]; then
    echo 'Sample file must be provided'
    exit_missing
fi

if [ $gflag -ne 1 ]; then
    echo 'Gene name must be provided'
    exit_missing
fi

if [ $oflag -ne 1 ]; then
    echo 'A folder for the output must be provided'
    exit_missing
fi

if $uflag && [ ${unir##*.} == fasta ]; then
    echo HuManN2 will use ${unir} as the protein database for translated search
else
    echo 'A UniRef90 database in fasta file must be provided'
    exit_missing
fi

module load Python
module load SAMtools
module load BLAST+

samplename=${sample%.*}
samplename=${samplename##*/}

if $hflag; then
    echo 'HuManN2 will not run'
    echo The resulting files from HuManN2 must be in ${outfolder}humann
    if $dflag; then
    	echo "As HUMAnN2 will not run, it is not necessary to setup the UniRef database for DIAMOND, so it will not be set up"
    fi
else
	if $dflag; then
		/bin/bash ${parent_path}/scripts/humann/diamondsetup.sh ${unir%.*} $threads
	fi
    /bin/bash ${parent_path}/scripts/humann/humann2.sh $sample ${outfolder} ${unir%/*} $threads
    /bin/bash ${parent_path}/scripts/humann/cleantrash.sh ${outfolder}humann2/${samplename}_humann2_temp/ $samplename
fi
module load Python
echo Starting UniRef searches...
/bin/bash ${parent_path}/scripts/searchuniref.sh $gene $unir $outfolder $parent_path
/bin/bash ${parent_path}/scripts/searchuniref.sh Uncharacterized $unir $outfolder $parent_path
echo UniRef searches DONE

echo Starting HuManN2 results filtering...
/bin/bash ${parent_path}/scripts/tophit_alt2.sh ${outfolder}Uncharacterized.txt ${outfolder}humann2/${samplename}_humann2_temp/${samplename}_diamond_aligned.tsv ${outfolder}humann2/${samplename}_humann2_temp/${samplename}_diamond_tophits.tsv $parent_path
/bin/bash ${parent_path}/scripts/filt_unis.sh ${outfolder}${gene}.txt ${outfolder}humann2/${samplename}_humann2_temp/${samplename}_diamond_tophits.tsv ${outfolder}humann2/${samplename}_humann2_temp/${samplename}_bowtie2_aligned.tsv ${outfolder}humann2/${samplename}_humann2_temp/${samplename}_${gene}.tsv $parent_path
python ${parent_path}/scripts/filt_byuni.py ${outfolder}humann2/${samplename}_humann2_temp/${samplename}_${gene}.tsv ${outfolder}byuni.txt ${outfolder}stats.txt
python ${parent_path}/scripts/1_percent.py ${outfolder}stats.txt ${outfolder}byuni.txt ${outfolder}byuni_filtered.txt ${outfolder}stats_filtered.txt
/bin/bash ${parent_path}/scripts/get_readseq.sh $sample ${outfolder}byuni_filtered.txt ${outfolder}withreadseq.txt $parent_path
echo HuManN2 results filtering DONE

echo Starting results division...
mkdir ${outfolder}divided
python ${parent_path}/scripts/divide.py ${outfolder}withreadseq.txt ${outfolder}divided/
echo Result division DONE

echo Starting downloading of references and variation calculation...
mkdir ${outfolder}divided/references
for uniref in $(cat ${outfolder}divided/references.fasta ); do
echo ${uniref##*_}
/bin/bash ${parent_path}/scripts/download_ref.sh -i ${uniref##*_} -o ${outfolder}divided/references/ -p ${parent_path}/scripts/
done

mkdir ${outfolder}sam
mkdir ${outfolder}sam/variation


for file in $(ls -p ${outfolder}divided/ | grep -v / ); do
makeblastdb -in ${outfolder}divided/${file} -dbtype nucl
filename=${file##*/}
echo $filename
blastn -db ${outfolder}divided/${file} -query ${outfolder}divided/references/${filename} -outfmt '17 SQ' -out ${outfolder}sam/${filename%.*}.sam -max_target_seqs 1000000
/bin/bash ${parent_path}/scripts/variance/heterozygosity_error.sh ${outfolder}sam/${filename%.*}.sam ${outfolder}sam/variation/ ${parent_path}
done


###for file in $(ls -p ${outfolder} | grep -v / ); do 
###makeblastdb -in ${outfolder}${file} -dbtype nucl
###filename=${file##*/}
###blastn -db ${outfolder}/${file} -query ${outfolder}references/${filename} -outfmt '17 SQ' -out ${outfolder}sam/${filename%.*}.sam -max_target_seqs 1000000
###/bin/bash heterozygosity_error.sh ${outfolder}sam/${file%.*}.sam ${outfolder}sam/variation/
###done


echo DONE!
echo Now go and have some fun!!!
