"""InMemoryStorage adapter for task persistence.

This adapter implements StoragePort using Python dict/list for in-memory storage.
Phase I implementation - data lost on application exit.
"""
import uuid

from src.domain.entities.task import Task
from src.domain.ports.storage_port import StoragePort


class InMemoryStorage(StoragePort):
    """
    In-memory storage adapter for tasks.

    Uses Python dict[str, Task] for O(1) lookups.
    Data is ephemeral - lost when application exits.
    Suitable for Phase I single-user console app.
    """

    def __init__(self) -> None:
        """Initialize empty in-memory storage."""
        self._tasks: dict[str, Task] = {}

    def save(self, task: Task) -> Task:
        """
        Save a new task and return it with generated ID.

        Generates UUID if task.id is empty.

        Args:
            task: Task to save

        Returns:
            Task with generated unique ID

        Raises:
            ValueError: If task validation fails
        """
        # Generate ID if not provided
        task_id = task.id if task.id else str(uuid.uuid4())
        # Create new task with generated ID
        saved_task = Task(
            id=task_id,
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            tags=task.tags,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )
        self._tasks[task_id] = saved_task
        return saved_task

    def get(self, task_id: str) -> Task | None:
        """
        Retrieve a task by ID.

        Args:
            task_id: Unique task identifier

        Returns:
            Task if found, None otherwise
        """
        return self._tasks.get(task_id)

    def get_all(self) -> list[Task]:
        """
        Retrieve all tasks.

        Returns:
            List of all tasks (empty list if none exist)
        """
        return list(self._tasks.values())

    def update(self, task_id: str, task: Task) -> Task:
        """
        Update an existing task.

        Args:
            task_id: ID of task to update
            task: Updated task data

        Returns:
            Updated task

        Raises:
            ValueError: If task_id not found
        """
        if task_id not in self._tasks:
            raise ValueError(f"Task with ID '{task_id}' not found")

        # Create updated task with provided id
        updated_task = Task(
            id=task_id,
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            tags=task.tags,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )
        self._tasks[task_id] = updated_task
        return updated_task

    def delete(self, task_id: str) -> None:
        """
        Delete a task by ID.

        Args:
            task_id: ID of task to delete

        Raises:
            ValueError: If task_id not found
        """
        if task_id not in self._tasks:
            raise ValueError(f"Task with ID '{task_id}' not found")
        del self._tasks[task_id]

    def exists(self, task_id: str) -> bool:
        """
        Check if a task exists.

        Args:
            task_id: ID of task to check

        Returns:
            True if task exists, False otherwise
        """
        return task_id in self._tasks
