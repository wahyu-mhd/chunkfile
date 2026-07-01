from collections.abc import Iterable
from typing import Any


class ManifestError(ValueError):
    pass


def chunk_object_key(user_id: int, file_id: int, chunk_index: int) -> str:
    ...


def ordered_chunks(rows: Iterable[Any]) -> list[Any]:
    ...
