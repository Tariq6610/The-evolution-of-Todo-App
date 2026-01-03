"""Integration tests for authentication endpoints."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from src.main import app
from src.domain.entities.user import User
from src.adapters.db.session import get_session


# Test database setup
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@pytest.fixture
def session():
    """Create a test database session."""
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def client(session):
    """Create a test client with a test database session."""
    def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


class TestRegisterEndpoint:
    """Test cases for the /register endpoint."""

    def test_register_new_user_successfully(self, client: TestClient) -> None:
        """Should register a new user and return user data."""
        response = client.post(
            "/auth/register",
            json={
                "email": "newuser@example.com",
                "password": "SecurePass123!",
                "full_name": "New User",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["full_name"] == "New User"
        assert data["is_active"] is True
        assert "id" in data
        assert "hashed_password" not in data  # Password should not be returned

    def test_register_with_duplicate_email(self, client: TestClient) -> None:
        """Should fail when registering with an existing email."""
        # Register first user
        client.post(
            "/auth/register",
            json={
                "email": "existing@example.com",
                "password": "SecurePass123!",
            },
        )

        # Try to register with same email
        response = client.post(
            "/auth/register",
            json={
                "email": "existing@example.com",
                "password": "AnotherPass123!",
            },
        )

        assert response.status_code == 400
        data = response.json()
        assert "already exists" in data["detail"].lower()

    def test_register_with_missing_password(self, client: TestClient) -> None:
        """Should fail when password is missing."""
        response = client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "full_name": "Test User",
            },
        )

        assert response.status_code == 422  # Validation error

    def test_register_with_invalid_email(self, client: TestClient) -> None:
        """Should fail with invalid email format."""
        response = client.post(
            "/auth/register",
            json={
                "email": "not-an-email",
                "password": "SecurePass123!",
            },
        )

        assert response.status_code == 422  # Validation error


class TestLoginEndpoint:
    """Test cases for the /login endpoint."""

    def test_login_successfully(self, client: TestClient) -> None:
        """Should login with valid credentials and return JWT token."""
        # Register user first
        client.post(
            "/auth/register",
            json={
                "email": "loginuser@example.com",
                "password": "LoginPass123!",
            },
        )

        # Login
        response = client.post(
            "/auth/login",
            data={
                "username": "loginuser@example.com",
                "password": "LoginPass123!",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_with_wrong_password(self, client: TestClient) -> None:
        """Should fail when password is incorrect."""
        # Register user first
        client.post(
            "/auth/register",
            json={
                "email": "user@example.com",
                "password": "CorrectPass123!",
            },
        )

        # Try to login with wrong password
        response = client.post(
            "/auth/login",
            data={
                "username": "user@example.com",
                "password": "WrongPass123!",
            },
        )

        assert response.status_code == 401
        data = response.json()
        assert "Incorrect email or password" in data["detail"]

    def test_login_with_nonexistent_user(self, client: TestClient) -> None:
        """Should fail when user does not exist."""
        response = client.post(
            "/auth/login",
            data={
                "username": "nonexistent@example.com",
                "password": "SomePass123!",
            },
        )

        assert response.status_code == 401
        data = response.json()
        assert "Incorrect email or password" in data["detail"]

    def test_login_without_password(self, client: TestClient) -> None:
        """Should fail when password field is missing."""
        response = client.post(
            "/auth/login",
            data={
                "username": "user@example.com",
            },
        )

        assert response.status_code == 422  # Validation error
