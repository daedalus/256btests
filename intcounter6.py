#!/usr/bin/env python
import sys
import random

import math

P = 115792089237316195423570985008687907853269984665640564039457584007908834671663L
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337L

i=-1

while True:
	
	i+=1

	a = ((P ** i) % N)
	b = ((N ** i) % N)

	print hex(a).replace('0x','').replace('L','').zfill(64)
	print hex(b).replace('0x','').replace('L','').zfill(64)

