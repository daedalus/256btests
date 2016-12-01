#!/usr/bin/env python
# Author Dario Clavijo 2016
# simple ROT13 algo or Caesar Cipher
import fileinput

def rot13(test):
	p = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "
	r = "nopqrstuvwxyzabcdefghijklmNOPQRSTUVWXYZABCDEFGHIJKLM "
	d = ""
	for l in test:
		f = p.find(l)
		if (f > -1):
			d += r[p.find(l)]
		else:
			d += l
	return d

for line in fileinput.input():
	print rot13(line.replace('\n',''))
