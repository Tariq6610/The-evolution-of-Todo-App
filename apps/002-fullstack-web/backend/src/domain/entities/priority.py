"""Priority enumeration for Todo application.

Defines task importance levels as string enum for JSON serialization.
"""
from enum import Enum


class Priority(str, Enum):
    """Task importance level.

    Values:
        - LOW: Task is low priority
        - MEDIUM: Task is medium priority (default)
        - HIGH: Task is high priority
    """
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
