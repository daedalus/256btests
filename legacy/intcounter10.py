from stdnum import luhn

i = 0

while True:
    i += 1
    c = luhn.checksum(str(i))
    print(str(i) + str(c))

# print hex(int(str_))
