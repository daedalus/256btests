#!/usr/bin/env python
import sys
import random

random.seed(sys.argv[1])

start = 2**32

while True:
    i = start + random.randint(0, (2**31))
    print(hex(i).replace("0x", "").replace("L", "").zfill(64))
    # print hex(N + i).replace('0x','').replace('L','').zfill(64)
