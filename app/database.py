# from collections.abc import Iterator
# import sqlite3

# from app.config import Settings


# def connect(settings: Settings) -> sqlite3.Connection:
#     ...


# def init_database(settings: Settings | None = None) -> None:
#     ...


# def get_db() -> Iterator[sqlite3.Connection]:
#     ...

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings


engine = create_engine(
    settings.database_url,
    echo=True if settings.app_env == "development" else False,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()