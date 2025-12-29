# Research: Phase I - In-Memory Console Todo App

**Feature**: 001-console-todo | **Date**: 2025-12-29

## Research Questions

**NONE** - No NEEDS CLARIFICATION markers in Technical Context. All technical decisions are clear:
- Python 3.11+ specified
- pytest, mypy, ruff dependencies defined
- In-memory storage confirmed
- TDD approach specified
- Hexagonal architecture mandated by constitution

## Technology Choices

### Python 3.11+

**Decision**: Python 3.11+
**Rationale**:
- Modern type hints improvements (TypeVar with default, Self type)
- Better performance and error messages
- Widely supported across platforms
- Constitution-specified language for Phase I

**Alternatives Considered**:
- Python 3.10: Slightly older, still supported but missing latest features
- Python 3.12+: Newest but may have compatibility issues on older systems

### pytest with TDD

**Decision**: pytest with pytest-cov, strict TDD Red-Green-Refactor
**Rationale**:
- Constitution-mandated testing approach for Phase I
- Industry standard for Python testing
- pytest fixtures enable clean test setup
- Coverage tracking ensures 100% domain logic coverage
- Red-Green-Refactor cycle enforced per constitution

**Alternatives Considered**:
- unittest (standard lib): More verbose, less feature-rich
- nose2: Depreciated, less modern than pytest

### In-Memory Storage

**Decision**: Python dict/list for task storage
**Rationale**:
- Specified in user requirements
- Simple, no external dependencies
- Adequate for single-user console app
- Easy to migrate to database in future phases

**Alternatives Considered**:
- SQLite file: Overkill for Phase I, adds complexity
- JSON file: Persistence not required for Phase I (in-memory specified)

### Hexagonal Architecture (Ports & Adapters)

**Decision**: Ports & Adapters pattern with domain/adapter separation
**Rationale**:
- Constitution-mandated architecture
- Enables seamless phase migration
- Domain logic remains pure, technology-agnostic
- Adapters can be swapped without affecting business rules

**Alternatives Considered**:
- Layered (MVC): Tighter coupling, harder to migrate
- Clean Architecture: Similar but more complex for this scope

## Best Practices Identified

### Type Hints with mypy Strict Mode

**Decision**: All functions/methods must have type hints, mypy strict mode
**Rationale**:
- Constitution-mandated (NON-NEGOTIABLE)
- Catches errors at development time
- Better IDE support and documentation
- Enables safe refactoring

**Implementation**:
```python
from typing import Optional
from datetime import datetime

def add_task(title: str, description: Optional[str] = None) -> Task:
    """Create a new task with given title and description."""
    ...
```

### ruff Linting and Formatting

**Decision**: ruff for both linting and formatting (replaces flake8, isort, black)
**Rationale**:
- Constitution-mandated
- Single tool for linting + formatting
- Faster than black/flake8/isort combo
- Compatible with existing configurations

**Implementation**:
```toml
[tool.ruff]
line-length = 88
select = ["E", "F", "I", "N", "W", "UP", "B", "C4", "SIM"]

[tool.mypy]
strict = true
warn_return_any = true
warn_unused_ignores = true
```

### Domain Entity Design

**Decision**: Pydantic models for entities (data validation + type safety)
**Rationale**:
- Combines type hints with runtime validation
- JSON serialization ready (future phases)
- Clear attribute definitions with validators
- Industry standard for Python models

**Implementation**:
```python
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Task(BaseModel):
    id: str = Field(..., description="Unique task identifier")
    title: str = Field(..., min_length=1, description="Task title")
    description: Optional[str] = Field(None, description="Optional description")
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    priority: Priority = Field(default=Priority.MEDIUM)
    tags: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

## Integration Patterns

### Port Interface Design

**Decision**: Abstract base classes (abc) for ports
**Rationale**:
- Enforces interface contracts
- Clear dependency inversion
- Easy mocking for testing
- Explicit contracts for adapters

**Implementation**:
```python
from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.task import Task

class TaskInputPort(ABC):
    @abstractmethod
    def add_task(self, task: Task) -> Task:
        """Add a new task and return with generated ID."""
        pass

    @abstractmethod
    def update_task(self, task_id: str, **updates) -> Task:
        """Update task fields and return updated task."""
        pass

    @abstractmethod
    def delete_task(self, task_id: str) -> None:
        """Delete task by ID."""
        pass

    @abstractmethod
    def toggle_status(self, task_id: str) -> Task:
        """Toggle task between pending and completed."""
        pass
```

### CLI Menu System

**Decision**: Simple numbered menu with input validation loop
**Rationale**:
- Specified in requirements (FR-012)
- Familiar pattern for console users
- Easy to implement and test
- Scales to more options gracefully

**Implementation Pattern**:
```python
def show_menu() -> None:
    """Display numbered menu options."""
    print("\n=== Todo Menu ===")
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Complete/Incomplete")
    print("0. Exit")

def get_user_choice() -> int:
    """Get and validate user menu choice."""
    while True:
        try:
            choice = int(input("Enter choice: "))
            if 0 <= choice <= 5:
                return choice
            print("Invalid choice. Please enter 0-5.")
        except ValueError:
            print("Please enter a number.")
```

## Summary

All technical decisions resolved without NEEDS CLARIFICATION. Design follows constitution mandates:
- Python 3.11+ with strict type hints
- TDD with pytest (Red-Green-Refactor)
- Hexagonal architecture (Ports & Adapters)
- In-memory storage with Pydantic entities
- ruff for linting/formatting, mypy strict mode

No blockers for proceeding to Phase 1 design artifacts.
