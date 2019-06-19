#!/bin/bash

cd $4/scripts
touch $3
num=$(wc -l $2)
python tophit_alt2.py $1 $2 $3 $num
