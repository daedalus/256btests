import itertools

p = itertools.permutations("abcdefghijklmnopqrstuvwxyz0123456789 ")
for i in p:
    print("".join(i))
