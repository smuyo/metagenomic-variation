import sys

database = open(sys.argv[1],'r')
outp = [None] * int(sys.argv[5])


dis = {}
for line in database:
	dis[line.split(' ')[0][1:]] = 'Gene'
database.close()

unidict = {}
dia_reads = open(sys.argv[2],'r')
num = 0
for line2 in dia_reads:
	if dis.get(line2.split('\t')[1]) != None:
		outp[num] = line2		
		num +=1
dia_reads.close()

bow_reads = open(sys.argv[3],'r')
for line in bow_reads:
	if dis.get((line.split('\t')[1]).split('|')[7]) != None:
		outp[num] = line
		num += 1
		if unidict.get((line.split('\t')[1]).split('|')[7]) == None:
			unidict[(line.split('\t')[1]).split('|')[7]] = {}
		if unidict[(line.split('\t')[1]).split('|')[7]].get((line.split('\t')[1]).split('|')[3]) == None:
			unidict[(line.split('\t')[1]).split('|')[7]][(line.split('\t')[1]).split('|')[3]] = 0
		unidict[(line.split('\t')[1]).split('|')[7]][(line.split('\t')[1]).split('|')[3]] += 1
bow_reads.close()

outp = filter(None, outp)
output = open(sys.argv[4],'w')
output.write(''.join(outp))
output.close()
for element in unidict:
	print(unidict[element])
