import sys
from io import StringIO

import pytest


@pytest.fixture
def sample_hex_lines():
    return StringIO(
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n"
        "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff\n"
        "0000000000000000000000000000000000000000000000000000000000000001\n"
    )


@pytest.fixture
def single_hex_line():
    return StringIO(
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n"
    )


@pytest.fixture
def empty_hex_lines():
    return StringIO("")


@pytest.fixture
def text_lines():
    return StringIO("hello\nworld\ntest\n")


@pytest.fixture
def mock_stdin(monkeypatch, sample_hex_lines):
    monkeypatch.setattr(sys, "stdin", sample_hex_lines)


@pytest.fixture
def hex_value():
    return "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
