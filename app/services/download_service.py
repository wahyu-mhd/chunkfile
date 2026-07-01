from dataclasses import dataclass
from pathlib import Path
import sqlite3

from app.config import Settings


class HashVerificationError(RuntimeError):
    pass


@dataclass(frozen=True)
class RebuiltFile:
    path: Path
    filename: str
    mime_type: str


def rebuild_file(
    db: sqlite3.Connection,
    user_id: int,
    file_id: int,
    storage,
    settings: Settings,
    ip_address: str | None,
) -> RebuiltFile:
    ...
