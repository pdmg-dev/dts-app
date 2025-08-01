# features/auth/schemas.py

from pydantic import BaseModel, StringConstraints, Field
from typing import Annotated
from datetime import datetime
from features.auth.models import Role

USERNAME_REGEX = r"^[a-zA-Z0-9_]{3,32}$"
PASSWORD_REGEX = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,64}$"


class UserCreate(BaseModel):
    """Schema for registering a new user."""

    username: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            to_lower=True,
            min_length=3,
            max_length=32,
            pattern=USERNAME_REGEX,
        ),
    ] = Field(description="3–32 chars: letters, digits, underscores only.")

    password_plain: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=8,
            max_length=64,
            pattern=PASSWORD_REGEX,
        ),
    ] = Field(
        description="8–64 chars, must include 1 letter, 1 digit, 1 special character."
    )

    model_config = {
        "title": "UserCreate",
        "json_schema_extra": {
            "example": {"username": "philip_dev", "password_plain": "DevPass@2025"}
        },
    }


class UserLogin(BaseModel):
    """Schema for user login (JWT)."""

    username: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True, to_lower=True, min_length=3, max_length=32
        ),
    ] = Field(description="Registered username.")

    password_plain: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1)
    ] = Field(description="User's password.")

    model_config = {
        "title": "UserLogin",
        "json_schema_extra": {
            "example": {"username": "philip_dev", "password_plain": "DevPass@2025"}
        },
    }


class UserRead(BaseModel):
    """Schema for returning user info (no password)."""

    id: int
    username: str
    role: Role
    is_active: bool
    created_at: datetime

    model_config = {
        "title": "UserRead",
        "from_attributes": True,  # ORM -> schema
        "json_schema_extra": {
            "example": {
                "id": 1,
                "username": "philip_dev",
                "role": "admin",
                "is_active": True,
                "created_at": "2025-07-31T15:30:00Z",
            }
        },
    }
