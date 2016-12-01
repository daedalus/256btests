#!/usr/bin/env python
import sys
import fileinput

P = 115792089237316195423570985008687907853269984665640564039457584007908834671663L
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337L



#skip = int("00000000000000000000000000000000000000000000000000000027eb78574a",16)
skip = 0

def hexify(i):
	return hex(i).replace('0x','').replace('L','').zfill(64)

data = []
for line in fileinput.input():
	line = line.replace('\n','').replace('\r','')	
	print line
	s = line.title()
	if (s != line):
		print s
	s = line.lower()
	if (s != line):
		print s
	s = line.upper()
	if (s != line):
		print s

			


