#!/usr/bin/env python
import sys
import fileinput

P = 115792089237316195423570985008687907853269984665640564039457584007908834671663L
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337L



#skip = int("00000000000000000000000000000000000000000000000000000027eb78574a",16)
#skip = 100000000

skip = 0

def hexify(i):
	return hex(i).replace('0x','').replace('L','').zfill(64)

data = []
for line in fileinput.input():
	line = line.replace('0x','').replace('L','').replace('\n','')	
	try:
		data.append(int(line,16))	
	except:
		pass

import random
random.shuffle(data)

start = 0
end = len(data) -1
mid = int(end / 2)

def diff(x,i,j):
	if (x != i and x != j):
		y = (x % N)
		if (skip < y):
			return hexify(y)

for i in range(start,end):
	for j in range(start,end):
		if i != j:
			x = data[i] and data[j]
			d = diff(x,data[i],data[j])
			if d: print d
			x = data[i] or data[j]
			d =  diff(x,data[i],data[j])
			if d: print d
			x = data[i] ^ data[j]
			d = diff(x,data[i],data[j])
			if d: print d

			


