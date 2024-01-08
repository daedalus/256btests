import fileinput

bits = 256
freqs = [0 for _ in range(0, bits)]
for line in fileinput.input():
    b = format(int(line, 16), "08b").zfill(256)
    for i in range(0, bits):
        if b[i] == "1":
            freqs[i] += 1
print(freqs)
