import sqlite3

from fastapi import APIRouter, Depends

from app.api.auth import get_current_user
from app.database import get_db
from app.schemas import AuditLogRecord


router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("", response_model=list[AuditLogRecord])
async def audit_logs(
    current_user: sqlite3.Row = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    ...
