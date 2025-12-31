"""Tests for Task entity with Pydantic validation."""
import pytest
from datetime import datetime, timezone
from pydantic import ValidationError

from src.domain.entities.task import Task, TaskStatus, Priority


class TestTask:
    """Tests for Task entity creation and validation."""

    def test_task_creation_with_required_fields(self) -> None:
        """Task should be created with required fields (id, title)."""
        # Test minimal valid task
        task = Task(
            id="test-001",
            title="Test Task"
        )
        assert task.id == "test-001"
        assert task.title == "Test Task"
        assert task.description is None
        assert task.status == TaskStatus.PENDING
        assert task.priority == Priority.MEDIUM
        assert task.tags == []

    def test_task_creation_with_all_fields(self) -> None:
        """Task should be created with all optional fields populated."""
        # Test task with all fields
        task = Task(
            id="test-002",
            title="Complete Test Task",
            description="A detailed description",
            status=TaskStatus.COMPLETED,
            priority=Priority.HIGH,
            tags=["work", "urgent"],
        )
        assert task.id == "test-002"
        assert task.title == "Complete Test Task"
        assert task.description == "A detailed description"
        assert task.status == TaskStatus.COMPLETED
        assert task.priority == Priority.HIGH
        assert task.tags == ["work", "urgent"]

    def test_task_title_cannot_be_empty(self) -> None:
        """Task title should reject empty strings."""
        # Test that empty title raises validation error
        with pytest.raises(ValidationError):
            Task(id="test-003", title="")

    def test_task_title_cannot_be_whitespace_only(self) -> None:
        """Task title should reject whitespace-only strings."""
        # Test that whitespace-only title raises validation error
        with pytest.raises(ValidationError):
            Task(id="test-004", title="   ")

    def test_task_title_minimum_length(self) -> None:
        """Task title should enforce minimum length of 1 character."""
        # Test single character title works
        task = Task(id="test-005", title="A")
        assert task.title == "A"

    def test_task_title_supports_longer_titles(self) -> None:
        """Task title should support longer text."""
        # Test longer title
        long_title = "A" * 100
        task = Task(id="test-006", title=long_title)
        assert len(task.title) == 100

    def test_task_description_optional(self) -> None:
        """Task description should be optional (None by default)."""
        # Test description defaults to None
        task = Task(id="test-007", title="Task")
        assert task.description is None

    def test_task_description_can_be_empty_string(self) -> None:
        """Task description can be an empty string if provided."""
        # Test explicit empty string
        task = Task(id="test-008", title="Task", description="")
        assert task.description == ""

    def test_task_status_default_is_pending(self) -> None:
        """Task status should default to PENDING."""
        # Test default status
        task = Task(id="test-009", title="Task")
        assert task.status == TaskStatus.PENDING

    def test_task_status_can_be_completed(self) -> None:
        """Task status can be set to COMPLETED."""
        # Test completed status
        task = Task(id="test-010", title="Task", status=TaskStatus.COMPLETED)
        assert task.status == TaskStatus.COMPLETED

    def test_task_priority_default_is_medium(self) -> None:
        """Task priority should default to MEDIUM."""
        # Test default priority
        task = Task(id="test-011", title="Task")
        assert task.priority == Priority.MEDIUM

    def test_task_priority_can_be_low(self) -> None:
        """Task priority can be set to LOW."""
        # Test low priority
        task = Task(id="test-012", title="Task", priority=Priority.LOW)
        assert task.priority == Priority.LOW

    def test_task_priority_can_be_high(self) -> None:
        """Task priority can be set to HIGH."""
        # Test high priority
        task = Task(id="test-013", title="Task", priority=Priority.HIGH)
        assert task.priority == Priority.HIGH

    def test_task_tags_default_is_empty_list(self) -> None:
        """Task tags should default to empty list."""
        # Test default tags
        task = Task(id="test-014", title="Task")
        assert task.tags == []

    def test_task_tags_can_contain_multiple_values(self) -> None:
        """Task tags should support multiple string values."""
        # Test multiple tags
        task = Task(id="test-015", title="Task", tags=["work", "urgent"])
        assert task.tags == ["work", "urgent"]

    def test_task_created_at_timestamp(self) -> None:
        """Task should capture creation timestamp."""
        # Test creation timestamp
        task = Task(id="test-016", title="Task")
        assert isinstance(task.created_at, datetime)
        # Test timestamp is recent (within last second)
        assert (datetime.now(timezone.utc) - task.created_at).total_seconds() < 1

    def test_task_updated_at_timestamp(self) -> None:
        """Task should capture last update timestamp."""
        # Test update timestamp
        task = Task(id="test-017", title="Task")
        assert isinstance(task.updated_at, datetime)
        # Test timestamp is recent (within last second)
        assert (datetime.now(timezone.utc) - task.updated_at).total_seconds() < 1

    def test_task_mark_completed_updates_status_and_timestamp(self) -> None:
        """mark_completed should change status to COMPLETED and update timestamp."""
        # Test mark_completed method
        task = Task(id="test-018", title="Task", status=TaskStatus.PENDING)
        original_updated = task.updated_at

        task.mark_completed()

        assert task.status == TaskStatus.COMPLETED
        assert task.updated_at > original_updated

    def test_task_mark_pending_updates_status_and_timestamp(self) -> None:
        """mark_pending should change status to PENDING and update timestamp."""
        # Test mark_pending method
        task = Task(id="test-019", title="Task", status=TaskStatus.COMPLETED)
        original_updated = task.updated_at

        task.mark_pending()

        assert task.status == TaskStatus.PENDING
        assert task.updated_at > original_updated

    def test_task_toggle_status_from_pending_to_completed(self) -> None:
        """toggle_status should change PENDING to COMPLETED and update timestamp."""
        # Test toggle from pending to completed
        task = Task(id="test-020", title="Task", status=TaskStatus.PENDING)
        original_updated = task.updated_at

        task.toggle_status()

        assert task.status == TaskStatus.COMPLETED
        assert task.updated_at > original_updated

    def test_task_toggle_status_from_completed_to_pending(self) -> None:
        """toggle_status should change COMPLETED to PENDING and update timestamp."""
        # Test toggle from completed to pending
        task = Task(id="test-021", title="Task", status=TaskStatus.COMPLETED)
        original_updated = task.updated_at

        task.toggle_status()

        assert task.status == TaskStatus.PENDING
        assert task.updated_at > original_updated

    def test_task_serialization_includes_all_fields(self) -> None:
        """Task should be serializable with all fields included."""
        # Test model_dump includes all fields
        task = Task(
            id="test-022",
            title="Serialization Test",
            description="Test description",
            status=TaskStatus.COMPLETED,
            priority=Priority.HIGH,
            tags=["test"]
        )

        task_dict = task.model_dump()
        assert task_dict["id"] == "test-022"
        assert task_dict["title"] == "Serialization Test"
        assert task_dict["description"] == "Test description"
        assert task_dict["status"] == "completed"
        assert task_dict["priority"] == "high"
        assert task_dict["tags"] == ["test"]
        assert "created_at" in task_dict
        assert "updated_at" in task_dict
