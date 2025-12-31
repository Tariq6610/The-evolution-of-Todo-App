from sqlmodel import Session, select
from typing import Optional

from src.domain.entities.user import User
from src.domain.ports.user_repository_port import UserRepositoryPort


class SQLUserRepository(UserRepositoryPort):
    """SQL adapter for user repository."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_by_id(self, user_id: str) -> Optional[User]:
        statement = select(User).where(User.id == user_id)
        return self.session.exec(statement).first()

    def get_by_email(self, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()

    def update(self, user_id: str, user_data: dict) -> User:
        user = self.get_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")

        for key, value in user_data.items():
            if value is not None:
                setattr(user, key, value)

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
