from collections.abc import Iterable
from pathlib import Path


def rebuild_from_plain_chunks(chunks: Iterable[bytes], output_path: Path) -> Path:
    ...


def cleanup_file(path: Path) -> None:
    ...
