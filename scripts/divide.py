import sys

original = open(sys.argv[1],'r')

unis = {}
for line in original:
	if line[0] == 'U':
		uniref = line
		unis[uniref] = {}
	else:
		if line[0] == '>':
			read = line
		else:
			unis[uniref][read] = line

original.close()

path = sys.argv[2]
uni_file = open(path+'references.fasta','w')
for uniref in unis:
	curr = open(path+uniref[:-1]+'.fasta','w')
	for read in unis[uniref]:
		curr.write(read + unis[uniref][read])
	curr.close()
	uni_file.write('>' + uniref)
