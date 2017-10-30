#!/usr/bin/env python
import sys
import fileinput

P = 115792089237316195423570985008687907853269984665640564039457584007908834671663L
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337L



skip = int("00000000000000000000000000000000000000000000000000000027eb78574a",16)

def hexify(i):
	return hex(i).replace('0x','').replace('L','').zfill(64)

data = []
for line in fileinput.input():
	line = line.replace('0x','').replace('L','').replace('\n','')
	try:
		data.append(int(line,16))
	except:
		pass

#import random
#random.shuffle(data)

start = 0
end = len(data) -1
mid = int(end / 2)

def prepare(data):
	data2 = []
	for k in range(mid,end):
		data2.append(data[k])
	for k in range(mid,start,-1):
		data2.append(data[k])

	return data2

def invert(data):
	data2 = []
	for k in range(start,end):
		data2.append(data[k])
	return data2

#data = prepare(data)
#data = invert(data)
#print end, mid

for i in range(start,end):
	for j in range(start,end):
		if i != j:
			x = abs(data[i] - data[j])
			if (x != data[i] and x != data[j]):
				y = (x % N)
				if (skip < y):
					print hexify(y)



