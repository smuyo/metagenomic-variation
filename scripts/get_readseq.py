#This script checks the lines that are result in our search and prints the sequence in order to retrieve it.

import sys


print(sys.argv[4])
gene = open(sys.argv[2],'r')                                  #We open the file provided in the first argument as the result of the searchuniref.sh script
wanted = {}
for l in gene:
	if l[0] == '>':
		wanted[l[1:]] = ''                       		#We add all the lines in a list
	else:
		wanted[l] = ''
gene.close()
print(len(wanted), 'final')

sequences = open(sys.argv[1],'r')                             #We open the uniref database
grab = False
last = ''
for line in sequences:                                         #This approach needs more RAM memory but the speed is higher, as there are less system calls needed
	if wanted.get(line[1:])!=None:   #We check if the nxt sequence is one we will be interested in 
		grab = True                                   #We set grab to true (to 'grab' the sequence)
		last = line[1:]
	else:
		if grab:
			wanted[last] = line                        #If grab is true and the current line is a sequence we add the line to writen
			grab = False

sequences.close()                                             #We close all open files


out = open(sys.argv[3],'w')
for sequence in wanted:
	if wanted[sequence] == '':
		out.write(sequence)
	else:
		out.write('>' + sequence + wanted[sequence])
out.close()
