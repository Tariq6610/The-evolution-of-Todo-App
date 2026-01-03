# Backend: Create Endpoint

Creates a RESTful API endpoint using FastAPI with async/await patterns, error handling, and proper HTTP status codes.

## Usage

```
/sp.backend.create-endpoint <method> <path> [--description "<desc>"]
```

## Examples

```bash
# Create GET endpoint for listing tasks
/sp.backend.create-endpoint GET /api/v1/tasks "List all tasks with pagination"

# Create POST endpoint for creating tasks
/sp.backend.create-endpoint POST /api/v1/tasks "Create new task with validation"

# Create GET endpoint for single task
/sp.backend.create-endpoint GET /api/v1/tasks/{id} "Get specific task by ID"
```

## Endpoint Creation Rules

1. **File Location**: `apps/002-fullstack-web/backend/app/api/<resource>.py`
2. **Method Support**: GET, POST, PUT, PATCH, DELETE
3. **Response Model**: Use Pydantic models for request/response
4. **Dependency Injection**: Use FastAPI `Depends` for database session
5. **Error Handling**: Return proper HTTP status codes
6. **Async/Await**: All database operations use async/await
7. **Transaction Management**: Use context managers for multi-step operations
8. **Security**: Input validation, SQL injection prevention

## HTTP Method Best Practices

| Method | Usage | Response Code | Description |
|---------|-------|---------------|-------------|
| `GET` | Read operations | 200 OK, 404 Not Found | Retrieve resources |
| `POST` | Create operations | 201 Created, 400 Bad Request | Create new resource |
| `PUT` | Update operations | 200 OK, 404 Not Found | Replace entire resource |
| `PATCH` | Partial updates | 200 OK, 404 Not Found | Update resource |
| `DELETE` | Delete operations | 204 No Content, 404 Not Found | Delete resource |

## Example: GET Endpoint

```python
# app/api/tasks.py
from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from pydantic import BaseModel

from app.core.domain import Task, TaskStatus, TaskPriority
from app.db.session import get_session
from app.db.repositories import TaskRepository

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])

class TaskResponse(BaseModel):
    id: str
    title: str
    description: str | None = None
    status: TaskStatus
    priority: TaskPriority
    tags: list[str]
    created_at: datetime
    updated_at: datetime | None = None

@router.get("", response_model=List[TaskResponse])
async def list_tasks(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
):
    task_repo = TaskRepository(session)
    tasks = await task_repo.get_all(skip=skip, limit=limit)
    return tasks
```

## Example: POST Endpoint

```python
from fastapi import status

class TaskCreateRequest(BaseModel):
    title: str
    description: str | None = None
    priority: TaskPriority = TaskPriority.MEDIUM
    tags: list[str] = []

@router.post("", response_model=TaskResponse, status_code=201)
async def create_task(
    task_data: TaskCreateRequest,
    session: Session = Depends(get_session),
):
    task_repo = TaskRepository(session)

    domain_task = Task(
        title=task_data.title,
        description=task_data.description,
        status=TaskStatus.PENDING,
        priority=task_data.priority,
        tags=task_data.tags,
    )

    created_task = await task_repo.create(domain_task)
    return created_task
```

## Example: PUT Endpoint

```python
class TaskUpdateRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    tags: list[str] | None = None

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdateRequest,
    session: Session = Depends(get_session),
):
    task_repo = TaskRepository(session)

    existing_task = await task_repo.get_by_id(task_id)
    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )

    # Update only provided fields
    if task_update.title is not None:
        existing_task.title = task_update.title
    if task_update.description is not None:
        existing_task.description = task_update.description
    if task_update.status is not None:
        existing_task.status = task_update.status
    if task_update.priority is not None:
        existing_task.priority = task_update.priority
    if task_update.tags is not None:
        existing_task.tags = task_update.tags

    updated_task = await task_repo.update(task_id, existing_task)
    return updated_task
```

## Example: DELETE Endpoint

```python
from fastapi import status

@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: int,
    session: Session = Depends(get_session),
):
    task_repo = TaskRepository(session)

    success = await task_repo.delete(task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )

    return None  # No content for 204
```

## Error Handling Patterns

```python
# Not Found (404)
if not item:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{resource_type} not found"
    )

# Bad Request (400)
if invalid_input:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid input data"
    )

# Conflict (409)
if resource_exists:
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Resource already exists"
    )

# Internal Server Error (500)
except Exception as e:
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="An unexpected error occurred"
    )
```

## Query Parameters

```python
@router.get("", response_model=List[TaskResponse])
async def list_tasks(
    skip: int = 0,        # Pagination: offset
    limit: int = 100,      # Pagination: max items
    status: TaskStatus | None = None,  # Filter by status
    priority: TaskPriority | None = None, # Filter by priority
    search: str | None = None,  # Search by title
    session: Session = Depends(get_session),
):
    task_repo = TaskRepository(session)
    tasks = await task_repo.get_all(skip=skip, limit=limit)

    # Apply filters
    if status:
        tasks = [t for t in tasks if t.status == status]
    if priority:
        tasks = [t for t in tasks if t.priority == priority]
    if search:
        tasks = [t for t in tasks if search.lower() in t.title.lower()]

    return tasks
```

## Checklist

After creating endpoint, verify:
- [ ] HTTP method matches operation (GET for read, POST for create)
- [ ] Response model defined and documented
- [ ] Database session injected via Depends()
- [ ] All database operations use async/await
- [ ] Proper error handling with HTTP status codes
- [ ] SQL injection prevented (parameterized queries)
- [ ] Input validation with Pydantic
- [ ] Transactions used for multi-step operations
- [ ] Query parameters documented and validated
- [ ] Response includes all necessary data
- [ ] Follows RESTful conventions
- [ ] Has docstring describing endpoint
