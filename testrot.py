#!/usr/bin/env python
import sys
import fileinput

P = 115792089237316195423570985008687907853269984665640564039457584007908834671663L
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337L

def hexify(i):
	return hex(i).replace('0x','').replace('L','').zfill(64)
	
get_bin = lambda x, n: format(x, 'b').zfill(n)

rol = lambda val, r_bits, max_bits: \
    (val << r_bits%max_bits) & (2**max_bits-1) | \
    ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))
 
# Rotate right: 0b1001 --> 0b1100
ror = lambda val, r_bits, max_bits: \
    ((val & (2**max_bits-1)) >> r_bits%max_bits) | \
    (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))


SKIP = 0

j=0
for line in fileinput.input():
	line = line.replace('0x','').replace('L','').replace('\n','')	
	try:
		k = int(line,16)
		for i in range(2,254):
			j+=1
			if j > SKIP:
				a = rol(k,i,256) % N
				b = ror(k,i,256) % N
				if (1000000 < a):
					print hexify(a)
				if (1000000 < b):
					print hexify(b)
	except:
		pass
			 	

