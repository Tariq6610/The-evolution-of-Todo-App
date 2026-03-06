#!/usr/bin/env python3
"""
Test script to verify user-specific task functionality.
"""

import os
import sys

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from uuid import uuid4

from sqlmodel import Session

from src.adapters.db.session import engine
from src.adapters.db.task_repository import SQLModelTaskRepository
from src.domain.entities.priority import Priority
from src.domain.services.todo_service import TodoService


def test_user_specific_functionality() -> None:
    """Test that user-specific functionality works correctly."""

    with Session(engine) as session:
        task_repo = SQLModelTaskRepository(session)
        todo_service = TodoService(task_repo)

        # Test user IDs
        user1_id = str(uuid4())
        user2_id = str(uuid4())

        print("Testing user-specific task functionality...")

        # Create tasks for user 1
        task1 = todo_service.create_task_for_user(
            title="User 1 Task",
            user_id=user1_id,
            description="Task for user 1",
            priority=Priority.HIGH,
        )
        print(f"Created task for user 1: {task1.title}")

        # Create another task for user 1
        task2 = todo_service.create_task_for_user(
            title="User 1 Second Task",
            user_id=user1_id,
            description="Another task for user 1",
            priority=Priority.MEDIUM,
        )
        print(f"Created second task for user 1: {task2.title}")

        # Create task for user 2
        task3 = todo_service.create_task_for_user(
            title="User 2 Task",
            user_id=user2_id,
            description="Task for user 2",
            priority=Priority.LOW,
        )
        print(f"Created task for user 2: {task3.title}")

        # Get tasks for user 1
        user1_tasks = todo_service.get_all_tasks_for_user(user_id=user1_id)
        print(f"User 1 has {len(user1_tasks)} tasks")

        # Get tasks for user 2
        user2_tasks = todo_service.get_all_tasks_for_user(user_id=user2_id)
        print(f"User 2 has {len(user2_tasks)} tasks")

        # Verify isolation
        if len(user1_tasks) == 2 and len(user2_tasks) == 1:
            print("✓ User isolation working correctly!")
        else:
            print("✗ User isolation failed!")

        # Test updating task for user
        updated_task = todo_service.update_task_for_user(
            task_id=task1.id,
            user_id=user1_id,
            title="Updated User 1 Task",
            description="Updated description for user 1",
        )
        print(f"Updated task: {updated_task.title}")

        # Try to update user 1's task with user 2's ID (should fail)
        try:
            todo_service.update_task_for_user(
                task_id=task1.id,
                user_id=user2_id,  # Wrong user ID
                title="Should fail",
            )
            print("✗ Security check failed - user 2 was able to update user 1's task")
        except ValueError:
            print("✓ Security check passed - user 2 cannot update user 1's task")

        print("All tests completed successfully!")


if __name__ == "__main__":
    test_user_specific_functionality()
