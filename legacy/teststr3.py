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
    line = line.replace("\n", "").replace("\r", "")
    data.append(line)


def join2(a, b):

    print(f"{a.title()} {b}")
    print(a.title() + b)
    print(f"{a} {b.title()}")
    print(a + b.title())
    print(f"{a.title()} {b.title()}")
    print(a.title() + b.title())
    print(f"{a.lower()} {b.lower()}")
    print(a.lower() + b.lower())
    print(f"{a.upper()} {b.upper()}")
    print(a.upper() + b.upper())
    print(f"{a.lower()} {b.upper()}")
    print(a.lower() + b.upper())
    print(f"{a.upper()} {b.lower()}")
    print(a.upper() + b.lower())
    print(f"{a} {b}")
    print(a + b)


for i in range(0, len(data) - 1):
    for j in range(0, len(data) - 1):
        join2(data[i], data[j])
