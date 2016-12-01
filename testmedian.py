#!/usr/bin/env python
import sys
import fileinput

P = 115792089237316195423570985008687907853269984665640564039457584007908834671663L
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337L

def hexify(i):
	return hex(i).replace('0x','').replace('L','').zfill(64)
	

j = 0
accum = 0
max_j = 2

for line in fileinput.input():
	line = line.replace('0x','').replace('L','').replace('\n','')	
	if len(line) > 2 and len(line) <= (64):
		try:
			accum += int(line,16)
			j += 1
			if j >= max_j:
				j = 0
				accum = 0
			
			print hexify(int(accum/max_j)%N)

		except:
			pass
			 	
