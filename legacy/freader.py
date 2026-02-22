#!/usr/bin/env python
# Author Dario Clavijo 2017
# GPLv3

import sys
import os
import math
import io


def shannon_entropy(data, iterator=None):
    """
    Borrowed from http://blog.dkbza.org/2007/05/scanning-data-for-entropy-anomalies.html
    """
    if not data:
        return 0
    entropy = 0

    if iterator is None:
        iterator = "".join(chr(i) for i in range(0, 255))
    for x in (ord(c) for c in iterator):
        p_x = float(data.count(chr(x))) / len(data)
        if p_x > 0:
            entropy += -p_x * math.log(p_x, 2)
    return entropy


thresshold = 4.5

filename = sys.argv[1]
# fp = open(filename)
fp = io.BufferedReader(io.FileIO(filename, "rb"))

start = int(sys.argv[2])
l = int(sys.argv[3])
flen = os.stat(filename).st_size
if flen == 0:
    flen = int(sys.argv[4])

RSIZE = 1024 * 128

while True:
    if start <= flen:
        # lastdata = ""
        fp.seek(start, 0)
        data = fp.read(RSIZE)
        for i in range(0, (RSIZE)):
            s = data[i : i + l]
            e = shannon_entropy(s)
            # print data.encode('hex'),e
            if e > thresshold:
                print(s.encode("hex"), e)
            del e
            del s
        del data
        # lastdata = data
    else:
        break
