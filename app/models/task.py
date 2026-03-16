from sqlmodel import Field, SQLModel
from sqlalchemy import Column, DateTime
from datetime import datetime, timezone
from typing import Optional


def utcnow():
    """Return timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


class Task(SQLModel, table=True):
    """Task model representing a todo item."""

    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, nullable=False)
    title: str = Field(max_length=200, nullable=False)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    category: str = Field(default="Personal", max_length=50, nullable=False, index=True)
    priority: str = Field(default="Medium", max_length=20, nullable=False, index=True)
    due_date: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True)
    )
    created_at: datetime = Field(
        default_factory=utcnow,
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    updated_at: datetime = Field(
        default_factory=utcnow,
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
