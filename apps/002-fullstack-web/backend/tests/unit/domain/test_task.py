"""Unit tests for Task entity and models."""

import pytest
from datetime import datetime, UTC

from src.domain.entities.task import Task
from src.domain.entities.task_status import TaskStatus
from src.domain.entities.priority import Priority


class TestTask:
    """Test cases for Task entity."""

    def test_task_creation_with_minimal_data(self) -> None:
        """Should create a Task with only required fields."""
        task = Task(
            id="task-1",
            title="Test Task",
        )

        assert task.id == "task-1"
        assert task.title == "Test Task"
        assert task.description is None
        assert task.status == TaskStatus.PENDING
        assert task.priority == Priority.MEDIUM
        assert task.tags == []
        assert isinstance(task.created_at, datetime)
        assert isinstance(task.updated_at, datetime)

    def test_task_creation_with_all_fields(self) -> None:
        """Should create a Task with all fields populated."""
        task = Task(
            id="task-2",
            title="Complete Project",
            description="Finish the project by deadline",
            status=TaskStatus.PENDING,
            priority=Priority.HIGH,
            tags=["work", "urgent"],
        )

        assert task.id == "task-2"
        assert task.title == "Complete Project"
        assert task.description == "Finish the project by deadline"
        assert task.status == TaskStatus.PENDING
        assert task.priority == Priority.HIGH
        assert task.tags == ["work", "urgent"]

    def test_task_with_completed_status(self) -> None:
        """Should create a Task with COMPLETED status."""
        task = Task(
            id="task-3",
            title="Done Task",
            status=TaskStatus.COMPLETED,
        )

        assert task.status == TaskStatus.COMPLETED

    def test_task_with_low_priority(self) -> None:
        """Should create a Task with LOW priority."""
        task = Task(
            id="task-4",
            title="Low Priority Task",
            priority=Priority.LOW,
        )

        assert task.priority == Priority.LOW

    def test_task_timestamps_auto_generated(self) -> None:
        """Should auto-generate created_at and updated_at timestamps."""
        before = datetime.now(UTC)

        task = Task(id="task-5", title="Test Task")

        after = datetime.now(UTC)

        assert before <= task.created_at <= after
        assert before <= task.updated_at <= after

    def test_title_must_not_be_whitespace_only(self) -> None:
        """Should reject titles with only whitespace."""
        with pytest.raises(ValueError, match="Title cannot be empty or whitespace-only"):
            Task(id="task-6", title="   ")


class TestTaskMethods:
    """Test cases for Task methods."""

    def test_mark_completed(self) -> None:
        """Should mark task as completed and update timestamp."""
        before = datetime.now(UTC)

        task = Task(id="task-7", title="Test", status=TaskStatus.PENDING)

        task.mark_completed()

        after = datetime.now(UTC)

        assert task.status == TaskStatus.COMPLETED
        assert before <= task.updated_at <= after

    def test_mark_pending(self) -> None:
        """Should mark task as pending and update timestamp."""
        before = datetime.now(UTC)

        task = Task(id="task-8", title="Test", status=TaskStatus.COMPLETED)

        task.mark_pending()

        after = datetime.now(UTC)

        assert task.status == TaskStatus.PENDING
        assert before <= task.updated_at <= after

    def test_toggle_status_from_pending(self) -> None:
        """Should toggle from PENDING to COMPLETED."""
        task = Task(id="task-9", title="Test", status=TaskStatus.PENDING)

        task.toggle_status()

        assert task.status == TaskStatus.COMPLETED

    def test_toggle_status_from_completed(self) -> None:
        """Should toggle from COMPLETED to PENDING."""
        task = Task(id="task-10", title="Test", status=TaskStatus.COMPLETED)

        task.toggle_status()

        assert task.status == TaskStatus.PENDING

    def test_multiple_toggles(self) -> None:
        """Should correctly toggle status multiple times."""
        task = Task(id="task-11", title="Test", status=TaskStatus.PENDING)

        task.toggle_status()
        assert task.status == TaskStatus.COMPLETED

        task.toggle_status()
        assert task.status == TaskStatus.PENDING

        task.toggle_status()
        assert task.status == TaskStatus.COMPLETED


class TaskPriorityValues:
    """Test cases for Priority enum values."""

    def test_low_priority(self) -> None:
        """Should have LOW priority value."""
        assert Priority.LOW == "LOW"

    def test_medium_priority(self) -> None:
        """Should have MEDIUM priority value."""
        assert Priority.MEDIUM == "MEDIUM"

    def test_high_priority(self) -> None:
        """Should have HIGH priority value."""
        assert Priority.HIGH == "HIGH"


class TaskStatusValues:
    """Test cases for TaskStatus enum values."""

    def test_pending_status(self) -> None:
        """Should have PENDING status value."""
        assert TaskStatus.PENDING == "PENDING"

    def test_completed_status(self) -> None:
        """Should have COMPLETED status value."""
        assert TaskStatus.COMPLETED == "COMPLETED"
