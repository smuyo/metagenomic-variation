#!/bin/bash

rm $1$2_bowtie2_aligned.sam 
rm $1$2_bowtie2_index.1.bt2 
rm $1$2_bowtie2_index.2.bt2 
rm $1$2_bowtie2_index.3.bt2
rm $1$2_bowtie2_index.4.bt2 
rm $1$2_bowtie2_unaligned.fa
rm $1$2_bowtie2_index.rev.1.bt2
rm $1$2_bowtie2_index.rev.2.bt2
rm $1$2_custom_chocophlan_database.ffn
rm $1$2_diamond_unaligned.fa
rm $1$2.log
rm -r $1tmp*
