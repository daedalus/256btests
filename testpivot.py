import fileinput

def swap(a,b):
	return b,a


tmp = ""
def pivot(s,tmp,i):
	l = len(s)
	if l>1:
		a = pivot(s[l/2:],tmp,i)[len(tmp)-1]
		b = pivot(s[:l/2],tmp,i)[len(tmp)-1]
		r = a+b if i else b+a
	else:
		r = s
	tmp.append(r)
	return tmp


tmp3 = []
c = 0
for line in fileinput.input():
	line = line.replace('\r','').replace('\n','')
	tmp = []
	tmp1 = pivot(line,tmp,False)
	tmp2 = pivot(line,tmp,True)

	for i in (set(sorted(tmp1+tmp2))):
		tmp3.append(i)

	if len(tmp3) > 1000000:
		for i in tmp3:
			print i
		tmp3 = []


