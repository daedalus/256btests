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
| `luhn-counter` | [python-stdnum](https://pypi.org/project/python-stdnum/) | `pip install python-stdnum` |
| `prob-gen` | [numpy](https://pypi.org/project/numpy/) | `pip install numpy` |

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
python generators.py seq-counter | head -5

# Pipe one generator's output into another
python generators.py seq-counter | python generators.py hex-reverse | head -4

# Generate random 256-bit integers with a seed, take the first 3
python generators.py rand-seeded myseed | head -3
```

---

### Generator name mapping (old → new)

Generator names have been updated to be more mathematically descriptive.
The old names are still accepted as **deprecated aliases** and will continue
to work indefinitely, but new scripts should use the new names.

| Name | Description |
|-----------------------------|-----------------------------|
| `bits-repr` | Last-8-char hex + binary + integer representation |
| `to-hex64` | Reduce mod N → 64-char hex |
| `entropy-scan` | Scan binary file for high-entropy byte sequences |
| `secp-pow-mod` | P^i mod N and N^i mod N (secp256k1 constants) |
| `weierstrass-sqrt` | floor(sqrt(x³+7)) variants mod N (Weierstrass curve) |
| `luhn-counter` | Integers with Luhn checksum digit appended |
| `seq-counter` | Sequential integers as 64-char hex |
| `cubic-shift` | (x³ << x) mod N as 64-char hex |
| `word-perms` | Unique permutations of stdin words |
| `alpha-perms` | All permutations of a–z, 0–9 and space |
| `str-perms` | All permutations of each stdin line |
| `prob-gen` | Weighted bit-probability model output |
| `rand-seeded` | Uniform random 256-bit integers (seeded) |
| `rand-reseed` | Random 256-bit integers; seed auto-increments every 1,000 values |
| `rand-offset` | Random integers starting at 2³² (seeded) |
| `rand-bytes` | 256-bit hex strings assembled from random bytes (seeded) |
| `line-echo` | Echo lines (strip CR/LF) |
| `bit-stats` | Per-bit-position frequency count |
| `sha512-hex` | SHA-512 of each line mod N |
| `mod-add` | Pairwise sums mod N |
| `bit-concat` | 256-bit values from concatenated binary strings |
| `bitwise-ops` | Pairwise AND / OR / XOR mod N |
| `str-numcat` | Concat with separators and numbers 0–999 |
| `additive-inv` | N−k, P−k, k XOR 2²⁵⁶, 2²⁵⁶−k variants mod N |
| `mean-sub` | Arithmetic mean, then ∞ loop subtracting mean from N |
| `pair-avg` | Rolling pair-average mod N |
| `iterated-pow-mod` | ((p % n)^i) % n as 64-char hex |
| `mod-mul` | Pairwise products mod N |
| `str-pivot` | Recursive pivot string transformation |
| `pow-range` | Each value raised to powers 96–127 mod N |
| `hex-reverse` | Character-reversed strings |
| `bit-rotate` | Rotate-left / rotate-right bit variants mod N |
| `secp256k1-ops` | secp256k1 curve candidate operations |
| `sha256-chain` | SHA-256 applied 101 times; 64-char hex output |
| `iter-sqrt` | Iterated integer sqrt × 16 mod N |
| `pair-concat` | Pairwise concatenation combinations |
| `str-cases` | title / lower / upper variants per line |
| `str-join-cases` | Pairwise join with case variants |
| `mod-sub` | Pairwise absolute differences mod N |
| `mod-neg` | N−k, P−k, 2²⁵⁶−k mod N |
| `xor-scan` | XOR with 0–255 mod N |
| `xor-pairs` | Pairwise XOR variants mod N and P |

`rot13` retains its name (ROT13 is already the standard mathematical name).

The following generators are new and have no legacy alias:

| Generator | Description |
|-----------|-------------|
| `mod-div` | Pairwise modular division a·inv(b) mod N; skip non-invertible pairs |
| `neg` | Additive inverse (−x) mod N for each input |
| `abs-diff` | Pairwise abs(a−b) mod N without skip threshold |
| `bit-not` | Bitwise NOT of each 256-bit value (masked to 256 bits, no field reduction) |
| `bit-and` | Pairwise bitwise AND (256-bit word, no field reduction) |
| `bit-or` | Pairwise bitwise OR (256-bit word, no field reduction) |
| `shl` | Left-shift each value by k bits, masked to 256 bits (use `--shift k`) |
| `shr` | Right-shift each value by k bits (use `--shift k`) |
| `gcd` | GCD of each pair, output as 64-char hex |
| `xgcd` | Extended GCD per pair: `g x y` where a·x + b·y = g |
| `mod-reduce` | Reduce decimal or hex input mod N → 64-char hex |

---

### Generator reference

#### Generators with required arguments

| Generator | Arguments | Description |
|-----------|-----------|-------------|
| `rand-seeded` | `seed` | Infinite stream of random 256-bit integers |
| `rand-offset` | `seed` | Infinite stream starting at 2³², random offset per value |
| `rand-bytes` | `seed` | Infinite 256-bit hex strings assembled from random bytes |
| `entropy-scan` | `filename start length [flen]` | Scan a binary file for high-entropy byte sequences |

```bash
python generators.py rand-seeded hello | head -3
python generators.py rand-offset 42   | head -3
python generators.py rand-bytes abc  | head -3
python generators.py entropy-scan /path/to/binary 0 16
```

#### Infinite generators (no stdin required)

| Generator | Description |
|-----------|-------------|
| `secp-pow-mod` | Prints `(P^i % N)` and `(N^i % N)` for i = 0, 1, 2, … |
| `weierstrass-sqrt` | Prints `floor(sqrt(x³+7))` variants mod N |
| `luhn-counter` | Integers with their Luhn checksum digit appended |
| `seq-counter` | Sequential integers as 64-char hex |
| `cubic-shift` | `(x³ << x) % N` as 64-char hex |
| `alpha-perms` | All permutations of a–z, 0–9 and space (astronomical count) |
| `rand-reseed` | Random 256-bit integers; seed auto-increments every 1,000 values |
| `bit-concat` | 256-bit values from concatenated binary strings |
| `iterated-pow-mod` | `((p % n)^i) % n` as 64-char hex |
| `prob-gen` | Weighted bit-probability model output (numpy required) |

```bash
python generators.py seq-counter   | head -5
python generators.py bit-concat | head -4
python generators.py rand-reseed     | head -3
```

#### Stdin-driven generators

These read hex-encoded 256-bit values (one per line) from stdin unless noted:

| Generator | Reads | Description |
|-----------|-------|-------------|
| `bits-repr` | hex lines | Last 8 hex chars + binary + int |
| `to-hex64` | hex lines | Reduce mod N → 64-char hex |
| `mod-add` | hex lines | Pairwise sums mod N |
| `bitwise-ops` | hex lines | Pairwise AND / OR / XOR mod N |
| `additive-inv` | hex lines | N−k, P−k, k XOR 2²⁵⁶, 2²⁵⁶−k variants mod N |
| `mean-sub` | hex lines | Arithmetic mean, then ∞ loop subtracting mean from N |
| `pair-avg` | hex lines | Rolling pair-average mod N |
| `mod-mul` | hex lines | Pairwise products mod N |
| `pow-range` | hex lines | Each value raised to powers 96–127 mod N |
| `hex-reverse` | hex lines | Character-reversed strings |
| `bit-rotate` | hex lines | Rotate-left / rotate-right bit variants mod N |
| `secp256k1-ops` | hex lines | secp256k1 curve candidate operations |
| `iter-sqrt` | hex lines | Iterated integer sqrt × 16 mod N |
| `mod-sub` | hex lines | Pairwise absolute differences mod N |
| `mod-neg` | hex lines | N−k, P−k, 2²⁵⁶−k mod N |
| `xor-scan` | hex lines | XOR with 0–255 mod N |
| `xor-pairs` | hex lines | Pairwise XOR variants mod N and P |
| `sha512-hex` | text lines | SHA-512 of each line mod N |
| `sha256-chain` | text lines | SHA-256 applied 101 times; 64-char hex output |
| `pair-concat` | text lines | Pairwise concatenation combinations |
| `str-cases` | text lines | title / lower / upper variants per line |
| `str-join-cases` | text lines | Pairwise join with case variants |
| `str-numcat` | text lines | Concat with separators and numbers 0–999 |
| `word-perms` | text lines | Unique permutations (lower / original / upper) |
| `str-perms` | text lines | All permutations of each line |
| `line-echo` | text lines | Echo lines (strip CR/LF) |
| `rot13` | text lines | ROT13 transform |
| `bit-stats` | hex lines | Per-bit-position frequency count |

#### New generators

These generators are new additions with no legacy alias:

| Generator | Reads | Description |
|-----------|-------|-------------|
| `neg` | hex lines | Additive inverse (−x) mod N; one value per input line |
| `abs-diff` | hex lines | Pairwise abs(a−b) mod N; no skip threshold |
| `bit-not` | hex lines | Bitwise NOT (flip all 256 bits); no field reduction |
| `bit-and` | hex lines | Pairwise bitwise AND; 256-bit word, no field reduction |
| `bit-or` | hex lines | Pairwise bitwise OR; 256-bit word, no field reduction |
| `shl` | hex lines | Left-shift each value by `--shift k` bits (default 1) |
| `shr` | hex lines | Right-shift each value by `--shift k` bits (default 1) |
| `gcd` | hex lines | GCD of each pair as 64-char hex |
| `xgcd` | hex lines | Extended GCD per pair: `g x y` on each line |
| `mod-div` | hex lines | Pairwise a·inv(b) mod N; skip non-invertible pairs |
| `mod-reduce` | decimal/hex lines | Reduce x mod N → 64-char hex |

**Semantics notes:**

- `bit-not`, `bit-and`, `bit-or`, `shl`, `shr` operate on raw 256-bit words (no
  modular reduction); output is a 256-bit value zfill-padded to 64 hex chars.
- `mod-div`: when b has no modular inverse modulo N (i.e. `gcd(b, N) ≠ 1`), the
  pair is silently skipped and a diagnostic is written to stderr.
- `xgcd` output uses three space-separated fields per line: the GCD `g` (64-char
  hex), and the Bézout coefficients `x` and `y` (signed decimal integers) such
  that `a·x + b·y = g`.
- `mod-reduce` accepts lines starting with `0x`/`0X` as hex, otherwise tries
  decimal first and then bare hex.

```bash
# neg — additive inverse
echo "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" \
    | python generators.py neg

# bit-not — flip all 256 bits
echo "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" \
    | python generators.py bit-not

# shl / shr — logical shifts (need at least 1 input line)
python generators.py seq-counter | head -5 | python generators.py shl --shift 8
python generators.py seq-counter | head -5 | python generators.py shr --shift 8

# abs-diff, bit-and, bit-or, gcd, xgcd, mod-div — pairwise (need ≥3 lines)
python generators.py seq-counter | head -5 | python generators.py abs-diff | head -6
python generators.py seq-counter | head -5 | python generators.py bit-and  | head -6
python generators.py seq-counter | head -5 | python generators.py bit-or   | head -6
python generators.py seq-counter | head -5 | python generators.py gcd      | head -6
python generators.py seq-counter | head -5 | python generators.py xgcd     | head -6
python generators.py seq-counter | head -5 | python generators.py mod-div  | head -6

# mod-reduce — decimal or hex input
echo "12345"      | python generators.py mod-reduce
echo "0xdeadbeef" | python generators.py mod-reduce
python generators.py seq-counter | head -3 | python generators.py mod-reduce
```

```bash
# Feed hex output from one generator into another
python generators.py seq-counter | python generators.py xor-scan  | head -10
python generators.py seq-counter | python generators.py mod-neg | head -6
python generators.py rand-seeded seed1 | python generators.py bit-rotate | head -8

# Text-based generators
echo "hello" | python generators.py rot13
printf "alice\nbob\n" | python generators.py str-cases
printf "alice\nbob\n" | python generators.py str-numcat | head -20
```

---

### Stdin / stdout piping

All generators write to stdout and read from stdin (where applicable), so they
compose naturally with standard Unix tools:

```bash
# Generate and inspect
python generators.py seq-counter | head -20

# Chain generators
python generators.py rand-seeded seed42 | python generators.py hex-reverse | head -5

# Statistical analysis of generated output
python generators.py rand-seeded seed1 | head -1000 | python generators.py bit-stats

# Save output to a file
python generators.py seq-counter | head -100 > data.txt
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
python generators.py seq-counter          | head -3
python generators.py iterated-pow-mod     | head -3
python generators.py cubic-shift          | head -3
python generators.py rand-seeded testseed | head -3
python generators.py rand-reseed          | head -3
python generators.py rand-offset testseed | head -3
python generators.py rand-bytes testseed  | head -3

# Old names (deprecated aliases) still work
python generators.py intcounter14         | head -3
python generators.py randomint testseed   | head -3

# Stdin-driven (provide a couple of hex lines)
printf 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n' \
    | python generators.py bits-repr
printf 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n' \
    | python generators.py to-hex64
printf 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n' \
    | python generators.py additive-inv
printf 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n' \
    | python generators.py mod-neg
printf 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n' \
    | python generators.py xor-scan | head -5

# Text generators
echo "hello" | python generators.py rot13
echo "hello" | python generators.py sha256-chain | head -3
echo "hello" | python generators.py sha512-hex

# List
python generators.py --list
```
