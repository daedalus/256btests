#!/usr/bin/env python
import sys
import fileinput

P = 115792089237316195423570985008687907853269984665640564039457584007908834671663L
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337L
b256 = (2**256)

def hexify(i):
	return hex(i).replace('0x','').replace('L','').zfill(64)
	
for line in fileinput.input():
	line = line.replace('0x','').replace('L','').replace('\n','')	
	try:
		k = int(line,16)
		#for i in range(1,256):
		#	print hexify(k / i) 
		#	print hexify(k * i) 
		#	print hexify((k / i) % P) 
		#	print hexify((k * i) % P) 

		print hexify((N-k) % N)
		print hexify((P-K) % N)
		print hexify((k ^ b256)  % N)
		print hexify((b256-k) % N)
	except:
		pass
			 	

