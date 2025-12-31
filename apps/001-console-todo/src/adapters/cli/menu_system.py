"""MenuSystem utility for CLI interactions.

Handles menu display, input collection, and validation.
Phase I implementation for console-based interaction.
"""

from src.domain.entities.priority import Priority


class MenuSystem:
    """
    CLI menu system for user interactions.

    Handles:
    - Menu display
    - User choice validation
    - Task input collection with validation
    """

    def show_menu(self) -> None:
        """Display numbered menu options."""
        print("\n=== Todo Menu ===")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Complete/Incomplete")
        print("0. Exit")

    def get_user_choice(self) -> int:
        """
        Get and validate user menu choice.

        Returns:
            Validated menu choice (0-5)

        Raises:
            ValueError: If user enters non-integer or invalid range
        """
        while True:
            try:
                choice = input("Enter choice (0-5): ").strip()
                choice_int = int(choice)
                if 0 <= choice_int <= 5:
                    return choice_int
                print("Invalid choice. Please enter 0-5.")
            except ValueError:
                print("Please enter a number.")

    def get_task_title_input(self) -> str:
        """
        Get task title with validation.

        Returns:
            Validated task title (non-empty, non-whitespace)

        Raises:
            ValueError: If user enters empty or whitespace-only title
        """
        while True:
            title = input("Enter task title: ").strip()
            if title:
                return title
            print("Title cannot be empty. Please enter a valid title.")

    def get_task_description_input(self) -> str | None:
        """
        Get optional task description.

        Returns:
            Description string if provided, None if skipped
        """
        prompt = "Enter task description (optional, press Enter to skip): "
        description = input(prompt).strip()
        return description if description else None

    def get_priority_selection(self) -> Priority:
        """
        Get priority selection from user.

        Returns:
            Selected Priority (LOW, MEDIUM, HIGH)
        """
        print("\nSelect priority:")
        print("1. Low")
        print("2. Medium (default)")
        print("3. High")

        while True:
            choice = input("\nEnter choice (1-3) or press Enter for default: ").strip()
            if not choice:
                return Priority.MEDIUM

            try:
                choice_int = int(choice)
                if choice_int == 1:
                    return Priority.LOW
                elif choice_int == 2:
                    return Priority.MEDIUM
                elif choice_int == 3:
                    return Priority.HIGH
                else:
                    print("Invalid choice. Please enter 1, 2, or 3.")
            except ValueError:
                print("Please enter a number (1, 2, or 3).")

    def get_tags_input(self) -> list[str]:
        """
        Get tags input from user.

        Returns:
            List of tag strings (empty list if none provided)
        """
        prompt = "Enter tags (comma-separated, optional, press Enter to skip): "
        tags_input = input(prompt).strip()
        if not tags_input:
            return []

        # Parse comma-separated tags and strip whitespace
        tags = [tag.strip() for tag in tags_input.split(",")]
        # Remove empty strings
        return [tag for tag in tags if tag]

    def get_task_id_input(self) -> str:
        """
        Get task ID from user.

        Returns:
            Task ID string
        """
        return input("Enter task ID: ").strip()

    def get_confirmation(self, prompt: str) -> bool:
        """
        Get yes/no confirmation from user.

        Args:
            prompt: Confirmation question to display

        Returns:
            True if user confirms (yes/y), False otherwise
        """
        while True:
            response = input(f"{prompt} (y/n): ").strip().lower()
            if response in ("y", "yes"):
                return True
            elif response in ("n", "no"):
                return False
            print("Please enter 'y' or 'n'.")
