"""Unit tests for MCPTaskTools."""

from unittest.mock import Mock

from chatbot_backend.adapters.mcp.tools import MCPTaskTools
from chatbot_backend.domain.entities.priority import Priority
from chatbot_backend.domain.entities.task import Task
from chatbot_backend.domain.entities.task_status import TaskStatus
from chatbot_backend.domain.services.todo_service import TodoService


class TestMCPTaskTools:
    """Test cases for MCPTaskTools."""

    def test_initialization(self) -> None:
        """Should initialize the MCP tools with the todo service."""
        mock_todo_service = Mock(spec=TodoService)

        tools = MCPTaskTools(mock_todo_service)

        assert tools.todo_service == mock_todo_service

    def test_add_task_success(self) -> None:
        """Should create a new task successfully."""
        mock_todo_service = Mock(spec=TodoService)
        mock_todo_service.storage = Mock()  # Add this line

        created_task = Mock()
        created_task.id = "task-123"
        created_task.title = "Test Task"
        created_task.description = "Test Description"
        created_task.priority = Mock(value=Priority.HIGH.value)
        created_task.status = Mock(value=TaskStatus.PENDING.value)
        created_task.created_at = Mock(isoformat=Mock(return_value="2026-02-22T00:00:00"))
        created_task.updated_at = Mock(isoformat=Mock(return_value="2026-02-22T00:00:00"))
        mock_todo_service.storage.save.return_value = created_task  # Change this line

        tools = MCPTaskTools(mock_todo_service)
        result = tools.add_task(
            {
                "title": "Test Task",
                "description": "Test Description",
                "priority": "high",
                "user_id": "user-123",
            }
        )

        assert result["success"] is True
        assert result["task"]["id"] == "task-123"
        assert result["task"]["title"] == "Test Task"
        assert result["task"]["description"] == "Test Description"
        assert result["task"]["priority"] == Priority.HIGH.value
        mock_todo_service.storage.save.assert_called_once()  # Change this line

    def test_add_task_missing_title(self) -> None:
        """Should return an error when title is missing."""
        mock_todo_service = Mock(spec=TodoService)

        tools = MCPTaskTools(mock_todo_service)
        result = tools.add_task({"description": "Test Description", "user_id": "user-123"})

        assert "error" in result
        assert "Title is required" in result["error"]

    def test_add_task_missing_user_id(self) -> None:
        """Should return an error when user_id is missing."""
        mock_todo_service = Mock(spec=TodoService)

        tools = MCPTaskTools(mock_todo_service)
        result = tools.add_task({"title": "Test Task", "description": "Test Description"})

        assert "error" in result
        assert "User ID is required" in result["error"]

    def test_add_task_default_priority(self) -> None:
        """Should use default priority when none is specified."""
        mock_todo_service = Mock(spec=TodoService)
        mock_todo_service.storage = Mock()

        created_task = Mock(
            id="task-123",
            title="Test Task",
            priority=Mock(value=Priority.MEDIUM.value),
            status=Mock(value=TaskStatus.PENDING.value),
            created_at=Mock(isoformat=Mock(return_value="2026-02-22T00:00:00")),
            updated_at=Mock(isoformat=Mock(return_value="2026-02-22T00:00:00")),
        )
        mock_todo_service.storage.save.return_value = created_task

        tools = MCPTaskTools(mock_todo_service)
        result = tools.add_task({"title": "Test Task", "user_id": "user-123"})

        assert result["success"] is True
        assert result["task"]["priority"] == Priority.MEDIUM.value
        mock_todo_service.storage.save.assert_called_once()

    def test_add_task_low_priority(self) -> None:
        """Should create a task with low priority."""
        mock_todo_service = Mock(spec=TodoService)
        mock_todo_service.storage = Mock()

        created_task = Mock(
            id="task-123",
            title="Test Task",
            priority=Mock(value=Priority.LOW.value),
            status=Mock(value=TaskStatus.PENDING.value),
            created_at=Mock(isoformat=Mock(return_value="2026-02-22T00:00:00")),
            updated_at=Mock(isoformat=Mock(return_value="2026-02-22T00:00:00")),
        )
        mock_todo_service.storage.save.return_value = created_task

        tools = MCPTaskTools(mock_todo_service)
        result = tools.add_task({"title": "Test Task", "priority": "low", "user_id": "user-123"})

        assert result["success"] is True
        assert result["task"]["priority"] == Priority.LOW.value
        mock_todo_service.storage.save.assert_called_once()

    def test_add_task_medium_priority(self) -> None:
        """Should create a task with medium priority."""
        mock_todo_service = Mock(spec=TodoService)
        mock_todo_service.storage = Mock()

        created_task = Mock(
            id="task-123",
            title="Test Task",
            priority=Mock(value=Priority.MEDIUM.value),
            status=Mock(value=TaskStatus.PENDING.value),
            created_at=Mock(isoformat=Mock(return_value="2026-02-22T00:00:00")),
            updated_at=Mock(isoformat=Mock(return_value="2026-02-22T00:00:00")),
        )
        mock_todo_service.storage.save.return_value = created_task

        tools = MCPTaskTools(mock_todo_service)
        result = tools.add_task({"title": "Test Task", "priority": "medium", "user_id": "user-123"})

        assert result["success"] is True
        assert result["task"]["priority"] == Priority.MEDIUM.value
        mock_todo_service.storage.save.assert_called_once()

    def test_add_task_exception_handling(self) -> None:
        """Should handle exceptions during task creation."""
        mock_todo_service = Mock(spec=TodoService)
        mock_todo_service.storage = Mock()
        mock_todo_service.storage.save.side_effect = Exception("Database error")

        tools = MCPTaskTools(mock_todo_service)
        result = tools.add_task({"title": "Test Task", "user_id": "user-123"})

        assert "error" in result
        assert "Failed to create task" in result["error"]

    def test_list_tasks_success(self) -> None:
        """Should retrieve user's tasks successfully."""
        mock_todo_service = Mock(spec=TodoService)
        mock_todo_service.storage = Mock()

        tasks = [
            Task(
                id="task-1",
                title="Task 1",
                status=TaskStatus.PENDING,
                priority=Priority.MEDIUM,
                description=None,
            ),
            Task(
                id="task-2",
                title="Task 2",
                status=TaskStatus.COMPLETED,
                priority=Priority.HIGH,
                description=None,
            ),
        ]
        mock_todo_service.storage.get_all_for_user.return_value = tasks

        tools = MCPTaskTools(mock_todo_service)
        result = tools.list_tasks({"user_id": "user-123"})

        assert result["success"] is True
        assert len(result["tasks"]) == 2
        assert result["tasks"][0]["id"] == "task-1"
        assert result["tasks"][1]["id"] == "task-2"
        mock_todo_service.storage.get_all_for_user.assert_called_once_with("user-123")

    def test_list_tasks_with_filters(self) -> None:
        """Should apply filters when retrieving tasks."""
        mock_todo_service = Mock(spec=TodoService)
        mock_todo_service.storage = Mock()

        all_tasks = [
            Task(
                id="task-1",
                title="Task 1",
                status=TaskStatus.PENDING,
                priority=Priority.MEDIUM,
                description=None,
            ),
            Task(
                id="task-2",
                title="Task 2",
                status=TaskStatus.COMPLETED,
                priority=Priority.HIGH,
                description=None,
            ),
            Task(
                id="task-3",
                title="Task 3",
                status=TaskStatus.PENDING,
                priority=Priority.LOW,
                description=None,
            ),
        ]
        mock_todo_service.storage.get_all_for_user.return_value = all_tasks

        tools = MCPTaskTools(mock_todo_service)
        result = tools.list_tasks(
            {
                "user_id": "user-123",
                "status": "pending",
                "priority": "medium",
                "limit": 10,
                "offset": 0,
            }
        )

        assert result["success"] is True
        # The filtering happens in the tool itself, so we expect all tasks back
        # but the tool would filter them based on status and priority
        assert len(result["tasks"]) == 1  # Only task-1
        assert result["tasks"][0]["id"] == "task-1"
        mock_todo_service.storage.get_all_for_user.assert_called_once_with("user-123")

    def test_list_tasks_missing_user_id(self) -> None:
        """Should return an error when user_id is missing."""
        mock_todo_service = Mock(spec=TodoService)

        tools = MCPTaskTools(mock_todo_service)
        result = tools.list_tasks({})

        assert "error" in result
        assert "User ID is required" in result["error"]

    def test_list_tasks_pagination(self) -> None:
        """Should apply pagination to the results."""
        mock_todo_service = Mock(spec=TodoService)
        mock_todo_service.storage = Mock()

        all_tasks = [
            Task(
                id=f"task-{i}",
                title=f"Task {i}",
                status=TaskStatus.PENDING,
                priority=Priority.MEDIUM,
                description=None,
            )
            for i in range(20)
        ]
        mock_todo_service.storage.get_all_for_user.return_value = all_tasks

        tools = MCPTaskTools(mock_todo_service)
        result = tools.list_tasks({"user_id": "user-123", "limit": 5, "offset": 10})

        assert result["success"] is True
        # Since filtering is applied after getting all tasks, we'd get all 20 tasks
        # but only the ones after offset and limited by limit
        # Actually, looking at the code, it applies pagination after filtering
        assert len(result["tasks"]) == 5
        assert result["tasks"][0]["id"] == "task-10"
        assert result["tasks"][-1]["id"] == "task-14"
        mock_todo_service.storage.get_all_for_user.assert_called_once_with("user-123")

    def test_complete_task_success(self) -> None:
        """Should mark a task as complete successfully."""
        mock_todo_service = Mock(spec=TodoService)
        mock_todo_service.storage = Mock()  # Add this line

        existing_task = Task(
            id="task-123",
            title="Test Task",
            status=TaskStatus.PENDING,
            priority=Priority.MEDIUM,
            description=None,
        )
        updated_task = Task(
            id="task-123",
            title="Test Task",
            status=TaskStatus.COMPLETED,
            priority=Priority.MEDIUM,
            description=None,
        )

        mock_todo_service.storage.get.return_value = existing_task
        mock_todo_service.storage.exists_for_user.return_value = True
        mock_todo_service.update_task_for_user.return_value = updated_task  # Correct method name

        tools = MCPTaskTools(mock_todo_service)
        result = tools.complete_task({"user_id": "user-123", "task_id": "task-123"})

        assert result["success"] is True
        assert result["task"]["id"] == "task-123"
        assert result["task"]["status"] == TaskStatus.COMPLETED.value
        mock_todo_service.storage.get.assert_called_once_with("task-123")
        mock_todo_service.storage.exists_for_user.assert_called_once_with("task-123", "user-123")
        mock_todo_service.update_task_for_user.assert_called_once()  # Correct method name

    def test_complete_task_missing_user_id(self) -> None:
        """Should return an error when user_id is missing."""
        mock_todo_service = Mock(spec=TodoService)

        tools = MCPTaskTools(mock_todo_service)
        result = tools.complete_task({"task_id": "task-123"})

        assert "error" in result
        assert "User ID is required" in result["error"]

    def test_complete_task_missing_task_id(self) -> None:
        """Should return an error when task_id is missing."""
        mock_todo_service = Mock(spec=TodoService)

        tools = MCPTaskTools(mock_todo_service)
        result = tools.complete_task({"user_id": "user-123"})

        assert "error" in result
        assert "Task ID is required" in result["error"]

    def test_complete_task_not_found(self) -> None:
        """Should return an error when task is not found."""
        mock_todo_service = Mock(spec=TodoService)
        mock_todo_service.storage = Mock()  # Add this line
        mock_todo_service.storage.get.return_value = None

        tools = MCPTaskTools(mock_todo_service)
        result = tools.complete_task({"user_id": "user-123", "task_id": "nonexistent"})

        assert "error" in result
        assert "not found" in result["error"]
        mock_todo_service.storage.get.assert_called_once_with("nonexistent")

    def test_complete_task_unauthorized(self) -> None:
        """Should return an error when task doesn't belong to user."""
        mock_todo_service = Mock(spec=TodoService)
        mock_todo_service.storage = Mock()  # Add this line

        existing_task = Task(
            id="task-123",
            title="Test Task",
            status=TaskStatus.PENDING,
            priority=Priority.MEDIUM,
            description=None,
        )
        mock_todo_service.storage.get.return_value = existing_task
        mock_todo_service.storage.exists_for_user.return_value = False

        tools = MCPTaskTools(mock_todo_service)
        result = tools.complete_task({"user_id": "user-123", "task_id": "task-123"})

        assert "error" in result
        assert "does not belong to user" in result["error"]

    def test_complete_task_exception_handling(self) -> None:
        """Should handle exceptions during task completion."""
        mock_todo_service = Mock(spec=TodoService)
        mock_todo_service.storage = Mock()  # Add this line
        mock_todo_service.storage.get.side_effect = Exception("Database error")

        tools = MCPTaskTools(mock_todo_service)
        result = tools.complete_task({"user_id": "user-123", "task_id": "task-123"})

        assert "error" in result
        assert "Failed to complete task" in result["error"]

    def test_delete_task_success(self) -> None:
        """Should delete a task successfully."""
        mock_todo_service = Mock(spec=TodoService)
        mock_todo_service.storage = Mock()  # Add this line

        mock_todo_service.storage.exists_for_user.return_value = True

        tools = MCPTaskTools(mock_todo_service)
        result = tools.delete_task({"user_id": "user-123", "task_id": "task-123"})

        assert result["success"] is True
        assert "deleted successfully" in result["message"]
        mock_todo_service.storage.exists_for_user.assert_called_once_with("task-123", "user-123")
        mock_todo_service.storage.delete_for_user.assert_called_once_with("user-123", "task-123")

    def test_delete_task_missing_user_id(self) -> None:
        """Should return an error when user_id is missing."""
        mock_todo_service = Mock(spec=TodoService)

        tools = MCPTaskTools(mock_todo_service)
        result = tools.delete_task({"task_id": "task-123"})

        assert "error" in result
        assert "User ID is required" in result["error"]

    def test_delete_task_missing_task_id(self) -> None:
        """Should return an error when task_id is missing."""
        mock_todo_service = Mock(spec=TodoService)

        tools = MCPTaskTools(mock_todo_service)
        result = tools.delete_task({"user_id": "user-123"})

        assert "error" in result
        assert "Task ID is required" in result["error"]

    def test_delete_task_unauthorized(self) -> None:
        """Should return an error when task doesn't belong to user."""
        mock_todo_service = Mock(spec=TodoService)
        mock_todo_service.storage = Mock()  # Add this line
        mock_todo_service.storage.exists_for_user.return_value = False

        tools = MCPTaskTools(mock_todo_service)
        result = tools.delete_task({"user_id": "user-123", "task_id": "task-123"})

        assert "error" in result
        assert "does not belong to user" in result["error"]

    def test_delete_task_exception_handling(self) -> None:
        """Should handle exceptions during task deletion."""
        mock_todo_service = Mock(spec=TodoService)
        mock_todo_service.storage = Mock()  # Add this line
        mock_todo_service.storage.exists_for_user.return_value = True
        mock_todo_service.storage.delete_for_user.side_effect = Exception("Database error")

        tools = MCPTaskTools(mock_todo_service)
        result = tools.delete_task({"user_id": "user-123", "task_id": "task-123"})

        assert "error" in result
        assert "Failed to delete task" in result["error"]

    def test_update_task_success(self) -> None:
        """Should update a task successfully."""
        mock_todo_service = Mock(spec=TodoService)
        mock_todo_service.storage = Mock()  # Add this line

        existing_task = Task(
            id="task-123",
            title="Old Title",
            description="Old Description",
            status=TaskStatus.PENDING,
            priority=Priority.MEDIUM,
        )
        updated_task = Task(
            id="task-123",
            title="New Title",
            description="New Description",
            status=TaskStatus.COMPLETED,
            priority=Priority.HIGH,
        )

        mock_todo_service.storage.get.return_value = existing_task
        mock_todo_service.storage.exists_for_user.return_value = True
        mock_todo_service.update_task_for_user.return_value = updated_task  # Correct method

        tools = MCPTaskTools(mock_todo_service)
        result = tools.update_task(
            {
                "user_id": "user-123",
                "task_id": "task-123",
                "title": "New Title",
                "description": "New Description",
                "status": "completed",
                "priority": "high",
            }
        )

        assert result["success"] is True
        assert result["task"]["id"] == "task-123"
        assert result["task"]["title"] == "New Title"
        assert result["task"]["description"] == "New Description"
        assert result["task"]["status"] == TaskStatus.COMPLETED.value
        assert result["task"]["priority"] == Priority.HIGH.value
        mock_todo_service.storage.get.assert_called_once_with("task-123")
        mock_todo_service.storage.exists_for_user.assert_called_once_with("task-123", "user-123")
        mock_todo_service.update_task_for_user.assert_called_once()  # Correct method

    def test_update_task_partial_updates(self) -> None:
        """Should update only the specified fields."""
        mock_todo_service = Mock(spec=TodoService)
        mock_todo_service.storage = Mock()  # Add this line

        existing_task = Task(
            id="task-123",
            title="Old Title",
            description="Old Description",
            status=TaskStatus.PENDING,
            priority=Priority.MEDIUM,
        )
        updated_task = Task(
            id="task-123",
            title="New Title",  # Only this changed
            description="Old Description",  # Unchanged
            status=TaskStatus.PENDING,  # Unchanged
            priority=Priority.MEDIUM,  # Unchanged
        )

        mock_todo_service.storage.get.return_value = existing_task
        mock_todo_service.storage.exists_for_user.return_value = True
        mock_todo_service.update_task_for_user.return_value = updated_task

        tools = MCPTaskTools(mock_todo_service)
        result = tools.update_task(
            {
                "user_id": "user-123",
                "task_id": "task-123",
                "title": "New Title",  # Only updating title
            }
        )

        assert result["success"] is True
        assert result["task"]["title"] == "New Title"
        # Other fields should remain unchanged
        mock_todo_service.update_task_for_user.assert_called_once()

    def test_update_task_invalid_status(self) -> None:
        """Should return an error for invalid status."""
        mock_todo_service = Mock(spec=TodoService)
        mock_todo_service.storage = Mock()  # Add this line

        existing_task = Task(
            id="task-123",
            title="Old Title",
            description=None,
            status=TaskStatus.PENDING,
            priority=Priority.MEDIUM,
        )
        mock_todo_service.storage.get.return_value = existing_task
        mock_todo_service.storage.exists_for_user.return_value = True

        tools = MCPTaskTools(mock_todo_service)
        result = tools.update_task(
            {"user_id": "user-123", "task_id": "task-123", "status": "invalid_status"}
        )

        assert "error" in result
        assert "Invalid status" in result["error"]

    def test_update_task_invalid_priority(self) -> None:
        """Should return an error for invalid priority."""
        mock_todo_service = Mock(spec=TodoService)
        mock_todo_service.storage = Mock()  # Add this line

        existing_task = Task(
            id="task-123",
            title="Old Title",
            description=None,
            status=TaskStatus.PENDING,
            priority=Priority.MEDIUM,
        )
        mock_todo_service.storage.get.return_value = existing_task
        mock_todo_service.storage.exists_for_user.return_value = True

        tools = MCPTaskTools(mock_todo_service)
        result = tools.update_task(
            {
                "user_id": "user-123",
                "task_id": "task-123",
                "priority": "invalid_priority",
            }
        )

        assert "error" in result
        assert "Invalid priority" in result["error"]

    def test_update_task_missing_user_id(self) -> None:
        """Should return an error when user_id is missing."""
        mock_todo_service = Mock(spec=TodoService)

        tools = MCPTaskTools(mock_todo_service)
        result = tools.update_task({"task_id": "task-123"})

        assert "error" in result
        assert "User ID is required" in result["error"]

    def test_update_task_missing_task_id(self) -> None:
        """Should return an error when task_id is missing."""
        mock_todo_service = Mock(spec=TodoService)

        tools = MCPTaskTools(mock_todo_service)
        result = tools.update_task({"user_id": "user-123"})

        assert "error" in result
        assert "Task ID is required" in result["error"]

    def test_update_task_not_found(self) -> None:
        """Should return an error when task is not found."""
        mock_todo_service = Mock(spec=TodoService)
        mock_todo_service.storage = Mock()  # Add this line
        mock_todo_service.storage.get.return_value = None

        tools = MCPTaskTools(mock_todo_service)
        result = tools.update_task({"user_id": "user-123", "task_id": "nonexistent"})

        assert "error" in result
        assert "not found" in result["error"]

    def test_update_task_unauthorized(self) -> None:
        """Should return an error when task doesn't belong to user."""
        mock_todo_service = Mock(spec=TodoService)
        mock_todo_service.storage = Mock()  # Add this line

        existing_task = Task(
            id="task-123",
            title="Old Title",
            description=None,
            status=TaskStatus.PENDING,
            priority=Priority.MEDIUM,
        )
        mock_todo_service.storage.get.return_value = existing_task
        mock_todo_service.storage.exists_for_user.return_value = False

        tools = MCPTaskTools(mock_todo_service)
        result = tools.update_task({"user_id": "user-123", "task_id": "task-123"})

        assert "error" in result
        assert "does not belong to user" in result["error"]

    def test_update_task_exception_handling(self) -> None:
        """Should handle exceptions during task update."""
        mock_todo_service = Mock(spec=TodoService)
        mock_todo_service.storage.get.side_effect = Exception("Database error")

        tools = MCPTaskTools(mock_todo_service)
        result = tools.update_task({"user_id": "user-123", "task_id": "task-123"})

        assert "error" in result
        assert "Failed to update task" in result["error"]
