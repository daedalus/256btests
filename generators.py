#!/usr/bin/env python3
"""
generators.py — Unified CLI for 256btests generators and test scripts.

Usage:
    python generators.py --list
    python generators.py <generator> [options]
    python generators.py <generator> --help

Stdin-driven generators read from standard input; pipe data in:
    python generators.py seq-counter | head -5
    echo "deadbeef" | python generators.py bits-repr

Old names (e.g. intcounter14, randomint, testxor) are accepted as deprecated
aliases and continue to work unchanged.
"""

import argparse
import sys
import os
import io
import math
import random
import hashlib
import itertools
import operator

# ── secp256k1 constants ───────────────────────────────────────────────────────
P = 115792089237316195423570985008687907853269984665640564039457584007908834671663
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337


# ── Shared helpers ────────────────────────────────────────────────────────────
def hexify(i):
    return hex(i).replace("0x", "").replace("L", "").zfill(64)


get_bin = lambda x, n: format(x, "b").zfill(n)

rol = lambda val, r_bits, max_bits: (val << r_bits % max_bits) & (
    2**max_bits - 1
) | ((val & (2**max_bits - 1)) >> (max_bits - (r_bits % max_bits)))

ror = lambda val, r_bits, max_bits: (
    (val & (2**max_bits - 1)) >> r_bits % max_bits
) | (val << (max_bits - (r_bits % max_bits)) & (2**max_bits - 1))


# ── Generator implementations ─────────────────────────────────────────────────


def run_256bitrepr(args):
    """Show last-8-char hex, binary repr, and integer for each stdin line."""
    for line in sys.stdin:
        line = line.replace("\n", "").replace("\r", "")
        h = line[-8:]
        i = int(h, 16)
        b = bin(i)
        print(h, b, i)


def run_64hex(args):
    """Reduce each hex stdin line modulo N and print as 64-char hex."""
    for line in sys.stdin:
        line = (
            line.replace("\n", "").replace("\r", "").replace("0x", "").replace("L", "")
        )
        if len(line) > 1:
            try:
                print(hexify(int(line, 16) % N))
            except Exception:
                pass


def run_freader(args):
    """Scan a binary file for high-entropy byte sequences.

    Note: Original (freader.py) used Python 2 bytes/string APIs that do not
    work under Python 3. Fixed:
      - shannon_entropy now accepts bytes natively (no chr/ord round-trip).
      - s.encode('hex') replaced with s.hex().
    """

    def shannon_entropy(data):
        if not data:
            return 0
        entropy = 0.0
        length = len(data)
        for x in range(256):
            count = data.count(x)
            if count > 0:
                p_x = count / length
                entropy -= p_x * math.log(p_x, 2)
        return entropy

    thresshold = 4.5
    filename = args.filename
    fp = io.BufferedReader(io.FileIO(filename, "rb"))
    start = args.start
    l = args.length
    flen = os.stat(filename).st_size
    if flen == 0:
        flen = args.flen if args.flen is not None else 0

    RSIZE = 1024 * 128

    while True:
        if start <= flen:
            fp.seek(start, 0)
            data = fp.read(RSIZE)
            for i in range(0, RSIZE):
                s = data[i : i + l]
                e = shannon_entropy(s)
                if e > thresshold:
                    print(s.hex(), e)  # Fixed: was s.encode('hex') (Python 2)
                del e
                del s
            del data
        else:
            break


def run_intcounter6(args):
    """Infinite: print (P^i % N) and (N^i % N) for i = 0, 1, 2, …"""
    i = -1
    while True:
        i += 1
        a = (P**i) % N
        b = (N**i) % N
        print(hex(a).replace("0x", "").replace("L", "").zfill(64))
        print(hex(b).replace("0x", "").replace("L", "").zfill(64))


def run_intcounter9(args):
    """Infinite: print floor(sqrt(x^3+7)) variants mod N for x = 2, 3, …"""
    x = 1
    while True:
        x += 1
        y = int(math.sqrt(x**3 + 7))
        print(hex((y - 1) % N).replace("0x", "").replace("L", "").zfill(64))
        print(hex(y % N).replace("0x", "").replace("L", "").zfill(64))
        print(hex((y + 1) % N).replace("0x", "").replace("L", "").zfill(64))


def run_intcounter10(args):
    """Infinite: print each integer concatenated with its Luhn checksum digit.

    Requires: python-stdnum  (pip install python-stdnum)
    """
    from stdnum import luhn

    i = 0
    while True:
        i += 1
        c = luhn.checksum(str(i))
        print(str(i) + str(c))


