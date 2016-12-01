import math

def hexify(i):
	return hex(i).replace('0x','').replace('L','').zfill(64)

N=115792089237316195423570985008687907852837564279074904382605163141518161494337L

#x = 2228224
x=0

while True:
	x+=1
	print hexify(N / x)
