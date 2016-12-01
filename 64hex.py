#!/usr/bin/env python
#!/usr/bin/env python
import fileinput


def hexify(i):
	return hex(int(line.replace('\n','').replace('\r','').replace('0x','').replace('L',''))).zfill(64)


for line in fileinput.input():	
	l = len(line)
	if l > 1:
		try:
			print hexfiy(line)
		except:
			pass

