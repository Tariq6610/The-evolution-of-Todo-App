from typing import Any

from src.adapters.security.jwt import create_access_token
from src.adapters.security.password import get_password_hash, verify_password
from src.domain.entities.user import User, UserCreate
from src.domain.exceptions import AuthenticationError, UserAlreadyExistsError
from src.domain.ports.user_repository_port import UserRepositoryPort


class AuthService:
    """Service for authentication logic."""

    def __init__(self, user_repo: UserRepositoryPort):
        self.user_repo = user_repo

    def register(self, user_in: UserCreate) -> User:
        """Register a new user."""
        existing_user = self.user_repo.get_by_email(user_in.email)
        if existing_user:
            raise UserAlreadyExistsError(user_in.email)

        password_hash = get_password_hash(user_in.password)
        new_user = User(
            email=user_in.email,
            full_name=user_in.full_name,
            hashed_password=password_hash,
            is_active=True,
        )
        return self.user_repo.create(new_user)

    def authenticate(self, email: str, password: str) -> User:
        """Authenticate a user and return the user object."""
        user = self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise AuthenticationError()
        if not user.is_active:
            raise AuthenticationError("User is inactive")
        return user

    def create_token(self, user: User) -> dict[str, str]:
        """Create a JWT token for a user."""
        access_token = create_access_token(data={"sub": user.id})
        return {"access_token": access_token, "token_type": "bearer"}
