"""
DTS App Main Application

This is the FastAPI entry point for the Document Tracking System (DTS).
It handles database initialization in development mode and provides the
root health-check endpoint.
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.database import Base, engine
from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context for FastAPI.
    
    Creates database tables in development mode at startup.
    Cleanup logic (e.g., closing connections) can be added here.
    """
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    lifespan=lifespan,
)


@app.get("/", summary="Root health-check", tags=["Health"])
def read_root():
    """
    Root endpoint for DTS API.

    Returns:
        dict: Application metadata and health status.
    """
    return {
        "app_name": settings.app_name,
        "version": settings.version,
        "status": "running",
        "message": "Welcome to the DTS API!"
    }
