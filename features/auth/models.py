from sqlalchemy import Integer, String, DateTime, Boolean, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from enum import Enum
from core.database import Base


class Role(str, Enum):
    """User role for authorization and access control."""

    ADMIN = "admin"
    STAFF = "staff"


class User(Base):
    """User table for authentication and roles."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(
        String(32), unique=True, nullable=False, index=True
    )
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    role: Mapped[Role] = mapped_column(
        SqlEnum(Role), default=Role.STAFF, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default_factory=lambda: datetime.now(timezone.utc)
    )
