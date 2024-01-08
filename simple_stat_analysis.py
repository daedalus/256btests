import fileinput

bits = 256
freqs = []

for i in range(0, bits):
    freqs.append(0)

c = 0
for line in fileinput.input():
    b = format(int(line, 16), "08b").zfill(256)
    for i in range(0, bits):
        if b[i] == "1":
            freqs[i] += 1
    c += 1

print(freqs)
