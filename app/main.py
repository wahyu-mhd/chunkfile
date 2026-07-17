from fastapi import FastAPI

from app.api import health
from app.api import files

app = FastAPI(title="ChunkVault")

app.include_router(health.router)
app.include_router(files.router)


@app.get("/")
def root():
    return {
        "message": "ChunkVault API is running",
        "docs": "/docs",
        "health": "/health",
        "files":"/files",
    }