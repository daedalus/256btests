import sys
import os

filename=sys.argv[1]
fp = open(filename)
i = int(sys.argv[2])
l = int(sys.argv[3])
flen=os.stat(filename).st_size

while True:
	if i <= flen:
		fp.seek(i,0)
		print fp.read(l).encode('hex')
		i += 1
	else:
		break

	
