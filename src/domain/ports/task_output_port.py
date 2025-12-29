"""TaskOutputPort interface for task query operations.

This port defines the contract for task retrieval operations.
Following Hexagonal Architecture - adapters implement this interface.
"""
from abc import ABC, abstractmethod

from src.domain.entities.task import Task


class TaskOutputPort(ABC):
    """
    Abstract interface for task query operations.

    This port defines queries that retrieve tasks without modifying them.
    Separated from TaskInputPort (commands) per CQRS pattern.
    """

    @abstractmethod
    def get_all_tasks(self) -> list[Task]:
        """
        Retrieve all tasks.

        Returns:
            List of all tasks (empty list if none exist)
        """
        pass

    @abstractmethod
    def get_task_by_id(self, task_id: str) -> Task:
        """
        Retrieve a task by ID.

        Args:
            task_id: Unique task identifier

        Returns:
            Task with matching ID

        Raises:
            ValueError: If task_id not found
        """
        pass

    @abstractmethod
    def get_task_count(self) -> int:
        """
        Get total number of tasks.

        Returns:
            Number of tasks (0 if none exist)
        """
        pass
