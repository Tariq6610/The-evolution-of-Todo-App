from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.user import User


class UserRepositoryPort(ABC):
    """Port for user storage operations."""

    @abstractmethod
    def create(self, user: User) -> User:
        """Store a new user."""
        pass

    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]:
        """Retrieve a user by ID."""
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by email."""
        pass

    @abstractmethod
    def update(self, user_id: str, user_data: dict) -> User:
        """Update user information."""
        pass
