from fastapi import FastAPI

from app.api import health

app = FastAPI(title="ChunkVault")

app.include_router(health.router)


@app.get("/")
def root():
    return {
        "message": "ChunkVault API is running",
        "docs": "/docs",
        "health": "/health",
        "files":"/files",
    }