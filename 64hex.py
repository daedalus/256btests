#!/usr/bin/env python
#!/usr/bin/env python
import fileinput

N = 115792089237316195423570985008687907852837564279074904382605163141518161494337L


def hexify(i):
	return hex(i).replace('0x','').replace('L','').zfill(64)


for line in fileinput.input():	
	line = line.replace('\n','').replace('\r','').replace('0x','').replace('L','')
	l = len(line)
	if l > 1:
		try:
			print hexify(int(line,16) % N)
		except:
			pass

