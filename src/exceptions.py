"""Custom exceptions for todo application.

Domain-specific exceptions for better error handling.
"""


class TaskNotFoundError(Exception):
    """Raised when a task is not found."""

    def __init__(self, task_id: str) -> None:
        self.task_id = task_id
        super().__init__(f"Task with ID '{task_id}' not found")


class InvalidTaskError(Exception):
    """Raised when task validation fails."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)
