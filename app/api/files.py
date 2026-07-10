import shutil
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.config import settings
from app.core.chunker import iter_file_chunks
from app.core.crypto import encrypt_chunk, load_master_key
from app.core.hasher import sha256_bytes
from app.core.storage_b2 import B2Storage
from app.database import get_db
from app.models import Chunk, StoredFile, User
from app.schemas import FileRead

router = APIRouter(prefix="/files", tags=["files"])


def get_or_create_dev_user(db: Session) -> User:
    user = db.query(User).filter(User.username == "dev").first()

    if user is not None:
        return user

    user = User(
        username="dev",
        password_hash="dev-only-not-production",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def save_to_staging(upload_file: UploadFile) -> Path:
    staging_dir = Path("data/staging")
    staging_dir.mkdir(parents=True, exist_ok=True)

    safe_name = Path(upload_file.filename or "uploaded_file").name
    staging_path = staging_dir / f"{uuid.uuid4()}-{safe_name}"

    with staging_path.open("wb") as output_file:
        shutil.copyfileobj(upload_file.file, output_file)

    return staging_path


def build_object_key(user_id, file_id, chunk_index: int) -> str:
    return f"users/{user_id}/files/{file_id}/chunks/{chunk_index:08d}.chunk"


@router.post("/upload", response_model=FileRead)
def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    user = get_or_create_dev_user(db)
    staging_path = save_to_staging(file)
    uploaded_object_keys: list[str] = []

    try:
        file_size = staging_path.stat().st_size

        if file_size == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Empty file is not allowed",
            )

        max_upload_bytes = settings.max_upload_mb * 1024 * 1024

        if file_size > max_upload_bytes:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File is larger than {settings.max_upload_mb} MB",
            )

        stored_file = StoredFile(
            user_id=user.id,
            original_filename=Path(file.filename or "uploaded_file").name,
            size_bytes=file_size,
            mime_type=file.content_type,
            status="uploading",
        )

        db.add(stored_file)
        db.flush()

        key = load_master_key()
        storage = B2Storage()
        chunk_size = settings.chunk_size_mb * 1024 * 1024

        for chunk_index, plaintext_chunk in iter_file_chunks(staging_path, chunk_size):
            encrypted = encrypt_chunk(plaintext_chunk, key)
            encrypted_hash = sha256_bytes(encrypted.ciphertext)

            object_key = build_object_key(
                user_id=user.id,
                file_id=stored_file.id,
                chunk_index=chunk_index,
            )

            storage.upload_bytes(
                object_key=object_key,
                data=encrypted.ciphertext,
            )

            uploaded_object_keys.append(object_key)

            chunk = Chunk(
                file_id=stored_file.id,
                chunk_index=chunk_index,
                object_key=object_key,
                encrypted_size=len(encrypted.ciphertext),
                sha256_encrypted=encrypted_hash,
                nonce=encrypted.nonce,
            )

            db.add(chunk)

        stored_file.status = "ready"

        db.commit()
        db.refresh(stored_file)

        return stored_file

    except HTTPException:
        db.rollback()

        storage = B2Storage()
        for object_key in uploaded_object_keys:
            try:
                storage.delete_object(object_key)
            except Exception:
                pass

        raise

    except Exception as error:
        db.rollback()

        storage = B2Storage()
        for object_key in uploaded_object_keys:
            try:
                storage.delete_object(object_key)
            except Exception:
                pass

        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {error}",
        ) from error

    finally:
        if staging_path.exists():
            staging_path.unlink()


@router.get("", response_model=list[FileRead])
def list_files(db: Session = Depends(get_db)):
    user = get_or_create_dev_user(db)

    files = (
        db.query(StoredFile)
        .filter(StoredFile.user_id == user.id)
        .filter(StoredFile.status != "deleted")
        .order_by(StoredFile.created_at.desc())
        .all()
    )

    return files