# SPEC.md — 256btests

## Purpose

A collection of 256-bit integer generators and test scripts, unified under a single CLI tool. The project provides various generators for creating, transforming, and analyzing 256-bit hex values, useful for cryptographic testing, fuzzing, and research purposes.

## Scope

- **In Scope:**
  - CLI tool with multiple generator subcommands
  - Generators for creating 256-bit values (sequential, random, seeded)
  - Generators for transforming 256-bit values (bitwise ops, modular arithmetic, hashing)
  - Generators for text transformation (ROT13, case variants, permutations)
  - Generators for statistical analysis (bit frequency, entropy)
  - Backward compatibility with deprecated legacy script names
  - Support for stdin/stdout piping for composition

- **Not in Scope:**
  - GUI or web interface
  - Database storage
  - Network API
  - MCP server functionality

## Public API / Interface

### CLI Entry Point

```bash
b256tests --help
b256tests --list
b256tests <generator> [options]
b256tests <generator> --help
```

### Generators (by category)

**Infinite generators (no stdin required):**
| Generator | Args | Description |
|-----------|------|-------------|
| `secp-pow-mod` | - | Prints (P^i % N) and (N^i % N) for i = 0, 1, 2, ... |
| `weierstrass-sqrt` | - | Prints floor(sqrt(x³+7)) variants mod N |
| `luhn-counter` | - | Integers with Luhn checksum digit (requires python-stdnum) |
| `seq-counter` | - | Sequential integers as 64-char hex |
| `cubic-shift` | - | (x³ << x) % N as 64-char hex |
| `alpha-perms` | - | All permutations of a-z, 0-9 and space |
| `rand-reseed` | - | Random 256-bit integers; seed auto-increments every 1000 values |
| `bit-concat` | - | 256-bit values from concatenated binary strings |
| `iterated-pow-mod` | - | ((p % n)^i) % n as 64-char hex |
| `prob-gen` | - | Weighted bit-probability model output (requires numpy) |

**Generators requiring seed argument:**
| Generator | Args | Description |
|-----------|------|-------------|
| `rand-seeded` | seed | Infinite stream of random 256-bit integers |
| `rand-offset` | seed | Infinite stream starting at 2³², random offset per value |
| `rand-bytes` | seed | Infinite 256-bit hex strings from random bytes |

**Generators requiring file arguments:**
| Generator | Args | Description |
|-----------|------|-------------|
| `entropy-scan` | filename start length [flen] | Scan binary file for high-entropy byte sequences |

**Stdin-driven generators (hex input):**
| Generator | Description |
|-----------|-------------|
| `bits-repr` | Last 8 hex chars + binary + integer |
| `to-hex64` | Reduce mod N to 64-char hex |
| `mod-add` | Pairwise sums mod N |
| `bitwise-ops` | Pairwise AND/OR/XOR mod N |
| `additive-inv` | N-k, P-k, k XOR 2²⁵⁶, 2²⁵⁶-k mod N |
| `mean-sub` | Arithmetic mean, then infinite loop subtracting mean from N |
| `pair-avg` | Rolling pair-average mod N |
| `mod-mul` | Pairwise products mod N |
| `pow-range` | Each value raised to powers 96-127 mod N |
| `hex-reverse` | Character-reversed strings |
| `bit-rotate` | Rotate-left/right bit variants mod N |
| `secp256k1-ops` | secp256k1 curve candidate operations |
| `iter-sqrt` | Iterated integer sqrt × 16 mod N |
| `mod-sub` | Pairwise absolute differences mod N |
| `mod-neg` | N-k, P-k, 2²⁵⁶-k mod N |
| `xor-scan` | XOR with 0-255 mod N |
| `xor-pairs` | Pairwise XOR variants mod N and P |
| `neg` | Additive inverse (-x) mod N |
| `abs-diff` | Pairwise abs(a-b) mod N |
| `bit-not` | Bitwise NOT (masked to 256 bits) |
| `bit-and` | Pairwise bitwise AND |
| `bit-or` | Pairwise bitwise OR |
| `shl` | Left-shift by k bits (--shift k) |
| `shr` | Right-shift by k bits (--shift k) |
| `gcd` | GCD of each pair |
| `xgcd` | Extended GCD per pair (g x y) |
| `mod-div` | Pairwise modular division a*inv(b) mod N |
| `mod-reduce` | Reduce decimal or hex mod N |

**Stdin-driven generators (text input):**
| Generator | Description |
|-----------|-------------|
| `sha512-hex` | SHA-512 of each line mod N |
| `sha256-chain` | SHA-256 applied 101 times |
| `pair-concat` | Pairwise concatenation combinations |
| `str-cases` | Title/lower/upper variants |
| `str-join-cases` | Pairwise join with case variants |
| `str-numcat` | Concat with numbers 0-999 |
| `word-perms` | Unique permutations |
| `str-perms` | All permutations of each line |
| `line-echo` | Echo lines (strip CR/LF) |
| `rot13` | ROT13 transform |
| `bit-stats` | Per-bit-position frequency count |

### Python API

```python
from b256tests import __version__
from b256tests.generators import run_seq_counter, run_rand_seeded
```

## Data Formats

- **Input:** Hex-encoded 256-bit values (64 hex characters), one per line
- **Output:** Hex-encoded 256-bit values (64 hex characters), one per line
- **Text generators:** UTF-8 encoded text, line-delimited

## Edge Cases

1. Empty stdin for stdin-driven generators: No output produced
2. Invalid hex input (non-hex characters): Skip line, continue processing
3. Zero divisor in mod-div: Skip pair, write diagnostic to stderr
4. Non-invertible modular divisor (gcd(b, N) != 1): Skip pair, write diagnostic to stderr
5. Very long input lines: Truncate to 64 chars before processing
6. Files with zero size in entropy-scan: Use flen override if provided
7. Seed argument with special characters: Convert to string for random.seed()
8. Lines starting with 0x/0X in mod-reduce: Interpret as hex

## Performance & Constraints

- All generators are streaming (process line-by-line)
- No artificial limits on output size (infinite generators run until killed)
- Memory usage: O(n) where n is stdin line count for pairwise generators
- No external dependencies for core generators (stdlib only)
- Optional dependencies: numpy, python-stdnum for specific generators