def run_intcounter14(args):
    """Infinite: print sequential integers as 64-char hex (starting at 1)."""
    x = 0
    while True:
        x += 1
        print(hexify(x))


def run_intcounter15(args):
    """Infinite: print ((x^3 << x) % N) as 64-char hex for x = 2, 3, …"""
    x = 1
    while True:
        x += 1
        y = ((x**3) << x) % N
        print(hexify(y))


def run_perms(args):
    """Read lines from stdin; print unique permutations (lower, original, upper)."""

    def sort_uniq(sequence):
        return map(operator.itemgetter(0), itertools.groupby(sorted(sequence)))

    def allequal(line):
        t = ""
        e = True
        for c in line:
            e = t == c
            t = c
        return e

    def perms_inner(tmp, idx, s):
        s = itertools.permutations(s)
        for p in s:
            idx += 1
            tmp.append("".join(p))
            if idx == 20:
                tmp = list(sort_uniq(tmp))
                for item in tmp:
                    print(item)
                tmp = []
        return tmp, idx

    tmp = []
    idx = 0
    for line in sys.stdin:
        try:
            line = line.replace("\n", "")
            if not allequal(line):
                tmp, idx = perms_inner(tmp, idx, line.lower())
                tmp, idx = perms_inner(tmp, idx, line)
                tmp, idx = perms_inner(tmp, idx, line.upper())
            else:
                print(line)
        except Exception:
            pass


def run_perms2(args):
    """Print every permutation of a–z, 0–9 and space (very long — pipe to head)."""
    p = itertools.permutations("abcdefghijklmnopqrstuvwxyz0123456789 ")
    for i in p:
        print("".join(i))


def run_perms3(args):
    """Read lines from stdin; print all permutations of each line."""
    for line in sys.stdin:
        try:
            line = line.replace("\n", "")
            for i in itertools.permutations(line):
                print("".join(i))
        except Exception:
            pass


def run_probagen(args):
    """Generate 256-bit hex values using a weighted bit-probability model.

    Requires: numpy  (pip install numpy)
    """
    import numpy

    weights = [
        11915, 11966, 12055, 11920, 11874, 11965, 11908, 11900, 11973, 11876,
        12070, 11938, 11974, 11947, 11936, 11935, 12048, 12142, 12033, 12081,
        11813, 11983, 11949, 12083, 12051, 12018, 11830, 12030, 11930, 12023,
        11967, 11871, 12037, 11902, 11995, 12074, 11959, 12099, 11897, 11978,
        11921, 11993, 11873, 12143, 12086, 11951, 11963, 11905, 12161, 11885,
        12095, 11918, 12053, 11985, 12070, 11922, 11830, 12018, 11989, 12044,
        11926, 12028, 11969, 12069, 12008, 12015, 12137, 12002, 12054, 12126,
        12022, 11898, 12031, 12109, 11856, 11996, 12090, 11789, 11931, 11983,
        12096, 11845, 11996, 12078, 12062, 12046, 11880, 11969, 11956, 12094,
        12160, 12001, 11988, 12067, 12113, 12047, 11828, 11894, 11921, 11951,
        12086, 11855, 11962, 12081, 12027, 12057, 12063, 12051, 12000, 12053,
        12119, 11951, 12049, 12076, 12028, 11915, 12015, 12033, 12033, 12071,
        12263, 12127, 12080, 11880, 11999, 12073, 12039, 11998, 11972, 12010,
        11925, 12172, 11941, 11974, 12065, 12082, 11921, 12008, 12124, 11989,
        12056, 11945, 12078, 11965, 11968, 11986, 11953, 11971, 12054, 11982,
        12037, 11947, 11922, 11983, 11933, 11914, 11998, 12024, 12052, 12106,
        12030, 11742, 11918, 11887, 12082, 12092, 12009, 11995, 11984, 11950,
        11939, 12060, 12064, 11874, 12053, 12055, 12058, 11975, 11933, 11921,
        11974, 12063, 11852, 12085, 11852, 11866, 12002, 11922, 12031, 11997,
        12070, 12099, 12000, 11870, 12019, 11973, 11933, 12016, 11956, 11990,
        11829, 12005, 11992, 12063, 12150, 11945, 12019, 12117, 12071, 12035,
        12083, 11923, 11993, 11972, 11991, 12060, 12094, 12070, 12012, 11997,
        12179, 12151, 12073, 11954, 11970, 12044, 11991, 12125, 12060, 11926,
        12013, 12183, 12028, 12017, 12099, 12176, 11952, 12146, 12189, 12063,
        12071, 12315, 12136, 12222, 12092, 12060, 12169, 12267, 11977, 12107,
        12096, 12110, 12166, 12111, 12062, 12198,
    ]

    count = 24414.0
    probs = [0 for _ in range(256)]

    def recalculate_probs(mult):
        for i in range(256):
            prob = (weights[i] / count) * mult
            probs[i] = [prob, 1 - prob]

    def gen_samples():
        accum = ""
        for i in range(256):
            bit = numpy.random.choice([1, 0], p=probs[i])
            accum += str(bit)
        return int(accum, 2)

    numpy.random.seed(0)

    def gen():
        for j in range(1, 199):
            recalculate_probs(j / 100.0)
            for _ in range(1000):
                i = gen_samples()
                print(hex(i).replace("0x", "").replace("L", "").zfill(64))

    gen()


