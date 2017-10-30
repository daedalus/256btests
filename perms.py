#!/usr/bin/env python
import fileinput
#from itertools import permutations


import itertools, operator

tmp = []
i = 0

def sort_uniq(sequence):
    return itertools.imap(
        operator.itemgetter(0),
        itertools.groupby(sorted(sequence)))

def allequal(line):
	t = ''
	e = True
	for c in line:
		e = (t == c)
		t = c
	return e


def perms(tmp,i,s):
	s = itertools.permutations(s)
	for p in s:
		i+= 1
		tmp.append(''.join(p))
		if i == 20:
			tmp = sort_uniq(tmp)
			for p in tmp:
				print p
			tmp = []


for line in fileinput.input():
        try:
                line = line.replace('\n','')
		#if len(line) <= 100:
		if not allequal(line):
			perms(tmp,i,line.lower())
			perms(tmp,i,line)
			perms(tmp,i,line.upper())
		else:
			print line
		#else:
		#	print line
        except:
                pass

