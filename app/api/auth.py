import sqlite3

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.database import get_db
from app.schemas import AuthToken


router = APIRouter(prefix="/auth", tags=["auth"])
templates = Jinja2Templates(directory="app/templates")
SESSION_COOKIE = "chunkvault_session"


async def _credentials_from_request(request: Request) -> tuple[str, str]:
    ...


def _client_ip(request: Request) -> str | None:
    ...


def _set_session_cookie(response: Response, token: str) -> None:
    ...


@router.get("/login", response_class=HTMLResponse, include_in_schema=False)
async def login_page(request: Request):
    ...


@router.post("/register", response_model=AuthToken)
async def register(
    request: Request,
    response: Response,
    db: sqlite3.Connection = Depends(get_db),
):
    ...


@router.post("/login", response_model=AuthToken)
async def login(
    request: Request,
    response: Response,
    db: sqlite3.Connection = Depends(get_db),
):
    ...


async def get_current_user(
    request: Request,
    db: sqlite3.Connection = Depends(get_db),
) -> sqlite3.Row:
    ...
