import math


def hexify(i):
    return hex(i).replace("0x", "").replace("L", "").zfill(64)


N = 115792089237316195423570985008687907852837564279074904382605163141518161494337

# x=1101824 + 36864 + 14336
x = 1

while True:
    x += 1
    y = ((x**3) << x) % N
    print(hexify(y))
