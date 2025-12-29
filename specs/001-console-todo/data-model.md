# Data Model: Phase I - In-Memory Console Todo App

**Feature**: 001-console-todo | **Date**: 2025-12-29

## Entities

### Task

Represents a todo item with complete attributes for tracking work.

**Location**: `src/domain/entities/task.py`

```python
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    """Task completion status."""
    PENDING = "pending"
    COMPLETED = "completed"


class Priority(str, Enum):
    """Task importance level."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Task(BaseModel):
    """
    Todo task entity.

    This entity is shared across all phases and forms the core domain model.
    Fields are technology-agnostic and use Pydantic for validation.

    Attributes:
        id: Unique task identifier (UUID string format)
        title: Task title (required, minimum 1 character)
        description: Optional detailed description
        status: Current completion state (pending/completed)
        priority: Importance level (low/medium/high)
        tags: List of category/label strings
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last modified
    """
    id: str = Field(..., description="Unique task identifier (UUID)")
    title: str = Field(..., min_length=1, description="Task title (required)")
    description: Optional[str] = Field(None, description="Optional detailed description")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Completion status")
    priority: Priority = Field(default=Priority.MEDIUM, description="Priority level")
    tags: List[str] = Field(default_factory=list, description="Category/label list")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")

    def mark_completed(self) -> None:
        """Mark task as completed and update timestamp."""
        self.status = TaskStatus.COMPLETED
        self.updated_at = datetime.utcnow()

    def mark_pending(self) -> None:
        """Mark task as pending and update timestamp."""
        self.status = TaskStatus.PENDING
        self.updated_at = datetime.utcnow()

    def toggle_status(self) -> None:
        """Toggle between pending and completed."""
        if self.status == TaskStatus.PENDING:
            self.mark_completed()
        else:
            self.mark_pending()
```

### Validation Rules

**From Functional Requirements**:

| Field | Rule | Requirement Reference |
|-------|-------|---------------------|
| id | Must be unique across all tasks | FR-002 |
| title | Must not be empty or whitespace-only | FR-007 |
| title | Minimum 1 character (enforced by Pydantic) | FR-007 |
| status | Must be either "pending" or "completed" | FR-004 |
| priority | Must be one of: low, medium, high | FR-010 |
| tags | Can be empty list, can contain multiple strings | FR-011 |

### State Transitions

**TaskStatus State Machine**:

```
    ┌──────────┐
    │ PENDING  │
    └────┬─────┘
         │ toggle_status()
         │
         ▼
    ┌──────────┐
    │COMPLETED │
    └────┬─────┘
         │ toggle_status()
         │
         ▼
    ┌──────────┐
    │ PENDING  │
    └──────────┘
```

**Transitions**:
- `pending` → `completed`: Via `mark_completed()` or `toggle_status()` when pending
- `completed` → `pending`: Via `mark_pending()` or `toggle_status()` when completed
- Self-transitions (pending→pending, completed→completed): Not allowed, no-op

**Requirements Coverage**:
- FR-004: Users can change status between pending and completed

### Relationships

**Current Phase (Phase I)**:
- Task is standalone entity
- No relationships to other entities (in-memory list storage)

**Future Phases**:
- Phase II: User relationship (many-to-one) for multi-user web app
- Phase III: AI conversation history relationship (one-to-many)
- Phase V: Event streaming relationship (audit log via Kafka)

### Storage Mapping

**In-Memory Storage (Phase I)**:
```python
# Storage: dict[str, Task] - maps task ID to Task object
tasks: dict[str, Task] = {}

# Operations:
# - Add: tasks[task.id] = task
# - Get: tasks.get(task_id)
# - List: list(tasks.values())
# - Update: tasks[task_id] = updated_task
# - Delete: del tasks[task_id]
# - Exists: task_id in tasks
```

**Future Storage Mappings**:
- Phase II (Neon DB): SQLModel/ORM mapping with table
- Phase V (Distributed): Event sourcing + read model in cache

## Collection Types

### TaskList

Represents the collection of tasks with CRUD operations.

**Location**: `src/domain/services/todo_service.py`

```python
from typing import List, Optional
from src.domain.entities.task import Task
from src.domain.ports.task_input_port import TaskInputPort
from src.domain.ports.task_output_port import TaskOutputPort
from src.domain.ports.storage_port import StoragePort


class TodoService:
    """
    Business logic service for todo operations.

    This service coordinates between ports and implements business rules.
    It contains pure domain logic with no framework dependencies.
    """

    def __init__(self, storage: StoragePort):
        self.storage = storage

    def create_task(
        self,
        title: str,
        description: Optional[str] = None,
        priority: Priority = Priority.MEDIUM,
        tags: Optional[List[str]] = None
    ) -> Task:
        """
        Create a new task with validation.

        Business Rules:
        - Title cannot be empty or whitespace (FR-007)
        - Unique ID generated via storage (FR-002)
        - Timestamps set to current time (FR-009)
        """
        # Implementation delegates to storage port
        pass

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks for display.

        Returns empty list if no tasks exist.
        """
        pass

    def update_task(
        self,
        task_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[Priority] = None,
        tags: Optional[List[str]] = None
    ) -> Task:
        """
        Update task fields.

        Only updates provided fields (partial update).
        Raises error if task not found (FR-008).
        Updates timestamp (FR-009).
        """
        pass

    def delete_task(self, task_id: str) -> None:
        """
        Delete a task by ID.

        Raises error if task not found (FR-008).
        """
        pass

    def toggle_task_status(self, task_id: str) -> Task:
        """
        Toggle task between pending and completed.

        Raises error if task not found (FR-008).
        Updates timestamp (FR-009).
        """
        pass

    def get_task_count(self) -> int:
        """
        Return total number of tasks.

        Used for display in View All Tasks (FR-014).
        """
        pass
```

## Data Flow Diagrams

### Create Task Flow

```
User Input (CLI)
    │
    ▼
ConsoleAdapter validates input
    │
    ▼
TodoService.create_task()
    │
    ▼
Task entity instantiated with validation
    │
    ▼
StoragePort.save() (in-memory)
    │
    ▼
Task returned with generated ID
    │
    ▼
ConsoleAdapter displays success
```

### View All Tasks Flow

```
User selects View All Tasks
    │
    ▼
TodoService.get_all_tasks()
    │
    ▼
StoragePort.get_all()
    │
    ▼
Task count calculated (FR-014)
    │
    ▼
ConsoleAdapter formats and displays
    │
    ▼
Tasks shown with all attributes (FR-003)
```

## Future Extensions

**Phase II+ Additions**:
- `due_date: Optional[datetime]` - Deadline tracking
- `recurrence: Optional[RecurrenceRule]` - Repeating tasks
- `user_id: Optional[str]` - Multi-user support
- `completed_at: Optional[datetime]` - Completion tracking

**Backward Compatibility**:
- New fields must be optional with defaults
- Existing fields never removed or renamed
- Serialization format stable across phases
