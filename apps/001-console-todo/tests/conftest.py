"""
Pytest fixtures for Todo App tests.

Provides reusable fixtures for test isolation and setup.
"""
import pytest
from typing import Generator


@pytest.fixture
def sample_task_data() -> dict:
    """Provide sample task data for testing."""
    return {
        "id": "test-task-001",
        "title": "Test Task",
        "description": "A task for testing purposes",
        "status": "pending",
        "priority": "medium",
        "tags": ["test"],
    }


@pytest.fixture
def sample_tasks_data() -> Generator[list[dict], None, None]:
    """Provide multiple sample tasks for testing."""
    tasks = [
        {
            "id": "task-001",
            "title": "First Task",
            "description": "First sample task",
            "status": "pending",
            "priority": "low",
            "tags": ["work"],
        },
        {
            "id": "task-002",
            "title": "Second Task",
            "description": "Second sample task",
            "status": "completed",
            "priority": "high",
            "tags": ["urgent"],
        },
        {
            "id": "task-003",
            "title": "Third Task",
            "description": "Third sample task",
            "status": "pending",
            "priority": "medium",
            "tags": [],
        },
    ]
    for task in tasks:
        yield task
