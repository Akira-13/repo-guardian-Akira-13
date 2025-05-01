import zlib
from pathlib import Path


def make_loose_object(obj_type: str, data: bytes, output_path: Path):
    """Create a loose Git object with a given type and data, written as zlib-compressed file."""
    header = f"{obj_type} {len(data)}".encode("ascii") + b"\0"
    content = header + data
    compressed = zlib.compress(content)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(compressed)


def generate_object_scanner_fixtures(base_dir: Path):
    """Generate git objects to be used with the object_scanner() tests."""
    # 1. Valid blob
    make_loose_object("blob", b"Hello, Git!", base_dir / "aa" / "valid_blob")

    # 2. Unknown type
    make_loose_object("foobar", b"strange object", base_dir / "ab" / "unknown_type")

    # 3. Size mismatch (says 10, but gives 3)
    header = b"blob 10\0foo"
    compressed = zlib.compress(header)
    (base_dir / "ac").mkdir(parents=True, exist_ok=True)
    with open(base_dir / "ac" / "size_mismatch", "wb") as f:
        f.write(compressed)

    # 4. Corrupted zlib
    (base_dir / "ad").mkdir(parents=True, exist_ok=True)
    with open(base_dir / "ad" / "corrupt_zlib", "wb") as f:
        f.write(b"This is not compressed")

    # 5. Malformed header
    compressed = zlib.compress(b"blob\0just some data")
    (base_dir / "ae").mkdir(parents=True, exist_ok=True)
    with open(base_dir / "ae" / "malformed_header", "wb") as f:
        f.write(compressed)

    # 6. Empty file
    (base_dir / "af").mkdir(parents=True, exist_ok=True)
    with open(base_dir / "af" / "empty_file", "wb") as f:
        f.write(b"")

    print(f"Fixtures written to {base_dir}")


if __name__ == "__main__":
    generate_object_scanner_fixtures(Path("object_scanner_fixtures/"))
