#!/bin/bash

#Arguments :
#1 -> Read file (in bam format)
#2 -> Search result file
#3 -> Output file

cd $4/scripts
samtools fastq $1 > $1.fastq
num=$(wc -l < $2)
touch $3
python get_readseq.py $1.fastq $2 $3 $num
rm $1.fastq
