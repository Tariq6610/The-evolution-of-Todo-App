from datetime import UTC, datetime
from uuid import uuid4

from pydantic import EmailStr, field_validator
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    """Base User model with shared fields."""

    email: EmailStr = Field(index=True, unique=True, nullable=False)
    full_name: str | None = None
    is_active: bool = Field(default=True)


class User(UserBase, table=True):
    """User entity and database table."""

    __tablename__ = "users"

    id: str | None = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
        index=True,
        nullable=False,
    )
    hashed_password: str = Field(nullable=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False,
    )


class UserCreate(UserBase):
    """Schema for creating a new user."""

    password: str

    @field_validator("password")
    @classmethod
    def validate_password_length(cls, v: str) -> str:
        """Validate password length for bcrypt compatibility (max 72 bytes)."""
        if len(v.encode("utf-8")) > 72:
            # Truncate to 72 bytes and decode back to string
            truncated_bytes = v.encode("utf-8")[:72]
            v = truncated_bytes.decode("utf-8", errors="ignore")
        return v


class UserRead(UserBase):
    """Schema for reading user data."""

    id: str
    created_at: datetime
    updated_at: datetime


class UserUpdate(SQLModel):
    """Schema for updating user data."""

    email: EmailStr | None = None
    full_name: str | None = None
    password: str | None = None
    is_active: bool | None = None

    @field_validator("password", mode="before")
    @classmethod
    def validate_update_password_length(cls, v: str | None) -> str | None:
        """Validate update password length for bcrypt compatibility (max 72 bytes)."""
        if v is None:
            return v
        if len(v.encode("utf-8")) > 72:
            # Truncate to 72 bytes and decode back to string
            truncated_bytes = v.encode("utf-8")[:72]
            v = truncated_bytes.decode("utf-8", errors="ignore")
        return v
