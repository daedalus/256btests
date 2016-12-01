#!/usr/bin/env python
import sys
import random

import math

P = 115792089237316195423570985008687907853269984665640564039457584007908834671663L
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337L

X=0x86b0745e46b9c82b33fa4444d51d761bd83dacae343aae5cf3c77e54f6e9dab6L


x = 1

while True:

	x+=1	

	y = int(math.sqrt(x**3+7))

	print hex((y-1) % N).replace('0x','').replace('L','').zfill(64)
	print hex(y % N).replace('0x','').replace('L','').zfill(64)
	print hex((y+1) % N).replace('0x','').replace('L','').zfill(64)


