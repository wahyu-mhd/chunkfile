from fastapi import FastAPI

from app.api import auth, files, health

app = FastAPI(title="ChunkVault")

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(files.router)


@app.get("/")
def root():
    return {
        "message": "ChunkVault API is running",
        "docs": "/docs",
        "health": "/health",
        "auth": "/auth",
        "files": "/files",
    }