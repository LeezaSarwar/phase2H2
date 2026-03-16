from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TaskCreate(BaseModel):
    """Request schema for creating a task."""

    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    category: str = Field(default="Personal", max_length=50)
    priority: str = Field(default="Medium", max_length=20)
    due_date: Optional[datetime] = None


class TaskUpdate(BaseModel):
    """Request schema for updating a task."""

    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    category: str = Field(..., max_length=50)
    priority: str = Field(..., max_length=20)
    due_date: Optional[datetime] = None


class TaskComplete(BaseModel):
    """Request schema for toggling task completion."""

    completed: bool


class TaskResponse(BaseModel):
    """Response schema for a single task."""

    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    category: str
    priority: str
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """Response schema for a list of tasks."""

    tasks: list[TaskResponse]
