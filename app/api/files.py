import sqlite3

from fastapi import APIRouter, Depends, File, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.api.auth import get_current_user
from app.database import get_db
from app.schemas import FileRecord


router = APIRouter(tags=["files"])
templates = Jinja2Templates(directory="app/templates")


def _client_ip(request: Request) -> str | None:
    ...


def _row_to_file(row: sqlite3.Row) -> FileRecord:
    ...


@router.get("/dashboard", response_class=HTMLResponse, include_in_schema=False)
async def dashboard(
    request: Request,
    db: sqlite3.Connection = Depends(get_db),
):
    ...


@router.get("/ui/files", response_class=HTMLResponse, include_in_schema=False)
async def files_page(
    request: Request,
    current_user: sqlite3.Row = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    ...


@router.post("/files/upload", response_model=FileRecord)
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    current_user: sqlite3.Row = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    ...


@router.get("/files", response_model=list[FileRecord])
async def list_files(
    current_user: sqlite3.Row = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    ...


@router.get("/files/{file_id}/download")
async def download_file(
    file_id: int,
    request: Request,
    current_user: sqlite3.Row = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    ...


@router.delete("/files/{file_id}")
async def delete_file(
    file_id: int,
    request: Request,
    current_user: sqlite3.Row = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    ...
