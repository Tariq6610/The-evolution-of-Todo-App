"""Task entity for Todo application.

This entity is shared across all phases and forms the core domain model.
Uses Pydantic for validation and serialization.
"""
from datetime import UTC, datetime

from pydantic import BaseModel, Field, field_validator
from src.domain.entities.priority import Priority
from src.domain.entities.task_status import TaskStatus


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
    description: str | None = Field(
        None, description="Optional detailed description"
    )
    status: TaskStatus = Field(
        default=TaskStatus.PENDING, description="Completion status"
    )
    priority: Priority = Field(
        default=Priority.MEDIUM, description="Priority level"
    )
    tags: list[str] = Field(default_factory=list, description="Category/label list")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Creation timestamp",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Last update timestamp",
    )

    @field_validator("title")
    @classmethod
    def title_must_not_be_whitespace_only(cls, v: str) -> str:
        """Validate that title is not whitespace-only."""
        if v.strip() == "":
            raise ValueError("Title cannot be empty or whitespace-only")
        return v.strip()

    def mark_completed(self) -> None:
        """Mark task as completed and update timestamp."""
        self.status = TaskStatus.COMPLETED
        self.updated_at = datetime.now(UTC)

    def mark_pending(self) -> None:
        """Mark task as pending and update timestamp."""
        self.status = TaskStatus.PENDING
        self.updated_at = datetime.now(UTC)

    def toggle_status(self) -> None:
        """Toggle between pending and completed."""
        if self.status == TaskStatus.PENDING:
            self.mark_completed()
        else:
            self.mark_pending()
