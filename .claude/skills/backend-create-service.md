# Backend: Create Service

Creates a business service layer with use cases, clean architecture, and proper dependency injection using FastAPI and SQLModel.

## Usage

```
/sp.backend.create-service <ServiceName> [--methods "<method1>,<method2>"]
```

## Examples

```bash
# Create TaskService with CRUD operations
/sp.backend.create-service TaskService --methods "create,get_by_id,get_all,update,delete"

# Create AuthService
/sp.backend.create-service AuthService --methods "register,login,logout,verify_token"
```

## Service Creation Rules

1. **File Location**: `apps/002-fullstack-web/backend/app/core/services.py`
2. **Business Logic Only**: No database operations, no API responses
3. **Domain Entities**: Work with domain models, not database models
4. **Repository Injection**: Inject repository via FastAPI Depends
5. **Async Methods**: All methods use async/await
6. **Error Handling**: Custom exceptions, consistent error messages
7. **Validation**: Input validation before business logic
8. **Logging**: Structured logging for debugging

## Service Structure

```python
# app/core/services.py
from typing import List, Optional
from fastapi import Depends

from app.core.domain import Task, TaskStatus, TaskPriority
from app.db.repositories import TaskRepository
from app.db.session import get_session

class TaskService:
    def __init__(self, task_repo: TaskRepository):
        self.task_repo = task_repo
        self.logger = logging.getLogger(__name__)

    async def create(self, task: Task) -> Task:
        # Business rules
        if not task.title or len(task.title) < 3:
            raise ValueError("Title must be at least 3 characters")

        if len(task.title) > 200:
            raise ValueError("Title must be at most 200 characters")

        # Delegate to repository
        return await self.task_repo.create(task)

    async def get_by_id(self, task_id: int) -> Optional[Task]:
        task = await self.task_repo.get_by_id(task_id)

        # Business rule: Archived tasks are hidden
        if task and task.status == TaskStatus.ARCHIVED:
            raise PermissionError("Task is archived")

        return task

    async def get_all_by_user(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Task]:
        return await self.task_repo.get_all_by_user(user_id, skip=skip, limit=limit)

    async def update_status(self, task_id: int, status: TaskStatus) -> Optional[Task]:
        task = await self.task_repo.get_by_id(task_id)

        if not task:
            raise ValueError("Task not found")

        # Business rule: Can't archive completed tasks
        if status == TaskStatus.ARCHIVED and task.status != TaskStatus.COMPLETED:
            raise ValueError("Cannot archive incomplete task")

        return await self.task_repo.update(task_id, task)

    async def delete(self, task_id: int, user_id: int) -> bool:
        task = await self.task_repo.get_by_id(task_id)

        if not task:
            raise ValueError("Task not found")

        # Business rule: Can't delete other users' tasks
        if task.user_id != user_id:
            raise PermissionError("You can only delete your own tasks")

        return await self.task_repo.delete(task_id)
```

## Common Service Methods

### CRUD Operations

```python
async def create(self, entity: DomainEntity) -> DomainEntity:
    """Create new entity with validation"""
    # Business rules
    # Delegate to repository

async def read(self, entity_id: int) -> Optional[DomainEntity]:
    """Get entity by ID with business rules"""
    # Business rules (permissions, filtering)
    # Delegate to repository

async def update(self, entity_id: int, updates: dict) -> Optional[DomainEntity]:
    """Update entity with validation"""
    # Business rules
    # Delegate to repository

async def delete(self, entity_id: int) -> bool:
    """Delete entity with business rules"""
    # Business rules (permissions, cascades)
    # Delegate to repository
```

### Business Logic

```python
async def calculate_task_score(self, task: Task) -> int:
    """Calculate priority score based on business rules"""
    score = 0

    # Priority scoring
    if task.priority == TaskPriority.HIGH:
        score += 50
    elif task.priority == TaskPriority.MEDIUM:
        score += 30
    elif task.priority == TaskPriority.LOW:
        score += 10

    # Due date urgency
    if task.due_date:
        days_until = (task.due_date - datetime.now()).days
        if days_until <= 1:
            score += 30
        elif days_until <= 3:
            score += 15

    return score

async def filter_archived(self, tasks: List[Task]) -> List[Task]:
    """Exclude archived tasks from results"""
    return [t for t in tasks if t.status != TaskStatus.ARCHIVED]
```

### Custom Exceptions

```python
class TaskServiceError(Exception):
    """Base exception for task service"""
    pass

class TaskNotFound(TaskServiceError):
    """Raised when task doesn't exist"""
    def __init__(self, task_id: int):
        super().__init__(f"Task {task_id} not found")

class InvalidTaskState(TaskServiceError):
    """Raised when invalid task state transition"""
    def __init__(self, current_state: str, new_state: str):
        super().__init__(f"Cannot transition from {current_state} to {new_state}")

class PermissionDenied(TaskServiceError):
    """Raised when user lacks permission"""
    def __init__(self, action: str):
        super().__init__(f"Permission denied: {action}")
```

## Dependency Injection

```python
# FastAPI dependency injection
from fastapi import Depends

from app.db.session import get_session
from app.db.repositories import TaskRepository

class TaskService:
    def __init__(self, task_repo: TaskRepository):
        self.task_repo = task_repo

# In API endpoints
@router.get("/{task_id}")
async def get_task(
    task_id: int,
    service: TaskService = Depends(TaskService),
):
    # FastAPI injects TaskService with TaskRepository
    return await service.get_by_id(task_id)

# Alternative: Manual dependency injection
from fastapi import Depends, Request

def get_current_user(request: Request) -> User:
    token = request.headers.get("Authorization")
    # Validate and decode token
    return user

@router.get("/tasks")
async def get_tasks(
    service: TaskService = Depends(TaskService),
    current_user: User = Depends(get_current_user),
):
    return await service.get_all_by_user(current_user.id)
```

## Logging

```python
import logging

class TaskService:
    def __init__(self, task_repo: TaskRepository):
        self.task_repo = task_repo
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())

    async def create(self, task: Task) -> Task:
        self.logger.info(f"Creating task: {task.title}")
        try:
            result = await self.task_repo.create(task)
            self.logger.info(f"Task created with ID: {result.id}")
            return result
        except Exception as e:
            self.logger.error(f"Failed to create task: {e}")
            raise TaskServiceError(f"Failed to create task: {e}")
```

## Use Cases

```python
# Use case 1: Create task with business rules
service.create(Task(title="Buy groceries", priority=TaskPriority.HIGH))
# Validates title length, delegates to repository

# Use case 2: Get tasks for specific user
service.get_all_by_user(user_id=123, skip=0, limit=50)
# Filters by user ID, applies business rules

# Use case 3: Update with state transition
service.update_status(task_id=1, status=TaskStatus.COMPLETED)
# Validates state transition, updates task
```

## Checklist

After creating service, verify:
- [ ] Contains only business logic
- [ ] No database operations or SQLModel usage
- [ ] Works with domain entities
- [ ] Repository injected via Depends
- [ ] All methods use async/await
- [ ] Custom exceptions defined
- [ ] Input validation before business rules
- [ ] Business rules documented in docstrings
- [ ] Proper error handling
- [ ] Logging configured
- [ ] No API-related code (responses, status codes)
- [ ] Clean separation of concerns
