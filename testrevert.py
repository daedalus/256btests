#!/usr/bin/env python
import sys
import fileinput

P = 115792089237316195423570985008687907853269984665640564039457584007908834671663
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337


# skip = int("00000000000000000000000000000000000000000000000000000027eb78574a",16)
skip = 0


def hexify(i):
    return hex(i).replace("0x", "").replace("L", "").zfill(64)


data = []
for line in fileinput.input():
    line = line.replace("0x", "").replace("L", "").replace("\n", "")
    print(line[::-1])
