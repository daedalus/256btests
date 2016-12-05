import sys

fp = open(sys.argv[1])
i = int(sys.argv[2])
l = int(sys.argv[3])

while True:
	i += 1
	fp.seek(i,0)
	print fp.read(l).encode('hex')
