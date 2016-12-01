import fileinput

for line in fileinput.input():
	line = line.replace('\n','').replace('\r','')
	h = line[-8:]
	i = int(h,16)
	b = bin(i)
	print h, b, i