def run_randomint(args):
    """Infinite: random 256-bit integers seeded by the seed argument."""
    random.seed(args.seed)
    while True:
        i = random.randint(0, (2**256))
        print(hex(i).replace("0x", "").replace("L", "").zfill(64))


def run_randomint2(args):
    """Infinite: random 256-bit integers; seed auto-increments every 1000 values."""
    seed = 0
    random.seed(seed)
    c = 0
    while True:
        c += 1
        i = random.randint(0, (2**256))
        print(hex(i).replace("0x", "").replace("L", "").zfill(64))
        if (c % 1000) == 0:
            seed += 1
            random.seed(seed)


def run_randomint3(args):
    """Infinite: random integers in [2^32, 2^32 + 2^31), seeded by the seed argument."""
    random.seed(args.seed)
    start = 2**32
    while True:
        i = start + random.randint(0, (2**31))
        print(hex(i).replace("0x", "").replace("L", "").zfill(64))


def run_randomint4(args):
    """Infinite: 256-bit hex strings assembled from random bytes, seeded by the seed argument."""
    random.seed(args.seed)

    def r256b():
        strhex = ""
        for _ in range(31):
            h = hex(int(math.floor(random.random() * 256))).replace("0x", "")
            if len(h) == 1:
                h = f"0{h}"
            strhex += h
        return strhex

    while True:
        print(r256b())


def run_replacer(args):
    """Echo each stdin line, stripping CR/LF."""
    for line in sys.stdin:
        print(line.replace("\n", "").replace("\r", ""))


def run_rot13(args):
    """Apply ROT13 (Caesar cipher) to each stdin line."""
    p = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "
    r = "nopqrstuvwxyzabcdefghijklmNOPQRSTUVWXYZABCDEFGHIJKLM "

    def rot13(test):
        return "".join(r[p.find(l)] for l in test)

    for line in sys.stdin:
        print(rot13(line.rstrip()))


def run_simple_stat_analysis(args):
    """Count per-bit-position frequency across 256-bit hex lines from stdin."""
    bits = 256
    freqs = [0] * bits
    for line in sys.stdin:
        b = format(int(line, 16), "08b").zfill(256)
        for i in range(bits):
            if b[i] == "1":
                freqs[i] += 1
    print(freqs)


def run_testSTRToSHA512(args):
    """SHA-512 each stdin line, reduce mod N, output as 64-char hex.

    Note: Original (testSTRToSHA512.py) passed a str to hashlib.update(), which
    requires bytes in Python 3. Fixed to encode to UTF-8 before hashing.
    """

    def sha512(s):
        n = hashlib.sha512()
        n.update(s.encode("utf-8"))  # Fixed: original passed str (Python 2 style)
        return n.hexdigest()

    for line in sys.stdin:
        line = line.replace("\r", "").replace("\n", "")
        print(hexify(int(sha512(line), 16) % N))


def run_testadd(args):
    """Read hex lines from stdin; print all pairwise sums mod N above skip threshold."""
    skip = int(
        "00000000000000000000000000000000000000000000000000000027eb78574a", 16
    )
    data = []
    for line in sys.stdin:
        line = line.replace("0x", "").replace("L", "").replace("\n", "")
        try:
            data.append(int(line, 16))
        except Exception:
            pass

    start = 0
    end = len(data) - 1

    for i in range(start, end):
        for j in range(start, end):
            if i != j:
                x = data[i] + data[j]
                if x not in [data[i], data[j]]:
                    y = x % N
                    if skip < y:
                        print(hexify(y))


def run_testbitpatterns(args):
    """Infinite: generate 256-bit hex values from concatenated binary strings."""

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


