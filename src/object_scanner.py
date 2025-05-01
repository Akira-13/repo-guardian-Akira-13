"""This module contains the Object Scanner functions to read loose objects."""

import zlib
from dataclasses import dataclass
from pathlib import Path


@dataclass
class GitObject:
    """
    Information of a Git object.

    ...

    Attributes
    ----------
    type : str
        String that represents the type of object.
    size : int
        Size of the object in bytes.
    data : bytes
        Bytes with the actual content of the object.
    """

    type: str
    size: int
    data: bytes


def read_loose(path: Path) -> GitObject:
    """
    Read loose raw objects in a .git directory.

    Parameters
    ----------
    path : Path
        Path of the .git directory.

    Returns
    -------
    GitObject
        Git object with its header and content data.

    Raises
    ------
    ValueError
        If tthere is any error with the reading of the object.
    """
    try:
        with open(path, "rb") as f:
            raw_data = f.read()
        decompressed = zlib.decompress(raw_data)
    except zlib.error as e:
        raise ValueError("Corrupt or unreadable Git object") from e

    header, sep, content = decompressed.partition(b"\0")
    if sep == b"":
        raise ValueError("Malformed Git object: missing header/content separator")

    try:
        type_str, size_str = header.decode("ascii").split()
        size = int(size_str)
    except Exception as e:
        raise ValueError(f"Invalid Git object header: {header}") from e

    if type_str not in {"blob", "tree", "commit", "tag"}:
        raise ValueError(f"Unknown Git object type: {type_str}")

    if len(content) != size:
        raise ValueError(
            f"Size mismatch: header says {size}, content is {len(content)}"
        )

    return GitObject(type=type_str, size=size, data=content)
