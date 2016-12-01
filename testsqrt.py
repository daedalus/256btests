#!/usr/bin/env python
import sys
import fileinput
import math
import random

P = 115792089237316195423570985008687907853269984665640564039457584007908834671663L
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337L

def hexify(i):
	return hex(i).replace('0x','').replace('L','').zfill(64)

def t(i):
	i = i + 1
	return i

def t2(i,r):
	for x in range(0-r,r):
		j = i + x 
		if j != i:
			yield j


r = 10000

for line in fileinput.input():
	line = line.replace('\n','')
	if len(line) > 2:
		try:
			i = int(line,16)
			for k in range(0,16):
				i = int(math.sqrt(i)) % N
				if i > 10000000:
                       			print hexify(i)

		except:
			pass