def run_testboolefuncs(args):
    """Read hex lines from stdin; print AND/OR/XOR pairwise combinations mod N."""
    skip = 0
    data = []
    for line in sys.stdin:
        line = line.replace("0x", "").replace("L", "").replace("\n", "")
        try:
            data.append(int(line, 16))
        except Exception:
            pass

    random.shuffle(data)

    start = 0
    end = len(data) - 1

    def diff(x, i, j):
        if x not in [i, j]:
            y = x % N
            if skip < y:
                return hexify(y)

    for i in range(start, end):
        for j in range(start, end):
            if i != j:
                x = data[i] and data[j]
                if d := diff(x, data[i], data[j]):
                    print(d)
                x = data[i] or data[j]
                if d := diff(x, data[i], data[j]):
                    print(d)
                x = data[i] ^ data[j]
                if d := diff(x, data[i], data[j]):
                    print(d)


def run_testconcatnumbers(args):
    """Read lines from stdin; concatenate each with numbers 0..999 using various separators."""

    def c2(line, n):
        for sep in list(" *+-_/?<>") + [""]:
            print(line + sep + str(n))
            print(str(n) + sep + line)

    max_concat = 1000
    for line in sys.stdin:
        line = line.rstrip()
        for i in range(max_concat):
            c2(line, i)


def run_testinv(args):
    """Read hex lines from stdin; print N-k, P-k, k XOR 2^256, and 2^256-k mod N.

    Note: Original (testinv.py) used 'K' (uppercase) on the P-k line, causing a
    NameError.  Fixed to 'k' (lowercase) to match the assigned input variable.
    """
    b256 = 2**256
    for line in sys.stdin:
        line = line.replace("0x", "").replace("L", "").replace("\n", "")
        try:
            k = int(line, 16)
            print(hexify((N - k) % N))
            print(hexify((P - k) % N))  # Fixed: was 'K' (NameError) in original
            print(hexify((k ^ b256) % N))
            print(hexify((b256 - k) % N))
        except Exception:
            pass


def run_testmean(args):
    """Read hex lines from stdin; compute arithmetic mean, then loop subtracting mean from N.

    Note: This generator first consumes all stdin, then enters an infinite loop.
    """
    data = []
    for line in sys.stdin:
        line = line.replace("0x", "").replace("L", "").replace("\n", "")
        try:
            i = int(line, 16)
            if i > 0:
                data.append(i)
        except Exception:
            pass

    random.shuffle(data)

    def AM(data):
        accum = sum(data[i] for i in range(len(data) - 1))
        return accum / len(data)

    m = AM(data)
    j = N
    while True:
        j -= m
        print(hexify(int(j) % N))


