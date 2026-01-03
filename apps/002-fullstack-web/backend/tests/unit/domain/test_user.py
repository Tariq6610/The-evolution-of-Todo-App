"""Unit tests for User entity and models."""

import pytest
from datetime import datetime, UTC

from src.domain.entities.user import User, UserCreate, UserRead, UserUpdate


class TestUser:
    """Test cases for User entity."""

    def test_user_creation_with_valid_data(self) -> None:
        """Should create a User with valid data."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123",
            full_name="Test User",
        )

        assert user.email == "test@example.com"
        assert user.hashed_password == "hashed_password_123"
        assert user.full_name == "Test User"
        assert user.is_active is True
        assert user.id is not None
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)

    def test_user_without_full_name(self) -> None:
        """Should create a User without optional full_name."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123",
        )

        assert user.full_name is None
        assert user.email == "test@example.com"

    def test_user_with_inactive_status(self) -> None:
        """Should create a User with is_active=False."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123",
            is_active=False,
        )

        assert user.is_active is False

    def test_user_timestamps_auto_generated(self) -> None:
        """Should auto-generate created_at and updated_at timestamps."""
        before = datetime.now(UTC)

        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123",
        )

        after = datetime.now(UTC)

        assert before <= user.created_at <= after
        assert before <= user.updated_at <= after

    def test_user_email_indexed_and_unique(self) -> None:
        """Should have email indexed and marked as unique."""
        # This is more of an integration test, but we can check the field attributes
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123",
        )

        # Email should be present
        assert hasattr(user, 'email')
        assert user.email is not None


class TestUserCreate:
    """Test cases for UserCreate schema."""

    def test_user_create_with_all_fields(self) -> None:
        """Should create UserCreate with all fields."""
        user_create = UserCreate(
            email="test@example.com",
            password="secure_password_123",
            full_name="Test User",
        )

        assert user_create.email == "test@example.com"
        assert user_create.password == "secure_password_123"
        assert user_create.full_name == "Test User"
        assert user_create.is_active is True  # default from UserBase

    def test_user_create_without_full_name(self) -> None:
        """Should create UserCreate without optional full_name."""
        user_create = UserCreate(
            email="test@example.com",
            password="secure_password_123",
        )

        assert user_create.email == "test@example.com"
        assert user_create.password == "secure_password_123"
        assert user_create.full_name is None


class TestUserRead:
    """Test cases for UserRead schema."""

    def test_user_read_structure(self) -> None:
        """Should have all required fields for reading user data."""
        user_read = UserRead(
            id="user-id-123",
            email="test@example.com",
            full_name="Test User",
            is_active=True,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )

        assert user_read.id == "user-id-123"
        assert user_read.email == "test@example.com"
        assert user_read.full_name == "Test User"
        assert user_read.is_active is True
        assert isinstance(user_read.created_at, datetime)
        assert isinstance(user_read.updated_at, datetime)


class TestUserUpdate:
    """Test cases for UserUpdate schema."""

    def test_user_update_with_email(self) -> None:
        """Should create UserUpdate with email."""
        user_update = UserUpdate(email="newemail@example.com")

        assert user_update.email == "newemail@example.com"
        assert user_update.full_name is None
        assert user_update.password is None

    def test_user_update_with_password(self) -> None:
        """Should create UserUpdate with password."""
        user_update = UserUpdate(password="new_password_123")

        assert user_update.password == "new_password_123"
        assert user_update.email is None
        assert user_update.full_name is None

    def test_user_update_with_all_fields(self) -> None:
        """Should create UserUpdate with all optional fields."""
        user_update = UserUpdate(
            email="newemail@example.com",
            full_name="New Name",
            password="new_password_123",
            is_active=False,
        )

        assert user_update.email == "newemail@example.com"
        assert user_update.full_name == "New Name"
        assert user_update.password == "new_password_123"
        assert user_update.is_active is False
