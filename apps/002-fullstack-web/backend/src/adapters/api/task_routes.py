from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from src.domain.entities.task import Task as DomainTask
from src.domain.services.todo_service import TodoService
from src.adapters.db.task_repository import SQLModelTaskRepository
from src.adapters.db.session import get_session
from sqlmodel import Session
from pydantic import BaseModel

router = APIRouter(tags=["Tasks"])

# Request/Response models
class TaskCreateRequest(BaseModel):
    title: str
    description: str | None = None
    priority: str = "MEDIUM"  # LOW, MEDIUM, HIGH
    tags: List[str] = []

class TaskUpdateRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: str | None = None  # LOW, MEDIUM, HIGH
    tags: List[str] | None = None

from datetime import datetime
class TaskResponse(BaseModel):
    id: str
    title: str
    description: str | None
    status: str  # PENDING, COMPLETED
    priority: str  # LOW, MEDIUM, HIGH
    tags: List[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Dependency to get todo service
def get_todo_service(session: Session = Depends(get_session)) -> TodoService:
    task_repo = SQLModelTaskRepository(session)
    return TodoService(task_repo)

@router.post("/", response_model=TaskResponse)
def create_task(task_in: TaskCreateRequest, todo_service: TodoService = Depends(get_todo_service)):
    try:
        task = todo_service.create_task(
            title=task_in.title,
            description=task_in.description,
            priority=task_in.priority.lower(),  # Convert to lowercase to match enum
            tags=task_in.tags
        )
        return task
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[TaskResponse])
def get_all_tasks(
    search: str | None = None,
    status: str | None = None,
    priority: str | None = None,
    tag: str | None = None,
    sort_by: str | None = None,
    todo_service: TodoService = Depends(get_todo_service),
):
    try:
        tasks = todo_service.get_all_tasks(
            search=search,
            status=status,
            priority=priority,
            tag=tag,
            sort_by=sort_by,
        )
        return tasks
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: str, todo_service: TodoService = Depends(get_todo_service)):
    try:
        task = todo_service.storage.get(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        return task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: str, task_in: TaskUpdateRequest, todo_service: TodoService = Depends(get_todo_service)):
    try:
        task = todo_service.update_task(
            task_id=task_id,
            title=task_in.title,
            description=task_in.description,
            priority=task_in.priority.lower() if task_in.priority else None,
            tags=task_in.tags
        )
        return task
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{task_id}")
def delete_task(task_id: str, todo_service: TodoService = Depends(get_todo_service)):
    try:
        todo_service.delete_task(task_id)
        return {"message": "Task deleted successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.patch("/{task_id}/toggle-status", response_model=TaskResponse)
def toggle_task_status(task_id: str, todo_service: TodoService = Depends(get_todo_service)):
    try:
        task = todo_service.toggle_task_status(task_id)
        return task
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )