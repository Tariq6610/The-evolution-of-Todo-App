"""Tests for MenuSystem CLI utilities."""
import sys
import io
from unittest.mock import patch

from src.adapters.cli.menu_system import MenuSystem
from src.domain.entities.priority import Priority


class TestMenuSystem:
    """Tests for MenuSystem utility."""

    def test_show_menu_displays_options(self, capsys) -> None:
        """MenuSystem.show_menu() should display numbered options."""
        menu = MenuSystem()
        menu.show_menu()
        captured = capsys.readouterr()
        content = captured.out
        assert "=== Todo Menu ===" in content
        assert "1. Add Task" in content
        assert "2. View All Tasks" in content
        assert "3. Update Task" in content
        assert "4. Delete Task" in content
        assert "5. Mark Complete/Incomplete" in content
        assert "0. Exit" in content

    @patch("builtins.input", return_value="2")
    def test_get_user_choice_returns_valid_number(self, mock_input) -> None:
        """MenuSystem.get_user_choice() should return valid choice."""
        menu = MenuSystem()
        choice = menu.get_user_choice()
        assert choice == 2
        mock_input.assert_called_once()

    @patch("builtins.input", side_effect=["abc", "2"])
    def test_get_user_choice_validates_integer_input(self, mock_input) -> None:
        """MenuSystem.get_user_choice() should validate integer input."""
        menu = MenuSystem()
        choice = menu.get_user_choice()
        assert choice == 2
        assert mock_input.call_count == 2

    @patch("builtins.input", side_effect=["10", "2"])
    def test_get_user_choice_validates_range(self, mock_input) -> None:
        """MenuSystem.get_user_choice() should validate range 0-5."""
        menu = MenuSystem()
        choice = menu.get_user_choice()
        assert choice == 2
        assert mock_input.call_count == 2

    @patch("builtins.input", return_value="Valid Task Title")
    def test_get_task_title_input_returns_title(self, mock_input) -> None:
        """MenuSystem.get_task_title_input() should return non-empty title."""
        menu = MenuSystem()
        title = menu.get_task_title_input()
        assert title == "Valid Task Title"
        mock_input.assert_called_once()

    @patch("builtins.input", side_effect=["", "Valid Title"])
    def test_get_task_title_validates_non_empty(self, mock_input) -> None:
        """MenuSystem.get_task_title_input() should validate non-empty."""
        menu = MenuSystem()
        title = menu.get_task_title_input()
        assert title == "Valid Title"
        assert mock_input.call_count == 2

    @patch("builtins.input", return_value="Task Description")
    def test_get_task_description_input_returns_description(self, mock_input) -> None:
        """MenuSystem.get_task_description_input() should return description."""
        menu = MenuSystem()
        description = menu.get_task_description_input()
        assert description == "Task Description"

    @patch("builtins.input", return_value="")
    def test_get_task_description_returns_none_when_skipped(self, mock_input) -> None:
        """MenuSystem.get_task_description_input() should return None when skipped."""
        menu = MenuSystem()
        description = menu.get_task_description_input()
        assert description is None

    @patch("builtins.input", return_value="")
    def test_get_priority_selection_returns_default(self, mock_input) -> None:
        """MenuSystem.get_priority_selection() should return MEDIUM when skipped."""
        menu = MenuSystem()
        priority = menu.get_priority_selection()
        assert priority == Priority.MEDIUM

    @patch("builtins.input", return_value="1")
    def test_get_priority_selection_returns_low(self, mock_input) -> None:
        """MenuSystem.get_priority_selection() should return LOW."""
        menu = MenuSystem()
        priority = menu.get_priority_selection()
        assert priority == Priority.LOW

    @patch("builtins.input", return_value="2")
    def test_get_priority_selection_returns_medium(self, mock_input) -> None:
        """MenuSystem.get_priority_selection() should return MEDIUM."""
        menu = MenuSystem()
        priority = menu.get_priority_selection()
        assert priority == Priority.MEDIUM

    @patch("builtins.input", return_value="3")
    def test_get_priority_selection_returns_high(self, mock_input) -> None:
        """MenuSystem.get_priority_selection() should return HIGH."""
        menu = MenuSystem()
        priority = menu.get_priority_selection()
        assert priority == Priority.HIGH

    @patch("builtins.input", return_value="")
    def test_get_tags_input_returns_empty_list_when_skipped(self, mock_input) -> None:
        """MenuSystem.get_tags_input() should return empty list when skipped."""
        menu = MenuSystem()
        tags = menu.get_tags_input()
        assert tags == []

    @patch("builtins.input", return_value="work,urgent,personal")
    def test_get_tags_input_parses_comma_separated(self, mock_input) -> None:
        """MenuSystem.get_tags_input() should parse comma-separated tags."""
        menu = MenuSystem()
        tags = menu.get_tags_input()
        assert tags == ["work", "urgent", "personal"]

    @patch("builtins.input", return_value="work, urgent, personal")
    def test_get_tags_input_strips_whitespace(self, mock_input) -> None:
        """MenuSystem.get_tags_input() should strip whitespace from tags."""
        menu = MenuSystem()
        tags = menu.get_tags_input()
        assert tags == ["work", "urgent", "personal"]

    @patch("builtins.input", return_value="task-123")
    def test_get_task_id_input_returns_id(self, mock_input) -> None:
        """MenuSystem.get_task_id_input() should return task ID."""
        menu = MenuSystem()
        task_id = menu.get_task_id_input()
        assert task_id == "task-123"

    @patch("builtins.input", return_value="y")
    def test_get_confirmation_returns_true_for_yes(self, mock_input) -> None:
        """MenuSystem.get_confirmation() should return True for 'y'."""
        menu = MenuSystem()
        result = menu.get_confirmation("Confirm?")
        assert result is True

    @patch("builtins.input", return_value="yes")
    def test_get_confirmation_returns_true_for_yes_full(self, mock_input) -> None:
        """MenuSystem.get_confirmation() should return True for 'yes'."""
        menu = MenuSystem()
        result = menu.get_confirmation("Confirm?")
        assert result is True

    @patch("builtins.input", return_value="n")
    def test_get_confirmation_returns_false_for_no(self, mock_input) -> None:
        """MenuSystem.get_confirmation() should return False for 'n'."""
        menu = MenuSystem()
        result = menu.get_confirmation("Confirm?")
        assert result is False

    @patch("builtins.input", return_value="no")
    def test_get_confirmation_returns_false_for_no_full(self, mock_input) -> None:
        """MenuSystem.get_confirmation() should return False for 'no'."""
        menu = MenuSystem()
        result = menu.get_confirmation("Confirm?")
        assert result is False
