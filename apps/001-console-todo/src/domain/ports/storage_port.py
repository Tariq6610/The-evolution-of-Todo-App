"""StoragePort interface for task persistence.

This port defines the contract for task storage adapters.
Following Hexagonal Architecture - adapters implement this interface.
"""
from abc import ABC, abstractmethod

from src.domain.entities.task import Task


class StoragePort(ABC):
    """
    Abstract interface for task storage.

    This port defines the contract that storage adapters must implement.
    Enables swapping storage implementations (in-memory, database, etc.)
    without affecting domain logic.
    """

    @abstractmethod
    def save(self, task: Task) -> Task:
        """
        Save a new task and return it with generated ID.

        Args:
            task: Task to save (may have placeholder ID)

        Returns:
            Task with generated unique ID

        Raises:
            ValueError: If task validation fails
        """
        pass

    @abstractmethod
    def get(self, task_id: str) -> Task | None:
        """
        Retrieve a task by ID.

        Args:
            task_id: Unique task identifier

        Returns:
            Task if found, None otherwise
        """
        pass

    @abstractmethod
    def get_all(self) -> list[Task]:
        """
        Retrieve all tasks.

        Returns:
            List of all tasks (empty list if none exist)
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def delete(self, task_id: str) -> None:
        """
        Delete a task by ID.

        Args:
            task_id: ID of task to delete

        Raises:
            ValueError: If task_id not found
        """
        pass

    @abstractmethod
    def exists(self, task_id: str) -> bool:
        """
        Check if a task exists.

        Args:
            task_id: ID of task to check

        Returns:
            True if task exists, False otherwise
        """
        pass
