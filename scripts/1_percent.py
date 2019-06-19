###This script processes the output of .... and keeps the references that have more than 1% of the reads aligned to them###


import sys

stats = open(sys.argv[1],'r')

first = 0
toget = []
nline = 0
nuni = 0
enduni = 0
for line in stats:
	if nline == 0:
		nline = 1
		total = line[:-1]
		min = int(total)//100
	else:
		uniref = line.split(' ')[0][:-1]
		num = line.split(' ')[1]
		nuni += 1
		if int(num) > min:
			toget.append(uniref)
			enduni += 1

stats.close()
print(toget)
reads = open(sys.argv[2],'r')
now = 'start'
out = []
endnum = 0
for line in reads:
	if line[0:6] == 'UniRef':
		now = line[:-1]
		if now in toget:
			out.append(line)
	else:
		if now in toget:
			out.append('>' + line)
			endnum += 1
			
reads.close()

output = open(sys.argv[3],'w')
output.write(''.join(out))
output.close()
endstat = open(sys.argv[4],'w')
endstat.write('Initial number of reads: ' + str(total) + '\n' + 'Final number of reads: ' + str(endnum) + '\n' + 'Initial number of references: ' + str(nuni) + '\n' + 'Final number of references: ' + str(enduni))
endstat.close()
