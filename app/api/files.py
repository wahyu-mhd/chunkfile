import shutil
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask

from sqlalchemy.orm import Session

from app.config import settings
from app.core.chunker import iter_file_chunks
from app.core.crypto import encrypt_chunk, load_master_key, decrypt_chunk
from app.core.hasher import sha256_bytes
from app.core.storage_b2 import B2Storage
from app.database import get_db
from app.models import Chunk, StoredFile, User, AuditLog
from app.schemas import FileRead

router = APIRouter(prefix="/files", tags=["files"])

def add_audit_log(
    db: Session,
    action: str,
    user_id=None,
    file_id=None,
    message: str | None = None,
):
    log = AuditLog(
        user_id=user_id,
        file_id=file_id,
        action=action,
        message=message,
    )

    db.add(log)

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

def cleanup_temp_file(path: Path) -> None:
    try:
        if path.exists():
            path.unlink()
    except Exception:
        pass

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
        add_audit_log(
            db=db,
            action="file_uploaded",
            user_id=user.id,
            file_id=stored_file.id,
            message=f"Uploaded {stored_file.original_filename}",
        )

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


# @router.get("", response_model=list[FileRead])
# def list_files(db: Session = Depends(get_db)):
#     user = get_or_create_dev_user(db)

#     files = (
#         db.query(StoredFile)
#         .filter(StoredFile.user_id == user.id)
#         .filter(StoredFile.status != "deleted")
#         .order_by(StoredFile.created_at.desc())
#         .all()
#     )

#     return files

@router.get("/{file_id}/download")
def download_file(
    file_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    user = get_or_create_dev_user(db)

    stored_file = (
        db.query(StoredFile)
        .filter(StoredFile.id == file_id)
        .filter(StoredFile.user_id == user.id)
        .filter(StoredFile.status == "ready")
        .first()
    )

    if stored_file is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )

    chunks = (
        db.query(Chunk)
        .filter(Chunk.file_id == stored_file.id)
        .order_by(Chunk.chunk_index.asc())
        .all()
    )

    if not chunks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No chunks found for this file",
        )

    temp_dir = Path("data/temp_restore")
    temp_dir.mkdir(parents=True, exist_ok=True)

    safe_name = Path(stored_file.original_filename).name
    output_path = temp_dir / f"{uuid.uuid4()}-{safe_name}"

    key = load_master_key()
    storage = B2Storage()

    try:
        with output_path.open("wb") as output_file:
            for chunk in chunks:
                encrypted_bytes = storage.download_bytes(chunk.object_key)

                current_hash = sha256_bytes(encrypted_bytes)

                if current_hash != chunk.sha256_encrypted:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=(
                            "Chunk integrity check failed "
                            f"at chunk index {chunk.chunk_index}"
                        ),
                    )

                plaintext_bytes = decrypt_chunk(
                    ciphertext=encrypted_bytes,
                    nonce=chunk.nonce,
                    key=key,
                )

                output_file.write(plaintext_bytes)
        
        add_audit_log(
            db=db,
            action="file_downloaded",
            user_id=user.id,
            file_id=stored_file.id,
            message=f"Downloaded {stored_file.original_filename}",
        )

        db.commit()
        return FileResponse(
            path=output_path,
            filename=stored_file.original_filename,
            media_type=stored_file.mime_type or "application/octet-stream",
            background=BackgroundTask(cleanup_temp_file, output_path),
        )

    except HTTPException:
        cleanup_temp_file(output_path)
        raise

    except Exception as error:
        cleanup_temp_file(output_path)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Download failed: {error}",
        ) from error
    
@router.delete("/{file_id}")
def delete_file(
    file_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    user = get_or_create_dev_user(db)

    stored_file = (
        db.query(StoredFile)
        .filter(StoredFile.id == file_id)
        .filter(StoredFile.user_id == user.id)
        .filter(StoredFile.status != "deleted")
        .first()
    )

    if stored_file is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )

    chunks = (
        db.query(Chunk)
        .filter(Chunk.file_id == stored_file.id)
        .order_by(Chunk.chunk_index.asc())
        .all()
    )

    storage = B2Storage()

    try:
        for chunk in chunks:
            storage.delete_object(chunk.object_key)

        stored_file.status = "deleted"

        add_audit_log(
            db=db,
            action="file_deleted",
            user_id=user.id,
            file_id=stored_file.id,
            message=f"Deleted {stored_file.original_filename}",
        )

        db.commit()

        return {
            "status": "deleted",
            "file_id": stored_file.id,
            "filename": stored_file.original_filename,
            "chunks_deleted": len(chunks),
        }

    except Exception as error:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Delete failed: {error}",
        ) from error
    

@router.get("/audit/recent")
def recent_audit_logs(db: Session = Depends(get_db)):
    user = get_or_create_dev_user(db)

    logs = (
        db.query(AuditLog)
        .filter(AuditLog.user_id == user.id)
        .order_by(AuditLog.created_at.desc())
        .limit(20)
        .all()
    )

    return [
        {
            "id": log.id,
            "action": log.action,
            "file_id": log.file_id,
            "message": log.message,
            "created_at": log.created_at,
        }
        for log in logs
    ]