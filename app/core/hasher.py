import hashlib
from pathlib import Path


def sha256_bytes(data) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path, block_size: int = 1024 * 1024) -> str:
    file_path = Path(path)
    hasher = hashlib.sha256()
    with file_path.open("rb") as file:
        while True:
            block = file.read(4 *1024*1024)
            if not block:
                break
            hasher.update(block)
    return hasher.hexdigest()
