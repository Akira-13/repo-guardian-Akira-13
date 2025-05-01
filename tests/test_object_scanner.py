"""
Suite of tests for the object_scanner.py.

Uses objects from the fixtures/ directory.

...

Tests
-----
test_read_valid_blob()
test_read_unknown_type()
test_read_corrupt_zlib()
test_read_malformed_header()
test_read_size_mismatch()
test_read_valid_blob()
test_read_empty_file()
"""

import pytest
from pathlib import Path
from src.object_scanner import read_loose

FIXTURES = Path("fixtures/object_scanner_fixtures")


def test_read_valid_blob():
    """Reads valid git object files (expected type, content, correct hash)."""
    path = FIXTURES / "aa" / "valid_blob"
    obj = read_loose(path)
    assert obj.type == "blob"
    assert isinstance(obj.data, bytes)
    assert obj.size == len(obj.data)
    assert obj.data == b"Hello, Git!"


def test_read_unknown_type(tmp_path):
    """Recognizes header has an unknown type."""
    path = FIXTURES / "ab" / "unknown_type"
    with pytest.raises(ValueError, match="Unknown Git object type"):
        read_loose(path)


def test_read_corrupt_zlib(tmp_path):
    """Recognizes invalid or tampered data."""
    path = FIXTURES / "ad" / "corrupt_zlib"
    with pytest.raises(ValueError, match="decompress|Corrupt"):
        read_loose(path)


def test_read_malformed_header(tmp_path):
    """Recognizes a malformed header."""
    path = FIXTURES / "ae" / "malformed_header"
    with pytest.raises(ValueError, match="Invalid Git object header|Malformed"):
        read_loose(path)


def test_read_size_mismatch(tmp_path):
    """Recognizes a size mismatch in the object."""
    path = FIXTURES / "ac" / "size_mismatch"
    with pytest.raises(ValueError, match="Size mismatch"):
        read_loose(path)


def test_read_empty_file():
    """Recongizes empty file."""
    path = FIXTURES / "af" / "empty_file"
    with pytest.raises(ValueError):
        read_loose(path)
