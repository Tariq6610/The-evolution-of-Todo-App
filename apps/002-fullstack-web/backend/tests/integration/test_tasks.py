"""Integration tests for task endpoints with authentication."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from src.main import app
from src.domain.entities.user import User, UserCreate
from src.domain.entities.task import Task
from src.adapters.db.session import get_session
from src.adapters.db.user_repository import SQLUserRepository
from src.adapters.security.password import get_password_hash
from src.adapters.security.jwt import create_access_token


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


@pytest.fixture
def auth_headers(client: TestClient, session: Session) -> dict[str, str]:
    """Create a test user and return authentication headers."""
    user_repo = SQLUserRepository(session)
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("TestPass123!"),
        full_name="Test User",
    )
    user_repo.create(user)

    token = create_access_token(data={"sub": user.id})
    return {"Authorization": f"Bearer {token}"}


class TestCreateTask:
    """Test cases for creating tasks."""

    def test_create_task_successfully(self, client: TestClient, auth_headers: dict) -> None:
        """Should create a new task and return task data."""
        response = client.post(
            "/tasks",
            json={
                "title": "New Task",
                "description": "Task description",
                "priority": "HIGH",
                "tags": ["work", "urgent"],
            },
            headers=auth_headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "New Task"
        assert data["description"] == "Task description"
        assert data["priority"] == "HIGH"
        assert data["status"] == "PENDING"
        assert "id" in data
        assert "user_id" in data

    def test_create_task_without_auth(self, client: TestClient) -> None:
        """Should fail when not authenticated."""
        response = client.post(
            "/tasks",
            json={"title": "Unauthorized Task"},
        )

        assert response.status_code == 401

    def test_create_task_with_minimal_data(self, client: TestClient, auth_headers: dict) -> None:
        """Should create task with only title."""
        response = client.post(
            "/tasks",
            json={"title": "Minimal Task"},
            headers=auth_headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Minimal Task"
        assert data["description"] is None
        assert data["priority"] == "MEDIUM"  # default
        assert data["status"] == "PENDING"  # default


class TestReadTasks:
    """Test cases for reading tasks."""

    def test_list_tasks_successfully(self, client: TestClient, auth_headers: dict) -> None:
        """Should return list of user's tasks."""
        # Create tasks
        client.post(
            "/tasks",
            json={"title": "Task 1"},
            headers=auth_headers,
        )
        client.post(
            "/tasks",
            json={"title": "Task 2"},
            headers=auth_headers,
        )

        # List tasks
        response = client.get("/tasks", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_list_empty_tasks(self, client: TestClient, auth_headers: dict) -> None:
        """Should return empty list when user has no tasks."""
        response = client.get("/tasks", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data == []

    def test_list_tasks_without_auth(self, client: TestClient) -> None:
        """Should fail when not authenticated."""
        response = client.get("/tasks")

        assert response.status_code == 401


class TestUpdateTask:
    """Test cases for updating tasks."""

    def test_update_task_successfully(self, client: TestClient, auth_headers: dict) -> None:
        """Should update an existing task."""
        # Create task
        create_response = client.post(
            "/tasks",
            json={"title": "Original Title"},
            headers=auth_headers,
        )
        task_id = create_response.json()["id"]

        # Update task
        update_response = client.patch(
            f"/tasks/{task_id}",
            json={
                "title": "Updated Title",
                "priority": "HIGH",
            },
            headers=auth_headers,
        )

        assert update_response.status_code == 200
        data = update_response.json()
        assert data["title"] == "Updated Title"
        assert data["priority"] == "HIGH"

    def test_update_task_without_auth(self, client: TestClient, auth_headers: dict) -> None:
        """Should fail when not authenticated."""
        # Create task
        create_response = client.post(
            "/tasks",
            json={"title": "Task"},
            headers=auth_headers,
        )
        task_id = create_response.json()["id"]

        # Try to update without auth
        response = client.patch(
            f"/tasks/{task_id}",
            json={"title": "Updated"},
        )

        assert response.status_code == 401

    def test_update_nonexistent_task(self, client: TestClient, auth_headers: dict) -> None:
        """Should fail when task does not exist."""
        response = client.patch(
            "/tasks/nonexistent-id",
            json={"title": "Updated"},
            headers=auth_headers,
        )

        assert response.status_code == 404


class TestDeleteTask:
    """Test cases for deleting tasks."""

    def test_delete_task_successfully(self, client: TestClient, auth_headers: dict) -> None:
        """Should delete an existing task."""
        # Create task
        create_response = client.post(
            "/tasks",
            json={"title": "To Delete"},
            headers=auth_headers,
        )
        task_id = create_response.json()["id"]

        # Delete task
        delete_response = client.delete(f"/tasks/{task_id}", headers=auth_headers)

        assert delete_response.status_code == 204

        # Verify task is deleted
        list_response = client.get("/tasks", headers=auth_headers)
        tasks = list_response.json()
        assert len(tasks) == 0

    def test_delete_task_without_auth(self, client: TestClient, auth_headers: dict) -> None:
        """Should fail when not authenticated."""
        # Create task
        create_response = client.post(
            "/tasks",
            json={"title": "Task"},
            headers=auth_headers,
        )
        task_id = create_response.json()["id"]

        # Try to delete without auth
        response = client.delete(f"/tasks/{task_id}")

        assert response.status_code == 401

    def test_delete_nonexistent_task(self, client: TestClient, auth_headers: dict) -> None:
        """Should fail when task does not exist."""
        response = client.delete("/tasks/nonexistent-id", headers=auth_headers)

        assert response.status_code == 404


class TestToggleStatus:
    """Test cases for toggling task status."""

    def test_toggle_status_from_pending(self, client: TestClient, auth_headers: dict) -> None:
        """Should toggle task from PENDING to COMPLETED."""
        # Create task
        create_response = client.post(
            "/tasks",
            json={"title": "Toggle Me"},
            headers=auth_headers,
        )
        task_id = create_response.json()["id"]

        # Toggle status
        response = client.patch(f"/tasks/{task_id}/toggle-status", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "COMPLETED"

    def test_toggle_status_from_completed(self, client: TestClient, auth_headers: dict) -> None:
        """Should toggle task from COMPLETED to PENDING."""
        # Create and complete task
        create_response = client.post(
            "/tasks",
            json={"title": "Toggle Back"},
            headers=auth_headers,
        )
        task_id = create_response.json()["id"]

        client.patch(f"/tasks/{task_id}/toggle-status", headers=auth_headers)

        # Toggle again
        response = client.patch(f"/tasks/{task_id}/toggle-status", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "PENDING"


class TestUserIsolation:
    """Test cases for multi-user data isolation."""

    def test_users_cannot_access_other_users_tasks(self, client: TestClient, session: Session) -> None:
        """Should prevent user A from accessing user B's tasks."""
        # Create user A
        user_a = User(
            email="usera@example.com",
            hashed_password=get_password_hash("PassA123!"),
        )
        user_repo = SQLUserRepository(session)
        user_repo.create(user_a)
        token_a = create_access_token(data={"sub": user_a.id})
        headers_a = {"Authorization": f"Bearer {token_a}"}

        # Create task for user A
        create_response = client.post(
            "/tasks",
            json={"title": "User A's Task"},
            headers=headers_a,
        )
        task_id = create_response.json()["id"]

        # Create user B
        user_b = User(
            email="userb@example.com",
            hashed_password=get_password_hash("PassB123!"),
        )
        user_repo.create(user_b)
        token_b = create_access_token(data={"sub": user_b.id})
        headers_b = {"Authorization": f"Bearer {token_b}"}

        # User B tries to access user A's task
        response = client.get(f"/tasks/{task_id}", headers=headers_b)

        assert response.status_code == 404  # Not found for user B

    def test_users_cannot_update_other_users_tasks(self, client: TestClient, session: Session) -> None:
        """Should prevent user A from updating user B's tasks."""
        # Create two users
        user_repo = SQLUserRepository(session)
        user_a = User(
            email="usera@example.com",
            hashed_password=get_password_hash("PassA123!"),
        )
        user_repo.create(user_a)
        token_a = create_access_token(data={"sub": user_a.id})
        headers_a = {"Authorization": f"Bearer {token_a}"}

        user_b = User(
            email="userb@example.com",
            hashed_password=get_password_hash("PassB123!"),
        )
        user_repo.create(user_b)
        token_b = create_access_token(data={"sub": user_b.id})
        headers_b = {"Authorization": f"Bearer {token_b}"}

        # User A creates task
        create_response = client.post(
            "/tasks",
            json={"title": "User A's Task"},
            headers=headers_a,
        )
        task_id = create_response.json()["id"]

        # User B tries to update user A's task
        response = client.patch(
            f"/tasks/{task_id}",
            json={"title": "Updated by User B"},
            headers=headers_b,
        )

        assert response.status_code == 404

    def test_users_cannot_delete_other_users_tasks(self, client: TestClient, session: Session) -> None:
        """Should prevent user A from deleting user B's tasks."""
        # Create two users
        user_repo = SQLUserRepository(session)
        user_a = User(
            email="usera@example.com",
            hashed_password=get_password_hash("PassA123!"),
        )
        user_repo.create(user_a)
        token_a = create_access_token(data={"sub": user_a.id})
        headers_a = {"Authorization": f"Bearer {token_a}"}

        user_b = User(
            email="userb@example.com",
            hashed_password=get_password_hash("PassB123!"),
        )
        user_repo.create(user_b)
        token_b = create_access_token(data={"sub": user_b.id})
        headers_b = {"Authorization": f"Bearer {token_b}"}

        # User A creates task
        create_response = client.post(
            "/tasks",
            json={"title": "User A's Task"},
            headers=headers_a,
        )
        task_id = create_response.json()["id"]

        # User B tries to delete user A's task
        response = client.delete(f"/tasks/{task_id}", headers=headers_b)

        assert response.status_code == 404
