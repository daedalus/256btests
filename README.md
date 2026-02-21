# 256btests

A collection of 256-bit integer generators and test scripts, now unified under a
single CLI tool: **`generators.py`**.

---

## Unified CLI — `generators.py`

`generators.py` is a self-contained Python 3 script that consolidates every
generator and test script in this repository into a single argparse-based CLI.
The old individual scripts remain in the repository unchanged.

### Requirements

Python 3.8+.  
Two generators need optional third-party packages:

| Generator | Package | Install |
|-----------|---------|---------|
| `intcounter10` | [python-stdnum](https://pypi.org/project/python-stdnum/) | `pip install python-stdnum` |
| `probagen` | [numpy](https://pypi.org/project/numpy/) | `pip install numpy` |

All other generators use only the Python standard library.

---

### List all generators

```bash
python generators.py --list
```

### General usage

```
python generators.py <generator> [options]
python generators.py <generator> --help
```

Most generators read from **stdin** and write to **stdout**, making them easy to
pipe:

```bash
# Generate 5 sequential 64-char hex values
python generators.py intcounter14 | head -5

# Pipe one generator's output into another
python generators.py intcounter14 | python generators.py testrevert | head -4

# Generate random 256-bit integers with a seed, take the first 3
python generators.py randomint myseed | head -3
```

---

### Generator reference

#### Generators with required arguments

| Generator | Arguments | Description |
|-----------|-----------|-------------|
| `randomint` | `seed` | Infinite stream of random 256-bit integers |
| `randomint3` | `seed` | Infinite stream starting at 2³², random offset per value |
| `randomint4` | `seed` | Infinite 256-bit hex strings assembled from random bytes |
| `freader` | `filename start length [flen]` | Scan a binary file for high-entropy byte sequences |

```bash
python generators.py randomint hello | head -3
python generators.py randomint3 42   | head -3
python generators.py randomint4 abc  | head -3
python generators.py freader /path/to/binary 0 16
```

#### Infinite generators (no stdin required)

| Generator | Description |
|-----------|-------------|
| `intcounter6` | Prints `(P^i % N)` and `(N^i % N)` for i = 0, 1, 2, … |
| `intcounter9` | Prints `floor(sqrt(x³+7))` variants mod N |
| `intcounter10` | Integers with their Luhn checksum digit appended |
| `intcounter14` | Sequential integers as 64-char hex |
| `intcounter15` | `(x³ << x) % N` as 64-char hex |
| `perms2` | All permutations of a–z, 0–9 and space (astronomical count) |
| `randomint2` | Random 256-bit integers; seed auto-increments every 1 000 values |
| `testbitpatterns` | 256-bit values from concatenated binary strings |
| `testmodulo3` | `((p % n)^i) % n` as 64-char hex |
| `probagen` | Weighted bit-probability model output (numpy required) |

```bash
python generators.py intcounter14   | head -5
python generators.py testbitpatterns | head -4
python generators.py randomint2     | head -3
```

#### Stdin-driven generators

These read hex-encoded 256-bit values (one per line) from stdin unless noted:

| Generator | Reads | Description |
|-----------|-------|-------------|
| `256bitrepr` | hex lines | Last 8 hex chars + binary + int |
| `64hex` | hex lines | Reduce mod N → 64-char hex |
| `testadd` | hex lines | Pairwise sums mod N |
| `testboolefuncs` | hex lines | Pairwise AND / OR / XOR mod N |
| `testinv` | hex lines | N−k, P−k, k XOR 2²⁵⁶, 2²⁵⁶−k variants mod N |
| `testmean` | hex lines | Arithmetic mean, then ∞ loop subtracting mean from N |
| `testmedian` | hex lines | Rolling pair-average mod N |
| `testmult` | hex lines | Pairwise products mod N |
| `testpwr` | hex lines | Each value raised to powers 96–127 mod N |
| `testrevert` | hex lines | Character-reversed strings |
| `testrot` | hex lines | Rotate-left / rotate-right bit variants mod N |
| `testsec256k1` | hex lines | secp256k1 curve candidate operations |
| `testsqrt` | hex lines | Iterated integer sqrt × 16 mod N |
| `testsub` | hex lines | Pairwise absolute differences mod N |
| `testsub256` | hex lines | N−k, P−k, 2²⁵⁶−k mod N |
| `testxor` | hex lines | XOR with 0–255 mod N |
| `testxor2` | hex lines | Pairwise XOR variants mod N and P |
| `testSTRToSHA512` | text lines | SHA-512 of each line mod N |
| `testsha256` | text lines | SHA-256 applied 101 times; 64-char hex output |
| `teststr` | text lines | Pairwise concatenation combinations |
| `teststr2` | text lines | title / lower / upper variants per line |
| `teststr3` | text lines | Pairwise join with case variants |
| `testconcatnumbers` | text lines | Concat with separators and numbers 0–999 |
| `perms` | text lines | Unique permutations (lower / original / upper) |
| `perms3` | text lines | All permutations of each line |
| `replacer` | text lines | Echo lines (strip CR/LF) |
| `rot13` | text lines | ROT13 transform |
| `simple-stat-analysis` | hex lines | Per-bit-position frequency count |

```bash
# Feed hex output from one generator into another
python generators.py intcounter14 | python generators.py testxor  | head -10
python generators.py intcounter14 | python generators.py testsub256 | head -6
python generators.py randomint seed1 | python generators.py testrot | head -8

# Text-based generators
echo "hello" | python generators.py rot13
printf "alice\nbob\n" | python generators.py teststr2
printf "alice\nbob\n" | python generators.py testconcatnumbers | head -20
```

---

### Stdin / stdout piping

All generators write to stdout and read from stdin (where applicable), so they
compose naturally with standard Unix tools:

```bash
# Generate and inspect
python generators.py intcounter14 | head -20

# Chain generators
python generators.py randomint seed42 | python generators.py testrevert | head -5

# Statistical analysis of generated output
python generators.py randomint seed1 | head -1000 | python generators.py simple-stat-analysis

# Save output to a file
python generators.py intcounter14 | head -100 > data.txt
```

---

### Notes on known bugs fixed in the unified script

The following bugs present in the original individual scripts would prevent
execution under Python 3 and have been fixed in `generators.py`
(the original files are left unchanged):

| Original script | Bug | Fix applied |
|-----------------|-----|-------------|
| `testinv.py` | `K` (undefined name) on the P−k line | Changed to `k` (lowercase) |
| `testsha256.py` | `bytes.encode('hex')` — Python 2 API | Changed to `bytes.hex()` |
| `testSTRToSHA512.py` | `hashlib.update(str)` — needs bytes in Python 3 | Added `.encode('utf-8')` |
| `testpivot.py` | `/` integer division (Python 2) causes `TypeError` | Changed to `//` |
| `freader.py` | Python 2 bytes/string mixing in entropy calc; `s.encode('hex')` | Rewrote entropy to use native Python 3 bytes; `s.hex()` |

---

## Legacy individual scripts

All original scripts (`256bitrepr.py`, `randomint.py`, etc.) remain in the
repository and are **unchanged**.  They are considered **deprecated** in favour
of `generators.py` but are kept for backwards compatibility.

To install optional dependencies for the legacy scripts:

```bash
pip install numpy python-stdnum
```

---

## Smoke tests

Run a quick check across several generators:

```bash
# Finite / quick generators
python generators.py intcounter14          | head -3
python generators.py testmodulo3           | head -3
python generators.py intcounter15          | head -3
python generators.py randomint testseed    | head -3
python generators.py randomint2            | head -3
python generators.py randomint3 testseed   | head -3
python generators.py randomint4 testseed   | head -3

# Stdin-driven (provide a couple of hex lines)
printf 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n' \
    | python generators.py 256bitrepr
printf 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n' \
    | python generators.py 64hex
printf 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n' \
    | python generators.py testinv
printf 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n' \
    | python generators.py testsub256
printf 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n' \
    | python generators.py testxor | head -5

# Text generators
echo "hello" | python generators.py rot13
echo "hello" | python generators.py testsha256 | head -3
echo "hello" | python generators.py testSTRToSHA512

# List
python generators.py --list
```
