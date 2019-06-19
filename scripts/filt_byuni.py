import sys
import time

hits = open(sys.argv[1],'r')
coso = {}
num_reads = 0

for line in hits:
	read = line.split('\t')[0].split('|')[0]
	uniref = line.split('\t')[1]
	if uniref[0:2] == 'gi':
		actual = uniref.split('|')[7]
		if coso.get(actual) != None:
			coso[actual].append(read)
			num_reads += 1
		else:
			coso[actual] = [read]
			num_reads += 1
	else:
		if coso.get(uniref) != None:
			coso[uniref].append(read)
			num_reads += 1
		else:
			coso[uniref] = [read]
			num_reads += 1

hits.close()

output = open(sys.argv[2],'w')
resumen = open(sys.argv[3],'w')
print('Found:\n')
resumen.write(str(num_reads))
for reference in coso:
	output.write(reference + '\n')
	output.write('\n'.join(coso[reference]) + '\n')
	resumen.write('\n' + reference + ': ' + str(len(coso[reference])))
	num_reads += len(coso[reference])
output.close()
resumen.close()


print('-----------------------------------------------')
print('Total number of references: ' + str(len(coso)))
print('Total number of reads: ' + str(num_reads))
