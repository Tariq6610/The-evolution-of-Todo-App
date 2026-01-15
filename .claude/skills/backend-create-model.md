# Backend: Create Model

Creates a SQLModel database model with Pydantic validation, relationships, and proper indexes.

## Usage

```
/sp.backend.create-model <ModelName> [--description "<desc>"]
```

## Examples

```bash
# Create Task model
/sp.backend.create-model Task --description "Core task entity with status, priority, tags"

# Create User model
/sp.backend.create-model User --description "User authentication model with email and password"
```

## Model Creation Rules

1. **File Location**: `apps/002-fullstack-web/backend/app/db/models.py`
2. **Inherit from SQLModel**: Base class for all models
3. **Table Configuration**: `table=True` with custom table name
4. **Field Types**: Use appropriate SQLModel field types
5. **Indexes**: Add indexes for frequently queried fields
6. **Relationships**: Use SQLModel relationships (one-to-many, many-to-many)
7. **Validation**: Field constraints (max_length, nullable, default)
8. **Default Values**: Use `default_factory` for timestamps, mutable lists
9. **Type Hints**: All fields properly typed

## Field Types

| Python Type | SQLModel Field | Description |
|-------------|---------------|-------------|
| `str` | `Field()` | Variable-length strings |
| `str | None` | `Field(default=None)` | Optional strings |
| `int` | `Field()` | Integer values, auto-increment with primary_key=True |
| `int | None` | `Field(default=None)` | Optional integers |
| `bool` | `Field()` | Boolean values |
| `bool | None` | `Field(default=False)` | Optional booleans |
| `datetime` | `Field(default_factory=datetime.utcnow)` | Timestamps |
| `float` | `Field()` | Decimal values |
| `list[str]` | `Field(default_factory=list, sa_column=JSON)` | String arrays (as JSON) |
| `dict` | `Field(sa_column=JSON)` | JSON objects |

## Example: Task Model

```python
# app/db/models.py
from typing import List, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Column, Text, JSON
from pydantic import EmailStr

class TaskModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True, max_length=200)
    description: Optional[str] = Field(default=None, max_length=500)
    status: str = Field(default="pending", max_length=20)
    priority: str = Field(default="medium", max_length=10)
    tags: List[str] = Field(default_factory=list, sa_column=JSON)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    due_date: Optional[datetime] = Field(default=None, index=True)

    class Config:
        indexes = [
            ("idx_task_status", ["status"]),
            ("idx_task_priority", ["priority"]),
            ("idx_task_due_date", ["due_date"]),
        ]
```

## Example: User Model

```python
class UserModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    username: str = Field(unique=True, index=True, max_length=100)
    password_hash: str = Field(max_length=255)  # Don't store plain passwords!
    full_name: Optional[str] = Field(default=None, max_length=255)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)

    class Config:
        indexes = [
            ("idx_user_email", ["email"]),
            ("idx_user_username", ["username"]),
        ]
```

## Relationships

### One-to-Many

```python
# User has many tasks
class UserModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, max_length=100)

class TaskModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True, max_length=200)
    user_id: int | None = Field(default=None, foreign_key="user.id", index=True)

    # Relationship attribute
    user: "UserModel" = Relationship(back_populates="tasks")
```

### Many-to-Many

```python
# Tasks can have many tags
class TaskTagModel(SQLModel, table=True):
    task_id: int | None = Field(foreign_key="task.id", primary_key=True)
    tag_id: int | None = Field(foreign_key="tag.id", primary_key=True)

class TaskModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True, max_length=200)

    # Relationships
    tags: list["TaskTagModel"] = Relationship(
        back_populates="task_associations",
        link_model=TaskTagModel
    )
```

## Best Practices

### Primary Key
```python
id: int | None = Field(default=None, primary_key=True)
```

### Unique Constraints
```python
email: EmailStr = Field(unique=True)  # SQLModel handles email validation
username: str = Field(unique=True, max_length=100)
```

### Indexes
```python
class Config:
    indexes = [
        ("idx_user_email", ["email"]),  # Single column
        ("idx_task_status_priority", ["status", "priority"]),  # Multi-column
    ]
```

### Default Values

```python
# Bad: Mutable default
tags: List[str] = Field(default=[])  # List is mutable!

# Good: Factory function
tags: List[str] = Field(default_factory=list)
created_at: datetime = Field(default_factory=datetime.utcnow)
```

### Foreign Keys

```python
user_id: int | None = Field(foreign_key="user.id", index=True)

# Don't forget to define relationship
user: "UserModel" = Relationship(back_populates="user_tasks")
```

### Large Text Fields

```python
# Use Text for unbounded text
description: Text = Field(default=None)  # PostgreSQL TEXT type

# Or str with explicit max_length
title: str = Field(max_length=200)
```

## Database Migration

After creating model, generate migration:

```bash
# In backend directory
cd apps/002-fullstack-web/backend

# Run Alembic migration
alembic revision --autogenerate -m "Added <ModelName> model"

# Apply migration
alembic upgrade head
```

## Checklist

After creating model, verify:
- [ ] Inherits from SQLModel
- [ ] table=True with meaningful table name
- [ ] Primary key defined
- [ ] Appropriate field types used
- [ ] Max length constraints on string fields
- [ ] Default values (default or default_factory)
- [ ] Indexes added for frequently queried fields
- [ ] Foreign keys properly defined
- [ ] Relationships defined where needed
- [ ] Type hints correct
- [ ] Database migration generated
- [ ] No hardcoded passwords or sensitive data
- [ ] Follows naming conventions (PascalCase model)
