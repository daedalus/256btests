n =int("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141",16)
p =int("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F",16)


def hexify(i):
	return hex(i).replace('0x','').replace('L','').zfill(64)

i = 0
while True:
	i +=1
	print hexify(((p % n)  ** i) % n)
