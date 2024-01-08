#!/usr/bin/env python
import sys
import fileinput
import math

P = 115792089237316195423570985008687907853269984665640564039457584007908834671663
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337


def quberoot(i):
    return -((-i) ** (1.0 / 3.0))


# skip = int("00000000000000000000000000000000000000000000000000000027eb78574a",16)
skip = 0


def hexify(i):
    return hex(i).replace("0x", "").replace("L", "").zfill(64)


data = []
for line in fileinput.input():
    line = line.replace("0x", "").replace("L", "").replace("\n", "")
    try:
        i = int(line, 16)
        k = int(math.sqrt((i**3) + 7))
        print(hexify((k - 1) % N))
        print(hexify(k % N))
        print(hexify((k + 1) % N))
        k = int(quberoot((i**2) - 7))
        print(hexify((k - 1) % N))
        print(hexify(k % N))
        print(hexify((k + 1) % N))
        k = int((3 * (i**2)) / 2)
        print(hexify((k - 1) % N))
        print(hexify(k % N))
        print(hexify((k + 1) % N))

    except:
        pass
