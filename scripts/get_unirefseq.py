#This script checks the lines that are result in our search and prints the sequence in order to retrieve it.

import sys

lines = open(sys.argv[1],'r')                                 #We open the file provided in the first argument as the result of the searchuniref.sh script


wanted = []
for l in lines:
	if l[0] == '#':
		break                                         #If we reach the SLURM information we end the loop
	wanted.append(l.partition(':')[0])                    #We add all the ids in a list
lines.close()

sequences = open(sys.argv[2],'r')                             #We open the uniref database
output = open(sys.argv[3],'w')                                #We open th efile in which the results will be written
curr_line = 0
writen = ''                                                   #We create the string that will contain everything that will be written in the output file.
for line in sequences:						    #This approach needs more RAM memory but the speed is higher, as there are less system calls needed
	curr_line += 1
	if line[0] == '>' and  str(curr_line) == wanted[0]:   #We check if the nxt sequence is one we will be interested in 
		grab = True                                   #We set grab to true (to 'grab' the sequence)
		writen = writen + line                        #We add the line to the string we are going to write into the output file
		wanted = wanted[1:]                           #We remove the sequence we have just grabbed from the list
		if len(wanted) == 0:			      #And if the list has no more sequences we end the loop
			break
	elif line[0] == '>':				      #If we are not interested in the next sequence we set grab to false
		grab = False	
	elif grab:
		writen = writen + line                        #If grab is true and the current line is a sequence we add the line to writen

output.write(writen)                                          #We write everything in writen to the output file
sequences.close()                                             #We close all open files
output.close()
