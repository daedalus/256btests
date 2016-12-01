#!/usr/bin/env python
import sys
import random
import math

random.seed(sys.argv[1])


def r256b():
	strhex = ""
	
	for i in range(0,31):
		h = hex(int(math.floor(random.random()*256))).replace('0x','')
		if len(h) == 1:
			h = "0" +h
		strhex += h
		#print hex(i).replace('0x','').replace('L','').zfill(64)
		#print hex(N + i).replace('0x','').replace('L','').zfill(64)
	
	
	return strhex

while True:
	print r256b()
	
