"""Tests for InMemoryStorage adapter."""
import pytest

from src.domain.entities.task import Task, TaskStatus, Priority
from src.adapters.storage.in_memory_storage import InMemoryStorage


class TestInMemoryStorage:
    """Tests for InMemoryStorage adapter."""

    def test_save_generates_unique_id(self) -> None:
        """InMemoryStorage.save() should generate unique ID for empty task."""
        storage = InMemoryStorage()
        task = Task(id="", title="Test Task")

        saved_task = storage.save(task)

        assert saved_task.id != ""
        assert len(saved_task.id) > 0

    def test_save_preserves_id_if_provided(self) -> None:
        """InMemoryStorage.save() should use provided ID if not empty."""
        storage = InMemoryStorage()
        task = Task(id="custom-id", title="Test Task")

        saved_task = storage.save(task)

        assert saved_task.id == "custom-id"

    def test_save_stores_task(self) -> None:
        """InMemoryStorage.save() should store task in internal dict."""
        storage = InMemoryStorage()
        task = Task(id="", title="Stored Task")

        saved_task = storage.save(task)

        retrieved_task = storage.get(saved_task.id)
        assert retrieved_task is not None
        assert retrieved_task.id == saved_task.id
        assert retrieved_task.title == "Stored Task"

    def test_get_returns_task(self) -> None:
        """InMemoryStorage.get() should return task by ID."""
        storage = InMemoryStorage()
        task = Task(id="", title="Get Test")
        saved_task = storage.save(task)

        retrieved_task = storage.get(saved_task.id)

        assert retrieved_task is not None
        assert retrieved_task.id == saved_task.id

    def test_get_returns_none_for_non_existent(self) -> None:
        """InMemoryStorage.get() should return None for non-existent ID."""
        storage = InMemoryStorage()

        task = storage.get("non-existent-id")

        assert task is None

    def test_get_all_returns_all_tasks(self) -> None:
        """InMemoryStorage.get_all() should return list of all tasks."""
        storage = InMemoryStorage()

        task1 = storage.save(Task(id="", title="Task 1"))
        task2 = storage.save(Task(id="", title="Task 2"))
        task3 = storage.save(Task(id="", title="Task 3"))

        all_tasks = storage.get_all()

        assert len(all_tasks) == 3
        task_ids = {t.id for t in all_tasks}
        assert task_ids == {task1.id, task2.id, task3.id}

    def test_get_all_returns_empty_list_when_no_tasks(self) -> None:
        """InMemoryStorage.get_all() should return empty list when no tasks."""
        storage = InMemoryStorage()

        all_tasks = storage.get_all()

        assert all_tasks == []

    def test_update_modifies_task(self) -> None:
        """InMemoryStorage.update() should update task with new values."""
        storage = InMemoryStorage()
        original_task = storage.save(Task(id="", title="Original"))

        updated_task_data = Task(
            id=original_task.id,
            title="Updated",
            description="New Description",
            status=TaskStatus.COMPLETED,
            priority=Priority.HIGH,
            tags=["updated"],
        )

        updated_task = storage.update(original_task.id, updated_task_data)

        assert updated_task.id == original_task.id
        assert updated_task.title == "Updated"
        assert updated_task.description == "New Description"

        retrieved_task = storage.get(original_task.id)
        assert retrieved_task.title == "Updated"

    def test_update_not_found_raises_error(self) -> None:
        """InMemoryStorage.update() should raise ValueError for non-existent task."""
        storage = InMemoryStorage()
        task = Task(id="", title="Test")

        with pytest.raises(ValueError, match="not found"):
            storage.update("non-existent-id", task)

    def test_delete_removes_task(self) -> None:
        """InMemoryStorage.delete() should remove task from storage."""
        storage = InMemoryStorage()
        task = storage.save(Task(id="", title="Delete Test"))

        storage.delete(task.id)

        retrieved_task = storage.get(task.id)
        assert retrieved_task is None

    def test_delete_not_found_raises_error(self) -> None:
        """InMemoryStorage.delete() should raise ValueError for non-existent task."""
        storage = InMemoryStorage()

        with pytest.raises(ValueError, match="not found"):
            storage.delete("non-existent-id")

    def test_exists_returns_true_for_existing_task(self) -> None:
        """InMemoryStorage.exists() should return True for existing task."""
        storage = InMemoryStorage()
        task = storage.save(Task(id="", title="Exists Test"))

        assert storage.exists(task.id) is True

    def test_exists_returns_false_for_non_existent_task(self) -> None:
        """InMemoryStorage.exists() should return False for non-existent task."""
        storage = InMemoryStorage()

        assert storage.exists("non-existent-id") is False
