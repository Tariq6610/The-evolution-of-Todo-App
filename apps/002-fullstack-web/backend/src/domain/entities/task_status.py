"""TaskStatus enumeration for Todo application.

Defines task completion status as string enum for JSON serialization.
"""
from enum import Enum


class TaskStatus(str, Enum):
    """Task completion status.

    Values:
        - PENDING: Task is not yet completed
        - COMPLETED: Task has been finished
    """
    PENDING = "pending"
    COMPLETED = "completed"
