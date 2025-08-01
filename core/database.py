# core/database.py

"""
Database configuration module for DTS App.

This module initializes the SQLAlchemy engine, session factory,
and provides the declarative Base for ORM models. It also exposes
a FastAPI dependency to access a database session in routes.
"""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from core.config import settings


class Base(DeclarativeBase):
    """Base class for all ORM models in the DTS app."""

    pass


# Configure connection arguments for SQLite in development
connect_args = {"check_same_thread": False} if "sqlite" in settings.db_url else {}

# SQLAlchemy engine for synchronous database operations
engine = create_engine(settings.db_url, connect_args=connect_args)

# Session factory for creating database sessions
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a database session.

    Yields:
        Session: SQLAlchemy session object for database operations.

    Usage:
        @app.get("/items/")
        def read_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    with SessionLocal() as db:
        yield db
