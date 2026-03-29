# 256btests

> A collection of 256-bit integer generators and test scripts, unified under a single CLI tool.

[![PyPI](https://img.shields.io/pypi/v/b256tests.svg)](https://pypi.org/project/b256tests/)
[![Python](https://img.shields.io/pypi/pyversions/b256tests.svg)](https://pypi.org/project/b256tests/)
[![Coverage](https://codecov.io/gh/daedalus/256btests/branch/main/graph/badge.svg)](https://codecov.io/gh/daedalus/256btests)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Install

```bash
pip install b256tests
```

## Usage (Python)

```python
from b256tests import GENERATORS, ALIASES

# Access constants
from b256tests import P, N
```

## CLI

```bash
b256tests --help
b256tests --list
b256tests <generator> [options]
b256tests <generator> --help
```

### Examples

```bash
# Generate 5 sequential 64-char hex values
b256tests seq-counter | head -5

# Pipe one generator's output into another
b256tests seq-counter | b256tests hex-reverse | head -4

# Generate random 256-bit integers with a seed, take the first 3
b256tests rand-seeded myseed | head -3

# Text transformations
echo "hello" | b256tests rot13

# List all generators
b256tests --list
```

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
| `neg` | hex lines | Additive inverse (−x) mod N |
| `abs-diff` | hex lines | Pairwise abs(a−b) mod N |
| `bit-not` | hex lines | Bitwise NOT (flip all 256 bits) |
| `bit-and` | hex lines | Pairwise bitwise AND |
| `bit-or` | hex lines | Pairwise bitwise OR |
| `shl` | hex lines | Left-shift by `--shift k` bits |
| `shr` | hex lines | Right-shift by `--shift k` bits |
| `gcd` | hex lines | GCD of each pair |
| `xgcd` | hex lines | Extended GCD per pair: `g x y` |
| `mod-div` | hex lines | Pairwise a·inv(b) mod N |
| `mod-reduce` | decimal/hex lines | Reduce mod N |

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

## API

### Constants

- `P`: secp256k1 prime field modulus
- `N`: secp256k1 curve order

### Registry

- `GENERATORS`: Dictionary of all available generator names to (function, description) tuples
- `ALIASES`: Dictionary mapping deprecated names to current names

## Development

```bash
git clone https://github.com/daedalus/256btests.git
cd 256btests
pip install -e ".[test]"

# run tests
pytest

# format
ruff format src/ tests/

# lint
ruff check src/ tests/

# type check
mypy src/
```

## Optional Dependencies

Some generators require additional packages:

| Generator | Package | Install |
|-----------|---------|---------|
| `luhn-counter` | python-stdnum | `pip install python-stdnum` |
| `prob-gen` | numpy | `pip install numpy` |

---

## Legacy individual scripts

All original scripts (`256bitrepr.py`, `randomint.py`, etc.) remain in the
repository and are **unchanged**.  They are considered **deprecated** in favour
of `b256tests` but are kept for backwards compatibility.

To install optional dependencies for the legacy scripts:

```bash
pip install numpy python-stdnum
```
