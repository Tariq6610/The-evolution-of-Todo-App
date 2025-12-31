"""Tests for TodoService business logic."""
import pytest

from src.domain.services.todo_service import TodoService
from src.domain.entities.task import TaskStatus, Priority
from src.adapters.storage.in_memory_storage import InMemoryStorage


class TestTodoService:
    """Tests for TodoService business logic."""

    def test_create_task_with_title_validation(self) -> None:
        """TodoService.create_task() should create task with generated ID."""
        storage = InMemoryStorage()
        service = TodoService(storage)

        task = service.create_task(
            title="Test Task",
            description="Test description",
            priority=Priority.HIGH,
            tags=["test"],
        )

        assert task.id != ""
        assert task.title == "Test Task"
        assert task.description == "Test description"
        assert task.status == TaskStatus.PENDING
        assert task.priority == Priority.HIGH
        assert task.tags == ["test"]

    def test_create_task_with_minimal_fields(self) -> None:
        """TodoService.create_task() should work with only title."""
        storage = InMemoryStorage()
        service = TodoService(storage)

        task = service.create_task(title="Minimal Task")

        assert task.id != ""
        assert task.title == "Minimal Task"
        assert task.description is None
        assert task.status == TaskStatus.PENDING
        assert task.priority == Priority.MEDIUM
        assert task.tags == []

    def test_get_all_tasks_returns_empty_list(self) -> None:
        """TodoService.get_all_tasks() should return empty list when no tasks."""
        storage = InMemoryStorage()
        service = TodoService(storage)

        tasks = service.get_all_tasks()

        assert tasks == []

    def test_get_all_tasks_returns_all_tasks(self) -> None:
        """TodoService.get_all_tasks() should return all created tasks."""
        storage = InMemoryStorage()
        service = TodoService(storage)

        task1 = service.create_task(title="Task 1")
        task2 = service.create_task(title="Task 2")

        tasks = service.get_all_tasks()

        assert len(tasks) == 2
        assert any(t.id == task1.id for t in tasks)
        assert any(t.id == task2.id for t in tasks)

    def test_update_task_partial_fields(self) -> None:
        """TodoService.update_task() should update only provided fields."""
        storage = InMemoryStorage()
        service = TodoService(storage)

        task = service.create_task(title="Original Title")
        original_description = task.description

        updated_task = service.update_task(task.id, title="Updated Title")

        assert updated_task.id == task.id
        assert updated_task.title == "Updated Title"
        assert updated_task.description == original_description

    def test_update_task_all_fields(self) -> None:
        """TodoService.update_task() should update all fields when provided."""
        storage = InMemoryStorage()
        service = TodoService(storage)

        task = service.create_task(title="Original", description="Orig Desc")
        original_created_at = task.created_at

        updated_task = service.update_task(
            task.id,
            title="Updated",
            description="New Desc",
            priority=Priority.HIGH,
            tags=["updated"],
        )

        assert updated_task.id == task.id
        assert updated_task.title == "Updated"
        assert updated_task.description == "New Desc"
        assert updated_task.priority == Priority.HIGH
        assert updated_task.tags == ["updated"]
        assert updated_task.created_at == original_created_at
        assert updated_task.updated_at > original_created_at

    def test_update_task_not_found_raises_error(self) -> None:
        """TodoService.update_task() should raise ValueError for non-existent task."""
        storage = InMemoryStorage()
        service = TodoService(storage)

        with pytest.raises(ValueError, match="not found"):
            service.update_task("non-existent-id", title="New Title")

    def test_delete_task_removes_task(self) -> None:
        """TodoService.delete_task() should remove task from storage."""
        storage = InMemoryStorage()
        service = TodoService(storage)

        task = service.create_task(title="To Delete")
        service.delete_task(task.id)

        tasks = service.get_all_tasks()
        assert len(tasks) == 0

    def test_delete_task_not_found_raises_error(self) -> None:
        """TodoService.delete_task() should raise ValueError for non-existent task."""
        storage = InMemoryStorage()
        service = TodoService(storage)

        with pytest.raises(ValueError, match="not found"):
            service.delete_task("non-existent-id")

    def test_toggle_task_status_pending_to_completed(self) -> None:
        """TodoService.toggle_task_status() should change PENDING to COMPLETED."""
        storage = InMemoryStorage()
        service = TodoService(storage)

        task = service.create_task(title="Toggle Test")
        assert task.status == TaskStatus.PENDING

        updated_task = service.toggle_task_status(task.id)

        assert updated_task.id == task.id
        assert updated_task.status == TaskStatus.COMPLETED

    def test_toggle_task_status_completed_to_pending(self) -> None:
        """TodoService.toggle_task_status() should change COMPLETED to PENDING."""
        storage = InMemoryStorage()
        service = TodoService(storage)

        task = service.create_task(title="Toggle Test")
        service.toggle_task_status(task.id)  # Mark as completed

        updated_task = service.toggle_task_status(task.id)

        assert updated_task.status == TaskStatus.PENDING

    def test_toggle_task_status_not_found_raises_error(self) -> None:
        """TodoService.toggle_task_status() should raise ValueError for non-existent task."""
        storage = InMemoryStorage()
        service = TodoService(storage)

        with pytest.raises(ValueError, match="not found"):
            service.toggle_task_status("non-existent-id")

    def test_get_task_count_returns_zero(self) -> None:
        """TodoService.get_task_count() should return 0 when no tasks."""
        storage = InMemoryStorage()
        service = TodoService(storage)

        assert service.get_task_count() == 0

    def test_get_task_count_returns_actual_count(self) -> None:
        """TodoService.get_task_count() should return actual task count."""
        storage = InMemoryStorage()
        service = TodoService(storage)

        service.create_task(title="Task 1")
        service.create_task(title="Task 2")
        service.create_task(title="Task 3")

        assert service.get_task_count() == 3
