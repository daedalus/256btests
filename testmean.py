#!/usr/bin/env python
import sys
import fileinput
import numpy as np

P = 115792089237316195423570985008687907853269984665640564039457584007908834671663L
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337L



#skip = int("00000000000000000000000000000000000000000000000000000027eb78574a",16)
skip = 0

def hexify(i):
	return hex(i).replace('0x','').replace('L','').zfill(64)

data = []
for line in fileinput.input():
	line = line.replace('0x','').replace('L','').replace('\n','')	
	try:
		i = int(line,16)
		if i > 0:
			data.append(i)
	except:
		pass

import random
random.shuffle(data)

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

#print np.mean(data)	
def AM(data):
	accum = 0
	for i in range(0,len(data)-1):
		accum += data[i]
	return accum / len(data)

def GM(data):
	accum = 1
	for i in range(0,len(data)-1):
		accum *= data[i]
	return accum ** (1 / len(data))
def HM(data):
	accum = 0
	for i in range(0,len(data)-1):
		accum += 1/data[i]
	return len(data) * (accum ** -1) 


#print hex(AM(data))
#print HM(data)


m = AM(data)
#for i in range(0,len(data)-1):
#	print hexify((m*data[i]) % N )
#	print hexify((m-data[i]) % N )
#	print hexify((m+data[i]) % N )

j = N
while True:
	j -= m
	print hexify(j % N)
