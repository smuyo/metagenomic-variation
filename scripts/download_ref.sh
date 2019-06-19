#!/bin/bash

usage() {
    echo "Usage: $0 -i [UNIREF ID]"
}

exit() {
    usage
    exit 1
}

while getopts "i:o:p:" options; do
    case "${options}" in
        i)
            uniid=${OPTARG}
            ;;
        o)
            outfold=${OPTARG}
            ;;
        p)
            scrpath=${OPTARG}
            ;;
        :)
            echo "Error: -${OPTARG} requires an argument"
            exit
            ;;
        *)
            exit
            ;;
    esac
done

wget --quiet -nv http://www.uniprot.org/uniprot/${uniid}.xml -O ${outfold}UniRef90_${uniid}.xml

embl=$(python ${scrpath}getreprid.py ${outfold}UniRef90_${uniid}.xml)

rm ${outfold}UniRef90_${uniid}.xml

wget --quiet http://www.ebi.ac.uk/ena/data/view/${embl}%26display%3Dfasta -O ${outfold}UniRef90_${uniid}.fasta

