from collections.abc import Iterator
from pathlib import Path


DEFAULT_CHUNK_SIZE = 1024 * 1024


def iter_file_chunks(path: Path, chunk_size: int = DEFAULT_CHUNK_SIZE) -> Iterator[bytes]:
    ...


def count_chunks(size_bytes: int, chunk_size: int = DEFAULT_CHUNK_SIZE) -> int:
    ...
