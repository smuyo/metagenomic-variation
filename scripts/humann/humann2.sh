#!/bin/bash

#This script performs all the needed steps to run HUMaNn2
#First it coverts a read file from sam to fastq, which uses to run MetaPhlAn and get the taxonomic profile for HUMaNn2, which then runs using the previously created files.
#After running all the intermediate files are removed

#Arguments:
##1 <- A sam read file (with its complete path)
##2 <- The folder on which you want the output to be in
##3 <- The folder of the protein database to be used during the translated search
##4 <- The number of threads you want HuManN2 to be executed with

module load MetaPhlAn

echo 'Start uncompressing'
samtools fastq $1 >${1%.*}.fastq
echo 'End uncompressing'
echo 'Start metaphlan'
metaphlan2.py ${1%.*}.fastq --input_type fastq --output ${1%.*}.tsv
echo 'End metaphlan'
echo 'Start humann2'
module load DIAMOND
module load humann2
humann2 --input ${1%.*}.fastq --output $2humann2/ --protein-database $3/ --taxonomic-profile ${1%.*}.tsv --threads $4 --input-format fastq --verbose
echo 'End HuMANN2'
