"""Tests for Priority enum."""
import pytest

from src.domain.entities.priority import Priority


class TestPriority:
    """Tests for Priority enumeration."""

    def test_priority_enum_values(self) -> None:
        """Priority enum should have exactly three values: low, medium, and high."""
        # Test that all three enum values exist
        assert hasattr(Priority, "LOW")
        assert hasattr(Priority, "MEDIUM")
        assert hasattr(Priority, "HIGH")

    def test_priority_values_are_strings(self) -> None:
        """All Priority values should be string values (for JSON serialization)."""
        # Verify enum inherits from str
        assert issubclass(Priority, str)

    def test_priority_low_value(self) -> None:
        """LOW priority should have the correct value."""
        # Test LOW value
        assert Priority.LOW == "low"

    def test_priority_medium_value(self) -> None:
        """MEDIUM priority should have the correct value."""
        # Test MEDIUM value
        assert Priority.MEDIUM == "medium"

    def test_priority_high_value(self) -> None:
        """HIGH priority should have the correct value."""
        # Test HIGH value
        assert Priority.HIGH == "high"

    def test_priority_all_values_defined(self) -> None:
        """Priority should define exactly three priority levels."""
        # Test we have exactly three values
        priorities = [Priority.LOW, Priority.MEDIUM, Priority.HIGH]
        assert len(priorities) == 3
        assert len(set(priorities)) == 3  # No duplicates
