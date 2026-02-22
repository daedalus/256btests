import fileinput


def c2(line, n):
    for i in list(" *+-_/?<>") + [""]:
        print(line + i + str(n))
        print(str(n) + i + line)


def c3(line, n):
    c2(line.upper(), n)
    c2(line.lower(), n)
    c2(line.capitalize(), n)


max_concat = 1000
for line in fileinput.input():
    line = line.rstrip()
    for i in range(0, max_concat):
        c2(line, i)
