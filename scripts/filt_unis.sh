#!/bin/bash

cd $5/scripts
num1=$(wc -l < $2)
num2=$(wc -l < $3)
num=$(($num1 + $num2))
echo $num
touch $4
python filt_unis.py $1 $2 $3 $4 $num
