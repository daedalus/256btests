#!/usr/bin/env python
import hashlib
import fileinput
import sys

def sha256bin(s):
	return hashlib.sha256(s).digest()

def hexify(s):
	return s.encode('hex').zfill(64)

for line in fileinput.input():
	i = 0
	line = line.rstrip()
	line = sha256bin(line)
	while i <= 100:
		line = sha256bin(line)
		print hexify(line)
		i += 1
