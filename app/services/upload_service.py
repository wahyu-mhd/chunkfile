import sqlite3

from fastapi import UploadFile

from app.config import Settings


async def upload_file(
    db: sqlite3.Connection,
    user_id: int,
    upload: UploadFile,
    storage,
    settings: Settings,
    ip_address: str | None,
) -> sqlite3.Row:
    ...
