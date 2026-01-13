#!/usr/bin/env python3
"""
Script to create test tasks for dashboard testing.
Run from the backend directory: python scripts/create_test_tasks.py
"""

import asyncio
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session, select
from passlib.context import CryptContext
from src.adapters.db.session import engine, init_db
from src.domain.entities.user import User
from src.adapters.db.task_repository import TaskTable


async def create_test_tasks():
    """Create test tasks for dashboard demonstration."""

    # Create tables if they don't exist
    init_db()

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    user_email = "admin@gmail.com"

    with Session(engine) as session:
        # Check if user exists
        user = session.exec(select(User).where(User.email == user_email)).first()

        if not user:
            print(f"User {user_email} not found. Please register first.")
            return

        print(f"Using user: {user.email}")

        # Check if tasks already exist
        existing_tasks = session.exec(select(TaskTable).where(TaskTable.user_id == user.id)).all()
        if existing_tasks:
            print(f"Found {len(existing_tasks)} existing tasks. Clearing them...")
            for task in existing_tasks:
                session.delete(task)
            session.commit()

        # Create test tasks
        test_tasks = [
            # High priority tasks
            TaskTable(
                title="Complete project proposal",
                description="Write and submit the quarterly project proposal with budget estimates",
                priority="high",
                status="pending",
                tags="work,important,q1",
                user_id=user.id
            ),
            TaskTable(
                title="Review security audit",
                description="Review the security audit report and address critical vulnerabilities",
                priority="high",
                status="pending",
                tags="security,urgent",
                user_id=user.id
            ),
            TaskTable(
                title="Client meeting preparation",
                description="Prepare presentation for Monday's client meeting",
                priority="high",
                status="completed",
                tags="client,presentation",
                user_id=user.id
            ),

            # Medium priority tasks
            TaskTable(
                title="Update documentation",
                description="Update API documentation with new endpoints",
                priority="medium",
                status="pending",
                tags="docs,api",
                user_id=user.id
            ),
            TaskTable(
                title="Code review for PR #42",
                description="Review the new feature pull request",
                priority="medium",
                status="pending",
                tags="code-review,backend",
                user_id=user.id
            ),
            TaskTable(
                title="Write unit tests",
                description="Add unit tests for the new authentication module",
                priority="medium",
                status="completed",
                tags="testing,auth",
                user_id=user.id
            ),
            TaskTable(
                title="Update dependencies",
                description="Update npm packages to latest versions",
                priority="medium",
                status="pending",
                tags="maintenance,frontend",
                user_id=user.id
            ),

            # Low priority tasks
            TaskTable(
                title="Clean up old logs",
                description="Archive and remove logs older than 30 days",
                priority="low",
                status="pending",
                tags="maintenance,devops",
                user_id=user.id
            ),
            TaskTable(
                title="Add comments to legacy code",
                description="Add documentation comments to the payment processing module",
                priority="low",
                status="completed",
                tags="docs,legacy",
                user_id=user.id
            ),
            TaskTable(
                title="Organize desktop files",
                description="Clean up and organize files on development machine",
                priority="low",
                status="pending",
                tags="personal,organization",
                user_id=user.id
            ),
            TaskTable(
                title="Update email signature",
                description="Update email signature with new title and contact info",
                priority="low",
                status="pending",
                tags="personal,admin",
                user_id=user.id
            ),

            # Additional tasks for variety
            TaskTable(
                title="Learn new framework",
                description="Complete the online course on Rust programming",
                priority="medium",
                status="pending",
                tags="learning,rust",
                user_id=user.id
            ),
            TaskTable(
                title="Backup database",
                description="Create a full backup of the production database",
                priority="high",
                status="completed",
                tags="backup,devops,critical",
                user_id=user.id
            ),
            TaskTable(
                title="Team lunch planning",
                description="Coordinate with team for this month's team building lunch",
                priority="low",
                status="pending",
                tags="team,social",
                user_id=user.id
            ),
            TaskTable(
                title="Performance optimization",
                description="Optimize database queries causing slow page loads",
                priority="medium",
                status="pending",
                tags="performance,database",
                user_id=user.id
            ),
        ]

        for task in test_tasks:
            session.add(task)

        session.commit()
        print(f"Created {len(test_tasks)} test tasks!")

        # Print summary
        all_tasks = session.exec(select(TaskTable).where(TaskTable.user_id == user.id)).all()
        completed = sum(1 for t in all_tasks if t.status == "COMPLETED")
        pending = sum(1 for t in all_tasks if t.status == "PENDING")
        high = sum(1 for t in all_tasks if t.priority == "HIGH")
        medium = sum(1 for t in all_tasks if t.priority == "MEDIUM")
        low = sum(1 for t in all_tasks if t.priority == "LOW")

        print(f"\nTask Summary:")
        print(f"  Total: {len(all_tasks)}")
        print(f"  Completed: {completed}")
        print(f"  Pending: {pending}")
        print(f"  High Priority: {high}")
        print(f"  Medium Priority: {medium}")
        print(f"  Low Priority: {low}")


if __name__ == "__main__":
    asyncio.run(create_test_tasks())
