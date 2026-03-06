from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from sqlmodel import Session

from chatbot_backend.adapters.db.session import get_session
from chatbot_backend.adapters.db.task_repository import SQLModelTaskRepository
from chatbot_backend.adapters.security.jwt import get_current_user
from chatbot_backend.domain.entities.priority import Priority
from chatbot_backend.domain.entities.task import Task as DomainTask
from chatbot_backend.domain.entities.user import User
from chatbot_backend.domain.services.todo_service import TodoService

router = APIRouter(tags=["Tasks"])


# Request/Response models
class TaskCreateRequest(BaseModel):
    title: str
    description: str | None = None
    priority: str = "MEDIUM"  # LOW, MEDIUM, HIGH
    tags: list[str] = []


class TaskUpdateRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: str | None = None  # LOW, MEDIUM, HIGH
    tags: list[str] | None = None


class TaskResponse(BaseModel):
    id: str
    title: str
    description: str | None
    status: str  # PENDING, COMPLETED
    priority: str  # LOW, MEDIUM, HIGH
    tags: list[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Dependency to get todo service with session
def get_todo_service(session: Session = Depends(get_session)) -> TodoService:
    task_repo = SQLModelTaskRepository(session)
    return TodoService(task_repo)


@router.post("", response_model=TaskResponse)
def create_task(
    request: Request,
    task_in: TaskCreateRequest,
    current_user: User = Depends(get_current_user),
    todo_service: TodoService = Depends(get_todo_service),
) -> DomainTask:
    try:
        try:
            priority_enum = Priority(task_in.priority.lower())
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Invalid priority value: {task_in.priority}. Must be one of: low, medium, high"
                ),
            ) from e

        if current_user.id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User ID not found"
            )
        task = todo_service.create_task_for_user(
            title=task_in.title,
            user_id=current_user.id,
            description=task_in.description,
            priority=priority_enum,
            tags=task_in.tags,
        )
        return task
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@router.get("", response_model=list[TaskResponse])
def get_all_tasks(
    request: Request,
    search: str | None = None,
    status_param: str | None = None,
    priority: str | None = None,
    tag: str | None = None,
    sort_by: str | None = None,
    current_user: User = Depends(get_current_user),
    todo_service: TodoService = Depends(get_todo_service),
) -> list[DomainTask]:
    try:
        # Normalize parameters to lowercase for case-insensitive matching
        normalized_status = status_param.lower() if status_param else None
        normalized_priority_param = priority.lower() if priority else None

        if current_user.id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User ID not found"
            )
        tasks = todo_service.get_all_tasks_for_user(
            user_id=current_user.id,
            search=search,
            status=normalized_status,
            priority=normalized_priority_param,
            tag=tag,
            sort_by=sort_by,
        )
        return tasks
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    request: Request,
    task_id: str,
    current_user: User = Depends(get_current_user),
    todo_service: TodoService = Depends(get_todo_service),
) -> DomainTask:
    try:
        if current_user.id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User ID not found"
            )
        # Check if the task exists and belongs to the user
        if not todo_service.storage.exists_for_user(task_id, current_user.id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

        task = todo_service.storage.get(task_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        return task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    request: Request,
    task_id: str,
    task_in: TaskUpdateRequest,
    current_user: User = Depends(get_current_user),
    todo_service: TodoService = Depends(get_todo_service),
) -> DomainTask:
    try:
        priority_enum = None
        if task_in.priority:
            try:
                priority_enum = Priority(task_in.priority.lower())
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        f"Invalid priority value: {task_in.priority}. "
                        "Must be one of: low, medium, high"
                    ),
                ) from e

        if current_user.id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User ID not found"
            )
        task = todo_service.update_task_for_user(
            task_id=task_id,
            user_id=current_user.id,
            title=task_in.title,
            description=task_in.description,
            priority=priority_enum,
            tags=task_in.tags,
        )
        return task
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@router.delete("/{task_id}")
def delete_task(
    request: Request,
    task_id: str,
    current_user: User = Depends(get_current_user),
    todo_service: TodoService = Depends(get_todo_service),
) -> dict[str, str]:
    try:
        if current_user.id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User ID not found"
            )
        todo_service.delete_task_for_user(task_id, current_user.id)
        return {"message": "Task deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@router.patch("/{task_id}/toggle-status", response_model=TaskResponse)
def toggle_task_status(
    request: Request,
    task_id: str,
    current_user: User = Depends(get_current_user),
    todo_service: TodoService = Depends(get_todo_service),
) -> DomainTask:
    try:
        if current_user.id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User ID not found"
            )
        task = todo_service.toggle_task_status_for_user(task_id, current_user.id)
        return task
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