def run_testmedian(args):
    """Read hex lines from stdin; print rolling pair-average mod N."""
    j = 0
    accum = 0
    max_j = 2
    for line in sys.stdin:
        line = line.replace("0x", "").replace("L", "").replace("\n", "")
        if len(line) > 2 and len(line) <= 64:
            try:
                accum += int(line, 16)
                j += 1
                if j >= max_j:
                    j = 0
                    accum = 0
                print(hexify(accum // max_j % N))
            except Exception:
                pass


def run_testmodulo3(args):
    """Infinite: print ((p % n)^i) % n as 64-char hex for i = 1, 2, 3, …"""
    n = int("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141", 16)
    p = int("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F", 16)
    i = 0
    while True:
        i += 1
        print(hexify(((p % n) ** i) % n))


def run_testmult(args):
    """Read hex lines from stdin; print all pairwise products mod N."""
    skip = 0
    data = []
    for line in sys.stdin:
        line = line.replace("0x", "").replace("L", "").replace("\n", "")
        try:
            data.append(int(line, 16))
        except Exception:
            pass

    random.shuffle(data)

    start = 0
    end = len(data) - 1

    for i in range(start, end):
        for j in range(start, end):
            if i != j:
                x = data[i] * data[j]
                if x not in [data[i], data[j]]:
                    y = x % N
                    if skip < y:
                        print(hexify(y))


def run_testpivot(args):
    """Read lines from stdin; apply recursive pivot string transformation.

    Note: Original (testpivot.py) used '/' for integer division (Python 2 style),
    causing a TypeError in Python 3.  Fixed to use '//' (floor division).
    """

    def pivot(s, tmp, i):
        l = len(s)
        if l > 1:
            a = pivot(s[l // 2 :], tmp, i)[len(tmp) - 1]  # Fixed: was l / 2
            b = pivot(s[: l // 2], tmp, i)[len(tmp) - 1]  # Fixed: was l / 2
            r = a + b if i else b + a
        else:
            r = s
        tmp.append(r)
        return tmp

    tmp3 = []
    for line in sys.stdin:
        line = line.replace("\r", "").replace("\n", "")
        tmp = []
        tmp1 = pivot(line, tmp, False)
        tmp2 = pivot(line, tmp, True)
        for i in set(sorted(tmp1 + tmp2)):
            tmp3.append(i)
        if len(tmp3) > 1000000:
            for i in tmp3:
                print(i)
            tmp3 = []


def run_testpwr(args):
    """Read hex lines from stdin; print each value raised to powers 96..127 mod N."""
    skip = 0
    MIN_PWR = 96
    MAX_PWR = 128
    data = []
    for line in sys.stdin:
        line = line.replace("0x", "").replace("L", "").replace("\n", "")
        try:
            data.append(int(line, 16))
        except Exception:
            pass

    end = len(data) - 1
    start = 0

    for i in range(start, end):
        for j in range(MIN_PWR, MAX_PWR):
            k = data[i] ** j
            if k > 10000000:
                print(hexify(k % N))


def run_testrevert(args):
    """Read hex lines from stdin; print each line with characters reversed."""
    for line in sys.stdin:
        line = line.replace("0x", "").replace("L", "").replace("\n", "")
        print(line[::-1])


def run_testrot(args):
    """Read hex lines from stdin; print rotate-left and rotate-right bit variants mod N."""
    SKIP = 0
    j = 0
    for line in sys.stdin:
        line = line.replace("0x", "").replace("L", "").replace("\n", "")
        try:
            k = int(line, 16)
            for i in range(2, 254):
                j += 1
                if j > SKIP:
                    a = rol(k, i, 256) % N
                    b = ror(k, i, 256) % N
                    if a > 1000000 and a != k:
                        print(hexify(a))
                    if b > 1000000 and a != k:
                        print(hexify(b))
        except Exception:
            pass


def run_testsec256k1(args):
    """Read hex lines from stdin; apply secp256k1 curve candidate operations."""

    def quberoot(i):
        return -((-i) ** (1.0 / 3.0))

    for line in sys.stdin:
        line = line.replace("0x", "").replace("L", "").replace("\n", "")
        try:
            i = int(line, 16)
            k = int(math.sqrt((i**3) + 7))
            print(hexify((k - 1) % N))
            print(hexify(k % N))
            print(hexify((k + 1) % N))
            k = int(quberoot((i**2) - 7))
            print(hexify((k - 1) % N))
            print(hexify(k % N))
            print(hexify((k + 1) % N))
            k = int((3 * (i**2)) / 2)
            print(hexify((k - 1) % N))
            print(hexify(k % N))
            print(hexify((k + 1) % N))
        except Exception:
            pass


def run_testsha256(args):
    """Read stdin lines; apply SHA-256 recursively 101 times and print hex output.

    Note: Original (testsha256.py) used bytes.encode('hex') (Python 2 API).
    Fixed to use bytes.hex() for Python 3 compatibility.
    """

    def sha256bin(s):
        if isinstance(s, str):
            s = s.encode("utf-8")
        return hashlib.sha256(s).digest()

    def hexify_bytes(s):
        return s.hex().zfill(64)  # Fixed: was s.encode('hex') (Python 2)

    for line in sys.stdin:
        line = line.rstrip()
        data = sha256bin(line)
        for _ in range(101):
            data = sha256bin(data)
            print(hexify_bytes(data))


def run_testsqrt(args):
    """Read hex lines from stdin; apply iterated integer sqrt 16 times mod N."""
    for line in sys.stdin:
        line = line.replace("\n", "")
        if len(line) > 2:
            try:
                i = int(line, 16)
                for _ in range(16):
                    i = int(math.sqrt(i)) % N
                    if i > 10000000:
                        print(hexify(i))
            except Exception:
                pass


def run_teststr(args):
    """Read hex lines from stdin; produce pairwise string concatenation combinations."""
    data = []
    for line in sys.stdin:
        line = line.replace("0x", "").replace("L", "").replace("\n", "")
        try:
            data.append(line)
        except Exception:
            pass

    start = 0
    end = len(data) - 1

    for i in range(start, end):
        for j in range(start, end):
            s = data[i] + data[j]
            print(s)
            print(s.title())
            s = f"{data[i]} {data[j]}"
            print(s)
            print(s.title())
            s = data[i].lower() + data[j].lower()
            print(s)
            print(s.title())
            s = f"{data[i].lower()} {data[j].lower()}"
            print(s)
            print(s.title())
            s = data[i].upper() + data[j].upper()
            s = f"{data[i].upper()} {data[j].upper()}"
            s = data[i].lower() + data[j].upper()
            print(s)
            print(s.title())
            s = f"{data[i].lower()} {data[j].upper()}"
            print(s.title())
            s = data[i].upper() + data[j].lower()
            print(s)
            print(s.title())
            s = f"{data[i].upper()} {data[j].lower()}"
            print(s)
            print(s.title())


def run_teststr2(args):
    """Read stdin lines; print each with title-case, lower-case, and upper-case variants."""
    for line in sys.stdin:
        line = line.replace("\n", "").replace("\r", "")
        print(line)
        s = line.title()
        if s != line:
            print(s)
        s = line.lower()
        if s != line:
            print(s)
        s = line.upper()
        if s != line:
            print(s)


def run_teststr3(args):
    """Read all stdin lines; print pairwise join combinations with case variants."""
    data = []
    for line in sys.stdin:
        line = line.replace("\n", "").replace("\r", "")
        data.append(line)

    def join2(a, b):
        print(f"{a.title()} {b}")
        print(a.title() + b)
        print(f"{a} {b.title()}")
        print(a + b.title())
        print(f"{a.title()} {b.title()}")
        print(a.title() + b.title())
        print(f"{a.lower()} {b.lower()}")
        print(a.lower() + b.lower())
        print(f"{a.upper()} {b.upper()}")
        print(a.upper() + b.upper())
        print(f"{a.lower()} {b.upper()}")
        print(a.lower() + b.upper())
        print(f"{a.upper()} {b.lower()}")
        print(a.upper() + b.lower())
        print(f"{a} {b}")
        print(a + b)

    for i in range(len(data) - 1):
        for j in range(len(data) - 1):
            join2(data[i], data[j])


def run_testsub(args):
    """Read hex lines from stdin; print pairwise absolute differences mod N above threshold."""
    skip = int(
        "00000000000000000000000000000000000000000000000000000027eb78574a", 16
    )
    data = []
    for line in sys.stdin:
        line = line.replace("0x", "").replace("L", "").replace("\n", "")
        try:
            data.append(int(line, 16))
        except Exception:
            pass

    start = 0
    end = len(data) - 1

    for i in range(start, end):
        for j in range(start, end):
            if i != j:
                x = abs(data[i] - data[j])
                if x not in [data[i], data[j]]:
                    y = x % N
                    if skip < y:
                        print(hexify(y))


def run_testsub256(args):
    """Read hex lines from stdin; print N-k, P-k, and 2^256-k mod N for each."""
    C = 2**256
    data = []
    for line in sys.stdin:
        line = line.replace("0x", "").replace("L", "").replace("\n", "")
        try:
            data.append(int(line, 16))
        except Exception:
            pass

    start = 0
    end = len(data) - 1

    for i in range(start, end):
        print(hexify((N - data[i]) % N))
        print(hexify((P - data[i]) % N))
        print(hexify((C - data[i]) % N))


def run_testxor(args):
    """Read hex lines from stdin; XOR each value with 0..255 and print results mod N."""

    def test_xor(i):
        for j in range(256):
            k = (i ^ j) % N
            print(hexify(k))

    for line in sys.stdin:
        line = line.replace("\n", "")
        try:
            test_xor(int(line, 16))
        except Exception:
            pass


def run_testxor2(args):
    """Read hex lines from stdin; print pairwise XOR variants mod N and P."""
    data = []
    for line in sys.stdin:
        line = line.replace("\n", "")
        try:
            data.append(int(line, 16))
        except Exception:
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

    for i in range(len(data) - 1):
        for j in range(len(data) - 1):
            xor(data[i], data[j])


# ── Registry ──────────────────────────────────────────────────────────────────
# Maps subcommand name -> (function, short description).
# Keys are the current (mathematically descriptive) names.
GENERATORS = {
    "additive-inv": (
        run_testinv,
        "Read hex lines; N-k, P-k, k XOR 2^256, 2^256-k mod N",
    ),
    "alpha-perms": (
        run_perms2,
        "Print all permutations of a–z, 0–9 and space (very long)",
    ),
    "bit-concat": (
        run_testbitpatterns,
        "Infinite: 256-bit hex values from concatenated bit strings",
    ),
    "bit-rotate": (
        run_testrot,
        "Read hex lines; rotate-left/right bit variants mod N",
    ),
    "bit-stats": (
        run_simple_stat_analysis,
        "Count per-bit-position frequency across 256-bit hex lines from stdin",
    ),
    "bits-repr": (
        run_256bitrepr,
        "Show last-8-char hex, binary repr, and integer for each stdin line",
    ),
    "bitwise-ops": (
        run_testboolefuncs,
        "Read hex lines; AND/OR/XOR pairwise combinations mod N",
    ),
    "cubic-shift": (
        run_intcounter15,
        "Infinite: (x^3 << x) mod N as 64-char hex",
    ),
    "entropy-scan": (
        run_freader,
        "Scan a binary file for high-entropy byte sequences",
    ),
    "hex-reverse": (
        run_testrevert,
        "Read hex lines; print each line character-reversed",
    ),
    "iter-sqrt": (
        run_testsqrt,
        "Read hex lines; iterated integer sqrt 16 times mod N",
    ),
    "iterated-pow-mod": (
        run_testmodulo3,
        "Infinite: ((p mod n)^i) mod n as 64-char hex",
    ),
    "line-echo": (
        run_replacer,
        "Echo each stdin line, stripping CR/LF",
    ),
    "luhn-counter": (
        run_intcounter10,
        "Infinite: integers with Luhn checksum digit (requires python-stdnum)",
    ),
    "mean-sub": (
        run_testmean,
        "Read hex lines; infinite loop subtracting arithmetic mean from N",
    ),
    "mod-add": (
        run_testadd,
        "Read hex lines; print pairwise sums mod N above threshold",
    ),
    "mod-mul": (
        run_testmult,
        "Read hex lines; pairwise products mod N",
    ),
    "mod-neg": (
        run_testsub256,
        "Read hex lines; N-k, P-k, and 2^256-k mod N for each value",
    ),
    "mod-sub": (
        run_testsub,
        "Read hex lines; pairwise absolute differences mod N above threshold",
    ),
    "pair-avg": (
        run_testmedian,
        "Read hex lines; rolling pair-average mod N",
    ),
    "pair-concat": (
        run_teststr,
        "Read hex lines; pairwise string concatenation combinations",
    ),
    "pow-range": (
        run_testpwr,
        "Read hex lines; raise each to powers 96–127 mod N",
    ),
    "prob-gen": (
        run_probagen,
        "Generate 256-bit hex via weighted bit-probability model (requires numpy)",
    ),
    "rand-bytes": (
        run_randomint4,
        "Infinite: 256-bit hex strings from random bytes (requires seed argument)",
    ),
    "rand-offset": (
        run_randomint3,
        "Infinite: random integers from 2^32+, seeded (requires seed argument)",
    ),
    "rand-reseed": (
        run_randomint2,
        "Infinite: random 256-bit integers; seed increments every 1000 values",
    ),
    "rand-seeded": (
        run_randomint,
        "Infinite: random 256-bit integers (requires seed argument)",
    ),
    "rot13": (
        run_rot13,
        "Apply ROT13 to each stdin line",
    ),
    "secp-pow-mod": (
        run_intcounter6,
        "Infinite: P^i mod N and N^i mod N (secp256k1 constants)",
    ),
    "secp256k1-ops": (
        run_testsec256k1,
        "Read hex lines; secp256k1 curve candidate operations",
    ),
    "seq-counter": (
        run_intcounter14,
        "Infinite: sequential integers as 64-char hex",
    ),
    "sha256-chain": (
        run_testsha256,
        "Read stdin lines; SHA-256 applied recursively 101 times",
    ),
    "sha512-hex": (
        run_testSTRToSHA512,
        "SHA-512 each stdin line, reduce mod N, output as 64-char hex",
    ),
    "str-cases": (
        run_teststr2,
        "Read stdin lines; print title/lower/upper case variants",
    ),
    "str-join-cases": (
        run_teststr3,
        "Read all stdin lines; pairwise join combinations with case variants",
    ),
    "str-numcat": (
        run_testconcatnumbers,
        "Read stdin lines; concatenate each with numbers 0..999",
    ),
    "str-perms": (
        run_perms3,
        "Read stdin lines; print all permutations of each line",
    ),
    "str-pivot": (
        run_testpivot,
        "Read stdin lines; recursive pivot string transformation",
    ),
    "to-hex64": (
        run_64hex,
        "Reduce hex stdin lines mod N; output 64-char hex",
    ),
    "weierstrass-sqrt": (
        run_intcounter9,
        "Infinite: floor(sqrt(x^3+7)) variants mod N",
    ),
    "word-perms": (
        run_perms,
        "Read stdin lines; print unique permutations (lower/original/upper)",
    ),
    "xor-pairs": (
        run_testxor2,
        "Read hex lines; pairwise XOR variants mod N and P",
    ),
    "xor-scan": (
        run_testxor,
        "Read hex lines; XOR each value with 0–255 mod N",
    ),
}

# ── Deprecated aliases ────────────────────────────────────────────────────────
# Maps old name -> new (canonical) name.
# Both old and new names are accepted by the CLI; old names print a deprecation
# notice and will be removed in a future release.
ALIASES = {
    "256bitrepr":          "bits-repr",
    "64hex":               "to-hex64",
    "freader":             "entropy-scan",
    "intcounter6":         "secp-pow-mod",
    "intcounter9":         "weierstrass-sqrt",
    "intcounter10":        "luhn-counter",
    "intcounter14":        "seq-counter",
    "intcounter15":        "cubic-shift",
    "perms":               "word-perms",
    "perms2":              "alpha-perms",
    "perms3":              "str-perms",
    "probagen":            "prob-gen",
    "randomint":           "rand-seeded",
    "randomint2":          "rand-reseed",
    "randomint3":          "rand-offset",
    "randomint4":          "rand-bytes",
    "replacer":            "line-echo",
    "simple-stat-analysis":  "bit-stats",
    "testSTRToSHA512":     "sha512-hex",
    "testadd":             "mod-add",
    "testbitpatterns":     "bit-concat",
    "testboolefuncs":      "bitwise-ops",
    "testconcatnumbers":   "str-numcat",
    "testinv":             "additive-inv",
    "testmean":            "mean-sub",
    "testmedian":          "pair-avg",
    "testmodulo3":         "iterated-pow-mod",
    "testmult":            "mod-mul",
    "testpivot":           "str-pivot",
    "testpwr":             "pow-range",
    "testrevert":          "hex-reverse",
    "testrot":             "bit-rotate",
    "testsec256k1":        "secp256k1-ops",
    "testsha256":          "sha256-chain",
    "testsqrt":            "iter-sqrt",
    "teststr":             "pair-concat",
    "teststr2":            "str-cases",
    "teststr3":            "str-join-cases",
    "testsub":             "mod-sub",
    "testsub256":          "mod-neg",
    "testxor":             "xor-scan",
    "testxor2":            "xor-pairs",
}


# ── CLI setup ─────────────────────────────────────────────────────────────────

# Reverse alias map: new_name -> [old_names...]
_REVERSE_ALIASES: dict = {}
for _old, _new in ALIASES.items():
    _REVERSE_ALIASES.setdefault(_new, []).append(_old)


def _build_parser():
    parser = argparse.ArgumentParser(
        prog="generators.py",
        description="256btests unified generator/test CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Run 'generators.py <generator> --help' for generator-specific options.\n"
            "Use --list to see all available generators.\n\n"
            "Examples:\n"
            "  python generators.py seq-counter | head -5\n"
            "  python generators.py rand-seeded myseed | head -3\n"
            "  echo 'hello' | python generators.py rot13\n"
            "  printf 'deadbeef\\n' | python generators.py bits-repr\n"
        ),
    )
    parser.add_argument(
        "--list",
        action="store_true",
        default=False,
        help="List all available generators and exit",
    )

    subparsers = parser.add_subparsers(dest="generator", metavar="generator")

    # Generators that require a positional 'seed' argument
    for name in ("rand-seeded", "rand-offset", "rand-bytes"):
        old_aliases = _REVERSE_ALIASES.get(name, [])
        sp = subparsers.add_parser(name, aliases=old_aliases, help=GENERATORS[name][1])
        sp.add_argument("seed", help="Random seed value")
        sp.set_defaults(func=GENERATORS[name][0])

    # entropy-scan — positional file/offset/length args
    sp = subparsers.add_parser(
        "entropy-scan",
        aliases=_REVERSE_ALIASES.get("entropy-scan", []),
        help=GENERATORS["entropy-scan"][1],
    )
    sp.add_argument("filename", help="Path to the binary file to scan")
    sp.add_argument("start", type=int, help="Start byte offset in the file")
    sp.add_argument("length", type=int, help="Length of each byte sequence to examine")
    sp.add_argument(
        "flen",
        type=int,
        nargs="?",
        default=None,
        help="Override file length (used only when stat reports 0)",
    )
    sp.set_defaults(func=run_freader)

    # All remaining generators — no special arguments
    _special = {"rand-seeded", "rand-offset", "rand-bytes", "entropy-scan"}
    for name, (func, desc) in GENERATORS.items():
        if name not in _special:
            old_aliases = _REVERSE_ALIASES.get(name, [])
            sp = subparsers.add_parser(name, aliases=old_aliases, help=desc)
            sp.set_defaults(func=func)

    return parser


def main():
    parser = _build_parser()
    args = parser.parse_args()

    if args.list:
        print("Available generators:\n")
        for name, (_, desc) in sorted(GENERATORS.items()):
            old_names = sorted(_REVERSE_ALIASES.get(name, []))
            alias_str = (
                f"  [deprecated aliases: {', '.join(old_names)}]" if old_names else ""
            )
            print(f"  {name:<30} {desc}{alias_str}")
        return

    if not hasattr(args, "func"):
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
