import sqlite3


def delete_file(
    db: sqlite3.Connection,
    user_id: int,
    file_id: int,
    storage,
    ip_address: str | None,
) -> None:
    ...
