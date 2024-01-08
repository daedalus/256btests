#!/usr/bin/env python
import sys
import random

import math

P = 115792089237316195423570985008687907853269984665640564039457584007908834671663
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337

X = 0x86B0745E46B9C82B33FA4444D51D761BD83DACAE343AAE5CF3C77E54F6E9DAB6


x = 1

while True:

    x += 1

    y = int(math.sqrt(x**3 + 7))

    print(hex((y - 1) % N).replace("0x", "").replace("L", "").zfill(64))
    print(hex(y % N).replace("0x", "").replace("L", "").zfill(64))
    print(hex((y + 1) % N).replace("0x", "").replace("L", "").zfill(64))
