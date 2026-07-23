from fastapi import FastAPI

from app.api import auth, files, health
from app.config import settings

# app = FastAPI(title="ChunkVault")

app = FastAPI(
    title="ChunkVault",
    docs_url=None if settings.app_env == "production" else "/docs",
    redoc_url=None if settings.app_env == "production" else "/redoc",
    openapi_url=None if settings.app_env == "production" else "/openapi.json",
)


@app.get("/")
def root():
    response = {
        "message": "ChunkVault API is running",
        "health": "/health",
        "auth": "/auth/login-page",
        "files": "/files",
    }

    if settings.app_env != "production":
        response["docs"] = "/docs"

    return response