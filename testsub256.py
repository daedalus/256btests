#!/usr/bin/env python
import sys
import fileinput

P = 115792089237316195423570985008687907853269984665640564039457584007908834671663L
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337L
C = 2**256


#skip = int("00000000000000000000000000000000000000000000000000000027eb78574a",16)
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


start = 0
end = len(data) - 1 

for i in range(start,end):
	print hexify((N-data[i]) % N)
	print hexify((P-data[i]) % N)
	print hexify((C-data[i]) % N) 

