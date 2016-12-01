#!/usr/bin/env python
import fileinput
import itertools, operator

tmp = []
i = 0

for line in fileinput.input():
        try:
                line = line.replace('\n','')
		for i in itertools.permutations(line):
			print ''.join(i)
        except:
                pass

