import uuid

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID, INET, BYTEA
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    username= mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash = mapped_column(
        Text,
        nullable=False,
    )

    created_at= mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    files = relationship("StoredFile", back_populates="user")


class StoredFile(Base):
    __tablename__ = "files"

    i= mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_i= mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    original_filenam= mapped_column(
        Text,
        nullable=False,
    )

    size_byte= mapped_column(
        BigInteger,
        nullable=False,
    )

    mime_typ = mapped_column(
        Text,
        nullable=True,
    )

    statu= mapped_column(
        String(20),
        nullable=False,
        default="uploading",
        index=True,
    )

    created_a= mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_a= mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user = relationship("User", back_populates="files")
    chunks = relationship(
        "Chunk",
        back_populates="file",
        cascade="all, delete-orphan",
        order_by="Chunk.chunk_index",
    )


class Chunk(Base):
    __tablename__ = "chunks"

    id= mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    file_id= mapped_column(
        UUID(as_uuid=True),
        ForeignKey("files.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    chunk_index= mapped_column(
        Integer,
        nullable=False,
    )

    object_key= mapped_column(
        Text,
        nullable=False,
    )

    encrypted_size= mapped_column(
        BigInteger,
        nullable=False,
    )

    sha256_encrypted= mapped_column(
        String(64),
        nullable=False,
    )

    nonce = mapped_column(
        BYTEA,
        nullable=False,
    )

    created_at= mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    file = relationship("StoredFile", back_populates="chunks")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id= mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id= mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    file_id= mapped_column(
        UUID(as_uuid=True),
        ForeignKey("files.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    action= mapped_column(
        String(50),
        nullable=False,
    )

    ip_address = mapped_column(
        INET,
        nullable=True,
    )

    message= mapped_column(
        Text,
        nullable=True,
    )

    created_at = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )