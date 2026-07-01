from pathlib import Path


def sha256_bytes(data: bytes) -> str:
    ...


def sha256_file(path: Path, block_size: int = 1024 * 1024) -> str:
    ...
