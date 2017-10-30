#!/usr/bin/env python
import sys
import fileinput

P = 115792089237316195423570985008687907853269984665640564039457584007908834671663L
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337L


def hexify(i):
	return hex(i).replace('0x','').replace('L','').zfill(64)

def test_xor(i):
	for j in xrange(0,256):
		k = ((i ^ j) % N)
		print hexify(k)

for line in fileinput.input():
	line = line.replace('\n','')
	try:
		test_xor(int(line,16))
	except:
		pass

