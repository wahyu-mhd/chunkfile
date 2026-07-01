import sqlite3


def log_action(
    db: sqlite3.Connection,
    user_id: int | None,
    action: str,
    file_id: int | None,
    ip_address: str | None,
    message: str,
) -> None:
    ...


def list_audit_logs(
    db: sqlite3.Connection,
    user_id: int,
    limit: int = 100,
) -> list[sqlite3.Row]:
    ...
