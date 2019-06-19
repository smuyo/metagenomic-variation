#!/bin/bash

#This script searches a gene we specify in the UniRef90 database and returns a file containing only the identifiers of the sequences of the gene we want.

cd $4/scripts

grep -i "${1//_/ }" $2 > $3$1.txt

