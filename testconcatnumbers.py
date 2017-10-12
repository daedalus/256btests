import fileinput

def c2(line,n):
	for i in list(" *+-_/?<>") + [""]:
		print line + i + str(n)
		print str(n) + i + line

def c3(line,n):
	c2(line.upper(),n)
	c2(line.lower(),n)
	c2(line.capitalize(),n)

max = 1000
for line in fileinput.input():
	line = line.rstrip()
	for i in xrange(0,max):
		c2(line,i)
