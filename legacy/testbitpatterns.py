def hexify(i):
    return hex(i).replace("0x", "").replace("L", "").zfill(64)


def test(i, a):
    b = ""
    while len(b) <= 256:
        if a:
            b = bin(i).replace("0b", "") + b
        else:
            b += bin(i).replace("0b", "")
        i += 1
    return hexify(int(b, 2))


i = 0
while True:
    i += 1
    print(test(i, False))
    print(test(i, True))
