"""Main entry point for Todo CLI application.

Phase I Console Todo App with in-memory storage.
"""
from src.adapters.cli.console_adapter import ConsoleAdapter
from src.adapters.cli.menu_system import MenuSystem
from src.adapters.storage.in_memory_storage import InMemoryStorage
from src.domain.services.todo_service import TodoService


def main() -> None:
    """
    Main application entry point.

    Initializes components and runs main application loop.
    """
    # Initialize storage (Phase I: in-memory)
    storage = InMemoryStorage()

    # Initialize business logic service
    service = TodoService(storage)

    # Initialize CLI components
    menu = MenuSystem()
    adapter = ConsoleAdapter(service, menu)

    # Main application loop
    try:
        while True:
            # Display menu
            adapter.menu.show_menu()

            # Get user choice
            choice = adapter.menu.get_user_choice()

            # Handle choice
            match choice:
                case 0:  # Exit
                    if adapter.show_exit_confirmation():
                        adapter.show_goodbye()
                        break
                case 1:  # Add Task
                    adapter.add_task_flow()
                case 2:  # View All Tasks
                    adapter.view_all_tasks_flow()
                case 3:  # Update Task
                    adapter.update_task_flow()
                case 4:  # Delete Task
                    adapter.delete_task_flow()
                case 5:  # Toggle Status
                    adapter.toggle_status_flow()
                case _:
                    print("Invalid choice. Please try again.")

    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user.")
        adapter.show_goodbye()
    except Exception as e:
        print(f"\n✗ An unexpected error occurred: {e}")
        print("Please restart the application.")


if __name__ == "__main__":
    main()
