# Backend: Create Repository

Creates a repository pattern for database operations using SQLModel with async/await, transactions, and clean separation of concerns.

## Usage

```
/sp.backend.create-repository <ModelName> [--description "<desc>"]
```

## Examples

```bash
# Create Task repository
/sp.backend.create-repository Task --description "Task CRUD operations with async patterns"

# Create User repository
/sp.backend.create-repository User --description "User authentication operations"
```

## Repository Creation Rules

1. **File Location**: `apps/002-fullstack-web/backend/app/db/repositories.py`
2. **Session Injection**: Constructor accepts SQLModel Session
3. **Async Methods**: All operations use async/await
4. **Transaction Management**: Use context managers for multi-step operations
5. **Error Handling**: Return None for not found, raise for database errors
6. **Domain Models**: Return domain entities, not database models
7. **Clean Methods**: Don't expose raw SQL, use SQLAlchemy only

## Standard CRUD Operations

### Create

```python
async def create(self, entity: DomainEntity) -> DomainEntity:
    db_entity = EntityModel.from_entity(entity)
    self.session.add(db_entity)
    await self.session.commit()
    await self.session.refresh(db_entity)
    return entity.from_model(db_entity)
```

### Read (Get by ID)

```python
async def get_by_id(self, entity_id: int) -> Optional[DomainEntity]:
    statement = select(EntityModel).where(EntityModel.id == entity_id)
    result = await self.session.exec(statement)
    db_entity = result.one_or_none()

    if not db_entity:
        return None

    return entity.from_model(db_entity)
```

### Read (Get All)

```python
async def get_all(self, skip: int = 0, limit: int = 100) -> List[DomainEntity]:
    statement = select(EntityModel).offset(skip).limit(limit)
    result = await self.session.exec(statement)
    db_entities = result.all()

    return [entity.from_model(e) for e in db_entities]
```

### Update

```python
async def update(self, entity_id: int, entity: DomainEntity) -> Optional[DomainEntity]:
    db_entity = await self.get_by_id(entity_id)

    if not db_entity:
        return None

    # Update fields
    for field, value in entity.dict(exclude_unset=True).items():
        setattr(db_entity, field, value)

    db_entity.updated_at = datetime.utcnow()
    self.session.add(db_entity)
    await self.session.commit()
    await self.session.refresh(db_entity)

    return entity.from_model(db_entity)
```

### Delete

```python
async def delete(self, entity_id: int) -> bool:
    db_entity = await self.get_by_id(entity_id)

    if not db_entity:
        return False

    await self.session.delete(db_entity)
    await self.session.commit()

    return True
```

## Complete Example: Task Repository

```python
# app/db/repositories.py
from typing import List, Optional
from datetime import datetime
from sqlmodel import Session, select

from app.db.models import TaskModel
from app.core.domain import Task, TaskStatus, TaskPriority

class TaskRepository:
    def __init__(self, session: Session):
        self.session = session

    async def create(self, task: Task) -> Task:
        db_task = TaskModel(
            title=task.title,
            description=task.description,
            status=task.status.value,
            priority=task.priority.value,
            tags=task.tags,
            created_at=task.created_at,
        )

        self.session.add(db_task)
        await self.session.commit()
        await self.session.refresh(db_task)

        return Task.from_model(db_task)

    async def get_by_id(self, task_id: int) -> Optional[Task]:
        statement = select(TaskModel).where(TaskModel.id == task_id)
        result = await self.session.exec(statement)
        db_task = result.one_or_none()

        if not db_task:
            return None

        return Task.from_model(db_task)

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Task]:
        statement = select(TaskModel).offset(skip).limit(limit)
        result = await self.session.exec(statement)
        db_tasks = result.all()

        return [Task.from_model(t) for t in db_tasks]

    async def update(self, task_id: int, task: Task) -> Optional[Task]:
        db_task = await self.get_by_id(task_id)

        if not db_task:
            return None

        db_task.title = task.title
        db_task.description = task.description
        db_task.status = task.status.value
        db_task.priority = task.priority.value
        db_task.tags = task.tags
        db_task.updated_at = datetime.utcnow()

        self.session.add(db_task)
        await self.session.commit()
        await self.session.refresh(db_task)

        return Task.from_model(db_task)

    async def delete(self, task_id: int) -> bool:
        db_task = await self.get_by_id(task_id)

        if not db_task:
            return False

        await self.session.delete(db_task)
        await self.session.commit()

        return True
```

## Transaction Management

### Multiple Operations

```python
async def transfer_tasks(self, from_id: int, to_id: int) -> bool:
    try:
        async with get_async_session() as session:
            task_repo = TaskRepository(session)

            # Get tasks
            from_task = await task_repo.get_by_id(from_id)
            to_user_id = await task_repo.get_by_id(to_id)

            if not from_task or not to_user_id:
                return False

            # Transfer ownership
            task_repo = TaskRepository(session)
            task_repo.tasks = await task_repo.get_all_by_user(to_user_id)

            return True

    except Exception as e:
        # Session automatically rolled back
        return False
```

## Domain Model Conversion

### From Model to Domain

```python
# Domain entity
class Task:
    id: str
    title: str
    status: TaskStatus

# Database model
class TaskModel(SQLModel, table=True):
    id: int
    title: str

# Conversion in repository
@staticmethod
def from_model(db_model: TaskModel) -> Task:
    return Task(
        id=str(db_model.id),
        title=db_model.title,
        status=TaskStatus(db_model.status),
    )
```

### From Domain to Model

```python
# Conversion helper
def to_model(entity: Task) -> TaskModel:
    return TaskModel(
        title=entity.title,
        status=entity.status.value,
        description=entity.description,
    )
```

## Query Building

### Filter by Status

```python
async def get_by_status(self, status: TaskStatus) -> List[Task]:
    statement = select(TaskModel).where(TaskModel.status == status.value)
    result = await self.session.exec(statement)
    db_tasks = result.all()

    return [Task.from_model(t) for t in db_tasks]
```

### Filter by Multiple Criteria

```python
async def get_filtered(
    self,
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
) -> List[Task]:
    statement = select(TaskModel)

    if status:
        statement = statement.where(TaskModel.status == status.value)
    if priority:
        statement = statement.where(TaskModel.priority == priority.value)

    result = await self.session.exec(statement)
    db_tasks = result.all()

    return [Task.from_model(t) for t in db_tasks]
```

### Sorting

```python
async def get_all_sorted(
    self,
    sort_by: str = "created_at",
    descending: bool = True,
) -> List[Task]:
    statement = select(TaskModel)

    if sort_by == "created_at":
        col = TaskModel.created_at
    elif sort_by == "priority":
        col = TaskModel.priority

    if descending:
        statement = statement.order_by(col.desc())
    else:
        statement = statement.order_by(col)

    result = await self.session.exec(statement)
    db_tasks = result.all()

    return [Task.from_model(t) for t in db_tasks]
```

## Checklist

After creating repository, verify:
- [ ] Accepts Session in constructor
- [ ] All methods are async (use async/await)
- [ ] Returns domain entities, not database models
- [ ] Handles "not found" by returning None
- [ ] Uses context managers for transactions
- [ ] Session.refresh() after modifications
- [ ] Session.commit() after each operation
- [ ] Proper error handling
- [ ] No raw SQL queries exposed
- [ ] Domain model separation maintained
- [ ] Query parameters validated
- [ ] Pagination support (skip, limit)
- [ ] Filtering capabilities implemented
