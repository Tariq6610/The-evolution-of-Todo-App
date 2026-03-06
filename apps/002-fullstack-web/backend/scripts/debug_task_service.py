#!/usr/bin/env python3
"""
Debug script to test the get_all_tasks_for_user functionality
"""

import os
import sys

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session

from src.adapters.db.session import engine
from src.adapters.db.task_repository import SQLModelTaskRepository
from src.domain.services.todo_service import TodoService


def test_get_all_tasks_for_user() -> None:
    """Test the get_all_tasks_for_user method that's causing the error."""

    with Session(engine) as session:
        task_repo = SQLModelTaskRepository(session)
        todo_service = TodoService(task_repo)

        # Test with the actual user ID we created
        test_user_id = "6b5bacbd-0247-4524-8cef-c411534a757f"  # From our previous run

        print("Testing get_all_tasks_for_user method...")

        try:
            # Test without filters first
            all_tasks = todo_service.get_all_tasks_for_user(user_id=test_user_id)
            print(f"✓ Successfully retrieved {len(all_tasks)} tasks without filters")

            # Test with filters
            filtered_tasks = todo_service.get_all_tasks_for_user(
                user_id=test_user_id, status="PENDING"
            )
            print(f"✓ Successfully retrieved {len(filtered_tasks)} pending tasks")

            filtered_tasks2 = todo_service.get_all_tasks_for_user(
                user_id=test_user_id, priority="HIGH"
            )
            print(f"✓ Successfully retrieved {len(filtered_tasks2)} high priority tasks")

            print("✓ All tests passed - the service method is working correctly")

        except Exception as e:
            print(f"✗ Error in get_all_tasks_for_user: {e}")
            import traceback

            traceback.print_exc()


if __name__ == "__main__":
    test_get_all_tasks_for_user()
