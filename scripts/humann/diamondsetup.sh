#!/bin/bash
#SBATCH --job-name=diamondsetup
#SBATCH --output=../output/diamondsetup%j.txt
#SBATCH --error=../output/diamondsetup%j.log
#SBATCH --time=05:30:00
#SBATCH --nodes=1
#SBATCH --mem=60gb
#SBATCH --cpus-per-task=4
#SBATCH --export=none
#SBATCH --get-user-env=L


#This file creates a diamond database from a provided fasta file.
#The path to the file should be provided in the first argument without the .fasta extension.

diamond makedb --in $1.fasta -d $1 -p $2            #We create a diamond database from the provided file.

