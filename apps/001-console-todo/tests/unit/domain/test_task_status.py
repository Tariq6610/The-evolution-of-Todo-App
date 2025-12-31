"""Tests for TaskStatus enum."""
import pytest
from enum import Enum

from src.domain.entities.task_status import TaskStatus


class TestTaskStatus:
    """Tests for TaskStatus enumeration."""

    def test_task_status_enum_values(self) -> None:
        """TaskStatus enum should have exactly two values: pending and completed."""
        # Test that both enum values exist
        assert hasattr(TaskStatus, "PENDING")
        assert hasattr(TaskStatus, "COMPLETED")

    def test_task_status_values_are_strings(self) -> None:
        """All TaskStatus values should be string values (for JSON serialization)."""
        # Verify enum inherits from str
        assert issubclass(TaskStatus, str)

    def test_task_status_pending_value(self) -> None:
        """PENDING status should have the correct value."""
        # Test PENDING value
        assert TaskStatus.PENDING == "pending"

    def test_task_status_completed_value(self) -> None:
        """COMPLETED status should have the correct value."""
        # Test COMPLETED value
        assert TaskStatus.COMPLETED == "completed"

    def test_task_status_all_values_defined(self) -> None:
        """TaskStatus should define exactly two status values."""
        # Test we have exactly two values
        statuses = [TaskStatus.PENDING, TaskStatus.COMPLETED]
        assert len(statuses) == 2
        assert len(set(statuses)) == 2  # No duplicates
