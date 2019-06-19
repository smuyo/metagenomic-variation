##This script processes a UniRef xml file and returns the ID of the representative protein

import sys

xml = open(sys.argv[1],'r')
this = False
check = False
for line in xml:
	sp = line.split(' ')
	if sp[0] == '<dbReference' and sp[1] == 'type="EMBL"':
		this = True
		check = False
		continue
	if this and check and sp[3].split('"')[1] == 'Genomic_DNA':
		print(possible)
		break
	if this and sp[0] == '<property':
		possible = (sp[-1].split('"')[1])
		check = True
		continue


xml.close()
