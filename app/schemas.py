# from pydantic import BaseModel


# class AuthToken(BaseModel):
#     access_token: str
#     token_type: str = "bearer"
#     user_id: int
#     username: str


# class FileRecord(BaseModel):
#     id: int
#     original_filename: str
#     size_bytes: int
#     mime_type: str | None
#     status: str
#     created_at: str
#     updated_at: str


# class AuditLogRecord(BaseModel):
#     id: int
#     action: str
#     file_id: int | None
#     ip_address: str | None
#     message: str
#     created_at: str
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class FileRead(BaseModel):
    id: UUID
    original_filename: str
    size_bytes: int
    mime_type: str | None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)