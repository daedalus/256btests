#!/usr/bin/env python
import sys
import random

seed = 0
random.seed(seed)

c = 0
while True:
    c += 1
    i = random.randint(0, (2**256))
    print(hex(i).replace("0x", "").replace("L", "").zfill(64))
    # print hex(N + i).replace('0x','').replace('L','').zfill(64)
    if (c % 1000) == 0:
        seed += 1
        random.seed(seed)
