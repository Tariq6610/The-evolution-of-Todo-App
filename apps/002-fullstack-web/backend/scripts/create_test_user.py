#!/usr/bin/env python3
"""
Script to create a test user for the dashboard.
Run from the backend directory: python scripts/create_test_user.py
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
from src.adapters.db.user_repository import SQLUserRepository


def create_test_user():
    """Create a test user for dashboard demonstration."""

    # Create tables if they don't exist
    init_db()

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    user_email = "tariq3@gmail.com"

    with Session(engine) as session:
        # Check if user exists
        user = session.exec(select(User).where(User.email == user_email)).first()

        if user:
            print(f"User {user_email} already exists.")
            return user

        # Create user
        hashed_password = pwd_context.hash("testpassword123")
        new_user = User(
            email=user_email,
            full_name="Tariq Test User",
            hashed_password=hashed_password
        )

        user_repo = SQLUserRepository(session)
        created_user = user_repo.create(new_user)

        print(f"Created user: {created_user.email} with ID: {created_user.id}")
        return created_user


if __name__ == "__main__":
    create_test_user()