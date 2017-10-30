#!/usr/bin/env python
import sys
import fileinput
import hashlib
import fileinput

P = 115792089237316195423570985008687907853269984665640564039457584007908834671663L
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337L

def hexify(i):
	return hex(i).replace('0x','').replace('L','').zfill(64)

def sha512(s):
	n = hashlib.sha512()
	n.update(s)
	return n.hexdigest()

def main():
	for line in fileinput.input():
		line = line.replace('\r','').replace('\n','')
		print hexify(int(sha512(line),16) % N)

main()
