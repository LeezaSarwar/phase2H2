from sqlmodel import Field, SQLModel
from datetime import datetime
from typing import Optional


class User(SQLModel, table=True):
    """User model for authentication."""

    __tablename__ = "users"

    id: str = Field(primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    name: Optional[str] = Field(default=None)
    password_hash: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
