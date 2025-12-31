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


class UserAlreadyExistsError(Exception):
    """Raised when trying to register with an email that is already taken."""

    def __init__(self, email: str) -> None:
        self.email = email
        super().__init__(f"User with email '{email}' already exists")


class AuthenticationError(Exception):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Invalid email or password") -> None:
        self.message = message
        super().__init__(message)
