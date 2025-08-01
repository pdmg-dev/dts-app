# main.py

"""
DTS App Main Application

This is the FastAPI entry point for the Document Tracking System (DTS).
It handles database initialization in development mode and provides the
root health-check endpoint.
"""

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from core.config import settings
from core.database import Base, engine
from core.logger import get_logger

logger = get_logger()
templates = Jinja2Templates(directory="templates")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context for FastAPI.

    Creates database tables in development mode at startup.
    Cleanup logic (e.g., closing connections) can be added here.
    """
    logger.info("Starting DTS App...")
    Base.metadata.create_all(bind=engine)
    yield
    logger.info("Shutting down DTS App...")


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    lifespan=lifespan,
)


@app.get("/", summary="Root health-check", tags=["Health"], response_class=HTMLResponse)
def read_root(request: Request):
    """Render the DTS App landing page."""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "app_name": settings.app_name,
            "version": settings.version,
            "status": "running",
            "message": "Welcome to the DTS API!",
        },
    )
