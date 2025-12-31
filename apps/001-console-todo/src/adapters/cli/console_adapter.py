"""ConsoleAdapter for CLI presentation.

Handles CLI presentation and user interaction flows.
Phase I implementation for console-based todo app.
"""

from src.adapters.cli.menu_system import MenuSystem
from src.domain.entities.priority import Priority
from src.domain.entities.task import Task
from src.domain.services.todo_service import TodoService


class ConsoleAdapter:
    """
    Console presentation adapter for todo application.

    Coordinates between user CLI interactions and TodoService.
    Implements all user flows defined in requirements.
    """

    def __init__(self, service: TodoService, menu: MenuSystem) -> None:
        """
        Initialize ConsoleAdapter with dependencies.

        Args:
            service: TodoService business logic
            menu: MenuSystem for CLI interactions
        """
        self.service = service
        self.menu = menu

    def add_task_flow(self) -> None:
        """
        Collect inputs and create a new task.

        Flow:
        1. Get title (required, validated)
        2. Get description (optional)
        3. Get priority (optional, default: MEDIUM)
        4. Get tags (optional, comma-separated)
        5. Create task via service
        6. Display success message
        """
        print("\n--- Add New Task ---")

        title = self.menu.get_task_title_input()
        description = self.menu.get_task_description_input()
        priority = self.menu.get_priority_selection()
        tags = self.menu.get_tags_input()

        try:
            task = self.service.create_task(
                title=title,
                description=description,
                priority=priority,
                tags=tags,
            )
            print("\n✓ Task created successfully!")
            print(f"  ID: {task.id}")
            print(f"  Title: {task.title}")
        except ValueError as e:
            print(f"\n✗ Error creating task: {e}")

    def view_all_tasks_flow(self) -> None:
        """
        Display all tasks with task count.

        Flow:
        1. Retrieve all tasks from service
        2. Display task count
        3. List all tasks with details
        4. Wait for user to press Enter
        """
        print("\n--- View All Tasks ---")

        tasks = self.service.get_all_tasks()
        task_count = len(tasks)

        if task_count == 0:
            print("\nNo tasks found.")
        else:
            print(f"\nTotal tasks: {task_count}")
            print("\n" + "-" * 60)
            for task in tasks:
                self._display_task(task)
                print("-" * 60)

        input("\nPress Enter to continue...")

    def _display_task(self, task: Task) -> None:
        """Display a single task with all details."""
        status_symbol = "✓" if task.status.value == "completed" else "○"
        priority_display = task.priority.value.upper()

        print(f"\n{status_symbol} [{task.id}] {task.title}")
        print(f"   Priority: {priority_display} | Status: {task.status.value}")

        if task.description:
            print(f"   Description: {task.description}")

        if task.tags:
            print(f"   Tags: {', '.join(task.tags)}")

        print(f"   Created: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")

    def update_task_flow(self) -> None:
        """
        Update an existing task.

        Flow:
        1. Get task ID
        2. Show current task details
        3. Get new values (optional, skip to keep current)
        4. Update task via service
        5. Display success message
        """
        print("\n--- Update Task ---")
        task_id = self.menu.get_task_id_input()

        try:
            # Get current task to display
            current_task = self.service.get_all_tasks()
            task = next((t for t in current_task if t.id == task_id), None)

            if task is None:
                print(f"\n✗ Task with ID '{task_id}' not found.")
                return

            print(f"\nCurrent task: {task.title}")
            print("Press Enter to skip any field you don't want to change.")

            default_title = task.title
            new_title = input(f"New title [{default_title}]: ").strip() or None

            default_desc = task.description or "none"
            prompt = f"New description [{default_desc}]: "
            new_description = input(prompt).strip() or None

            print("\nSelect priority:")
            print("1. Low")
            print("2. Medium")
            print("3. High")
            default_priority = task.priority.value
            prompt = "\nEnter choice (1-3) or Enter: "
            default_display = f"[{default_priority}]" if default_priority else ""
            full_prompt = prompt + default_display
            priority_choice = input(full_prompt).strip()
            new_priority = None
            if priority_choice:
                if priority_choice == "1":
                    new_priority = Priority.LOW
                elif priority_choice == "2":
                    new_priority = Priority.MEDIUM
                elif priority_choice == "3":
                    new_priority = Priority.HIGH

            tags_display = ", ".join(task.tags) or "none"
            tags_input = input(f"New tags [{tags_display}]: ").strip() or None
            new_tags = None
            if tags_input:
                new_tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]

            updated_task = self.service.update_task(
                task_id=task_id,
                title=new_title,
                description=new_description,
                priority=new_priority,
                tags=new_tags,
            )

            print("\n✓ Task updated successfully!")
            print(f"  ID: {updated_task.id}")
            print(f"  Title: {updated_task.title}")

        except ValueError as e:
            print(f"\n✗ Error updating task: {e}")

    def delete_task_flow(self) -> None:
        """
        Delete a task with confirmation.

        Flow:
        1. Get task ID
        2. Show task details
        3. Confirm deletion
        4. Delete task if confirmed
        5. Display success message
        """
        print("\n--- Delete Task ---")
        task_id = self.menu.get_task_id_input()

        try:
            # Find task to display
            tasks = self.service.get_all_tasks()
            task = next((t for t in tasks if t.id == task_id), None)

            if task is None:
                print(f"\n✗ Task with ID '{task_id}' not found.")
                return

            print(f"\nTask: {task.title}")
            if task.description:
                print(f"Description: {task.description}")

            if self.menu.get_confirmation("Are you sure you want to delete this task?"):
                self.service.delete_task(task_id)
                print("\n✓ Task deleted successfully.")
            else:
                print("\n✗ Deletion cancelled.")

        except ValueError as e:
            print(f"\n✗ Error deleting task: {e}")

    def toggle_status_flow(self) -> None:
        """
        Toggle task completion status.

        Flow:
        1. Get task ID
        2. Show current status
        3. Toggle status via service
        4. Display new status
        """
        print("\n--- Toggle Task Status ---")
        task_id = self.menu.get_task_id_input()

        try:
            # Find task
            tasks = self.service.get_all_tasks()
            task = next((t for t in tasks if t.id == task_id), None)

            if task is None:
                print(f"\n✗ Task with ID '{task_id}' not found.")
                return

            print(f"\nTask: {task.title}")
            print(f"Current status: {task.status.value}")

            updated_task = self.service.toggle_task_status(task_id)

            print("\n✓ Task status updated!")
            print(f"  New status: {updated_task.status.value}")

        except ValueError as e:
            print(f"\n✗ Error toggling task status: {e}")

    def show_exit_confirmation(self) -> bool:
        """
        Show exit confirmation dialog.

        Returns:
            True if user confirms exit, False otherwise
        """
        return self.menu.get_confirmation("Are you sure you want to exit?")

    def show_goodbye(self) -> None:
        """Display goodbye message."""
        print("\nThank you for using the Todo App!")
        print("Have a productive day!\n")
