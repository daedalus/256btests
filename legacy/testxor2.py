#!/usr/bin/env python
import sys
import fileinput

P = 115792089237316195423570985008687907853269984665640564039457584007908834671663
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337


def hexify(i):
    return hex(i).replace("0x", "").replace("L", "").zfill(64)


data = []
for line in fileinput.input():
    line = line.replace("\n", "")
    try:
        data.append(int(line, 16))
    except:
        pass


def xor(a, b):
    k = abs(a ^ b)
    if k not in [a, b]:
        c = k % N
        if c > 100000000:
            print(hexify(c))
        c = (N - k) % N
        if c > 100000000:
            print(hexify(c))
        c = (P - k) % N
        if c > 100000000:
            print(hexify(c))


for i in range(0, len(data) - 1):
    for j in range(0, len(data) - 1):
        xor(data[i], data[j])
