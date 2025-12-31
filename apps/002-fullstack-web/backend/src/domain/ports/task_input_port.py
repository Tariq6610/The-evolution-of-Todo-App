"""TaskInputPort interface for task command operations.

This port defines the contract for task modification operations.
Following Hexagonal Architecture - adapters implement this interface.
"""
from abc import ABC, abstractmethod

from src.domain.entities.priority import Priority
from src.domain.entities.task import Task


class TaskInputPort(ABC):
    """
    Abstract interface for task command operations.

    This port defines commands that modify tasks (create, update, delete, toggle).
    Separated from TaskOutputPort (queries) per CQRS pattern.
    """

    @abstractmethod
    def create_task(
        self,
        title: str,
        description: str | None = None,
        priority: Priority = Priority.MEDIUM,
        tags: list[str] | None = None,
    ) -> Task:
        """
        Create a new task.

        Args:
            title: Task title (required)
            description: Optional detailed description
            priority: Task priority (default: MEDIUM)
            tags: Optional list of tags

        Returns:
            Created task with generated ID

        Raises:
            ValueError: If title is empty or whitespace
        """
        pass

    @abstractmethod
    def update_task(
        self,
        task_id: str,
        title: str | None = None,
        description: str | None = None,
        priority: Priority | None = None,
        tags: list[str] | None = None,
    ) -> Task:
        """
        Update task fields.

        Only updates provided fields (partial update).

        Args:
            task_id: ID of task to update
            title: New title (optional)
            description: New description (optional)
            priority: New priority (optional)
            tags: New tags (optional)

        Returns:
            Updated task

        Raises:
            ValueError: If task_id not found or title is empty
        """
        pass

    @abstractmethod
    def delete_task(self, task_id: str) -> None:
        """
        Delete a task.

        Args:
            task_id: ID of task to delete

        Raises:
            ValueError: If task_id not found
        """
        pass

    @abstractmethod
    def toggle_task_status(self, task_id: str) -> Task:
        """
        Toggle task between pending and completed.

        Args:
            task_id: ID of task to toggle

        Returns:
            Task with updated status

        Raises:
            ValueError: If task_id not found
        """
        pass
