import sys

unch = open(sys.argv[1],'r')
ids = {}
for line in unch:
	ids[line.split(' ')[0]] = 'Unchar'

unch.close()
print('Unch finished')

diamond = open(sys.argv[2],'r')
out = [None] * int(sys.argv[4])
num = 0
last = ''
avis = ''
for line in diamond:
	read = line.split('\t')[0]
	uniref = line.split('\t')[1]
	if read != last and ids.get(read) == None:
		last = read
		out[num] = line
		num += 1
	elif avis != read:
		avis = read
	else:
		last = read

print('Diamond finished')
out = filter(None, out)
diamond.close()
output = open(sys.argv[3],'w')
output.write("".join(out))
output.close()

