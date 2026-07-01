from collections.abc import Iterator
import sqlite3

from app.config import Settings


def connect(settings: Settings) -> sqlite3.Connection:
    ...


def init_database(settings: Settings | None = None) -> None:
    ...


def get_db() -> Iterator[sqlite3.Connection]:
    ...
