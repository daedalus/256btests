import sys
from io import StringIO

from b256tests.generators import (
    ALIASES,
    GENERATORS,
    N,
    P,
    hexify,
    run_64hex,
    run_256bitrepr,
    run_bit_not,
    run_mod_reduce,
    run_neg,
    run_rot13,
)


class TestHexify:
    def test_hexify_zero(self):
        assert hexify(0) == "0" * 64

    def test_hexify_one(self):
        assert hexify(1) == "0" * 63 + "1"

    def test_hexify_large(self):
        result = hexify(2**256 - 1)
        assert result == "f" * 64

    def test_hexify_max_int(self):
        result = hexify(2**255)
        assert (
            result == "8000000000000000000000000000000000000000000000000000000000000000"
        )


class TestSeqCounter:
    def test_seq_counter_in_generators(self):
        assert "seq-counter" in GENERATORS


class TestSecpPowMod:
    def test_secp_pow_mod_in_generators(self):
        assert "secp-pow-mod" in GENERATORS


class TestRandSeeded:
    def test_rand_seeded_in_generators(self):
        assert "rand-seeded" in GENERATORS


class TestNeg:
    def test_neg_zero(self, mock_stdin, capsys):
        stdin = StringIO("0" * 64 + "\n")
        sys.stdin = stdin
        args = type("Args", (), {})()
        run_neg(args)
        captured = capsys.readouterr()
        assert captured.out.strip() == "0" * 64

    def test_neg_one(self, mock_stdin, capsys):
        stdin = StringIO("0" * 63 + "1\n")
        sys.stdin = stdin
        args = type("Args", (), {})()
        run_neg(args)
        captured = capsys.readouterr()
        assert captured.out.strip() == hex(N - 1).replace("0x", "").zfill(64)

    def test_neg_all_ones(self, mock_stdin, capsys):
        stdin = StringIO("f" * 64 + "\n")
        sys.stdin = stdin
        args = type("Args", (), {})()
        run_neg(args)
        captured = capsys.readouterr()
        result = int(captured.out.strip(), 16)
        expected = (N - (2**256 - 1)) % N
        assert result == expected


class TestBitNot:
    def test_bit_not_zero(self, mock_stdin, capsys):
        stdin = StringIO("0" * 64 + "\n")
        sys.stdin = stdin
        args = type("Args", (), {})()
        run_bit_not(args)
        captured = capsys.readouterr()
        assert captured.out.strip() == "f" * 64

    def test_bit_not_all_ones(self, mock_stdin, capsys):
        stdin = StringIO("f" * 64 + "\n")
        sys.stdin = stdin
        args = type("Args", (), {})()
        run_bit_not(args)
        captured = capsys.readouterr()
        assert captured.out.strip() == "0" * 64


class TestModReduce:
    def test_mod_reduce_decimal(self, mock_stdin, capsys):
        stdin = StringIO("12345\n")
        sys.stdin = stdin
        args = type("Args", (), {})()
        run_mod_reduce(args)
        captured = capsys.readouterr()
        assert captured.out.strip() == hex(12345 % N).replace("0x", "").zfill(64)

    def test_mod_reduce_hex(self, mock_stdin, capsys):
        stdin = StringIO("0xdeadbeef\n")
        sys.stdin = stdin
        args = type("Args", (), {})()
        run_mod_reduce(args)
        captured = capsys.readouterr()
        expected = hex(0xDEADBEEF % N).replace("0x", "").zfill(64)
        assert captured.out.strip() == expected

    def test_mod_reduce_large_hex(self, mock_stdin, capsys):
        stdin = StringIO("f" * 64 + "\n")
        sys.stdin = stdin
        args = type("Args", (), {})()
        run_mod_reduce(args)
        captured = capsys.readouterr()
        assert captured.out.strip() == hex(
            0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF % N
        ).replace("0x", "").zfill(64)


class TestRot13:
    def test_rot13_hello(self, mock_stdin, capsys):
        stdin = StringIO("hello\n")
        sys.stdin = stdin
        args = type("Args", (), {})()
        run_rot13(args)
        captured = capsys.readouterr()
        assert captured.out.strip() == "uryyb"

    def test_rot13_uryyb(self, mock_stdin, capsys):
        stdin = StringIO("uryyb\n")
        sys.stdin = stdin
        args = type("Args", (), {})()
        run_rot13(args)
        captured = capsys.readouterr()
        assert captured.out.strip() == "hello"


class TestBitsRepr:
    def test_bits_repr_hex(self, mock_stdin, capsys):
        stdin = StringIO(
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n"
        )
        sys.stdin = stdin
        args = type("Args", (), {})()
        run_256bitrepr(args)
        captured = capsys.readouterr()
        lines = captured.out.strip().split()
        assert lines[0] == "aaaaaaaa"
        assert "0b" in lines[1]


class TestToHex64:
    def test_to_hex64_two_chars(self, mock_stdin, capsys):
        stdin = StringIO("ff\n")
        sys.stdin = stdin
        args = type("Args", (), {})()
        run_64hex(args)
        captured = capsys.readouterr()
        assert captured.out.strip() == hex(0xFF % N).replace("0x", "").zfill(64)

    def test_to_hex64_large(self, mock_stdin, capsys):
        stdin = StringIO("ff" * 64 + "\n")
        sys.stdin = stdin
        args = type("Args", (), {})()
        run_64hex(args)
        captured = capsys.readouterr()
        assert captured.out.strip() == hex(int("ff" * 64, 16) % N).replace(
            "0x", ""
        ).zfill(64)


class TestRegistry:
    def test_generators_not_empty(self):
        assert len(GENERATORS) > 0

    def test_aliases_not_empty(self):
        assert len(ALIASES) > 0

    def test_seq_counter_in_generators(self):
        assert "seq-counter" in GENERATORS

    def test_deprecated_alias_works(self):
        assert "intcounter14" in ALIASES
        assert ALIASES["intcounter14"] == "seq-counter"


class TestConstants:
    def test_p_is_secp256k1_prime(self):
        expected_p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
        assert P == expected_p

    def test_n_is_secp256k1_order(self):
        expected_n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
        assert N == expected_n


class TestEdgeCases:
    def test_empty_stdin_no_output(self, capsys):
        stdin = StringIO("")
        sys.stdin = stdin
        args = type("Args", (), {})()
        run_neg(args)
        captured = capsys.readouterr()
        assert captured.out == ""

    def test_invalid_hex_skipped(self, capsys):
        stdin = StringIO("notahex\n")
        sys.stdin = stdin
        args = type("Args", (), {})()
        run_neg(args)
        captured = capsys.readouterr()
        assert captured.out == ""

    def test_whitespace_handled(self, capsys):
        stdin = StringIO("  aaaa  \n")
        sys.stdin = stdin
        args = type("Args", (), {})()
        run_neg(args)
        captured = capsys.readouterr()
        assert captured.out.strip() != ""
