from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.api import audit, auth, files, health
from app.config import get_settings


settings = get_settings()
app = FastAPI(title=settings.app_title)
app.include_router(auth.router)
app.include_router(files.router)
app.include_router(audit.router)
app.include_router(health.router)


@app.get("/", include_in_schema=False)
async def root():
    ...
