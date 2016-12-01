#!/usr/bin/env python
import sys
import random

random.seed(sys.argv[1])

while True:
	i = random.randint(0,(2**256))
	print hex(i).replace('0x','').replace('L','').zfill(64)
	#print hex(N + i).replace('0x','').replace('L','').zfill(64)

	
