from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from datetime import datetime, timezone

from app.database import get_session
from app.models import Task
from app.schemas import (
    TaskCreate,
    TaskUpdate,
    TaskComplete,
    TaskResponse,
    TaskListResponse,
)
from app.middleware.auth import get_current_user, verify_user_access

router = APIRouter(prefix="/api/{user_id}/tasks", tags=["Tasks"])


@router.get("", response_model=TaskListResponse)
async def list_tasks(
    user_id: str,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """List all tasks for a user."""
    verify_user_access(current_user.get("sub"), user_id)

    statement = (
        select(Task)
        .where(Task.user_id == user_id)
        .order_by(Task.created_at.desc())
    )
    result = await session.execute(statement)
    tasks = result.scalars().all()

    return TaskListResponse(tasks=[TaskResponse.model_validate(t) for t in tasks])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: str,
    data: TaskCreate,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """Create a new task."""
    verify_user_access(current_user.get("sub"), user_id)

    task = Task(
        user_id=user_id,
        title=data.title.strip(),
        description=data.description.strip() if data.description else None,
        category=data.category,
        priority=data.priority,
        due_date=data.due_date,
    )

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return TaskResponse.model_validate(task)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: str,
    task_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """Get a single task by ID."""
    verify_user_access(current_user.get("sub"), user_id)

    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.execute(statement)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return TaskResponse.model_validate(task)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: str,
    task_id: int,
    data: TaskUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """Update a task."""
    verify_user_access(current_user.get("sub"), user_id)

    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.execute(statement)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    task.title = data.title.strip()
    task.description = data.description.strip() if data.description else None
    task.category = data.category
    task.priority = data.priority
    task.due_date = data.due_date
    task.updated_at = datetime.now(timezone.utc)

    await session.commit()
    await session.refresh(task)

    return TaskResponse.model_validate(task)


@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def toggle_complete(
    user_id: str,
    task_id: int,
    data: TaskComplete,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """Toggle task completion status."""
    verify_user_access(current_user.get("sub"), user_id)

    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.execute(statement)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    task.completed = data.completed
    task.updated_at = datetime.now(timezone.utc)

    await session.commit()
    await session.refresh(task)

    return TaskResponse.model_validate(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user_id: str,
    task_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """Delete a task."""
    verify_user_access(current_user.get("sub"), user_id)

    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.execute(statement)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    await session.delete(task)
    await session.commit()
