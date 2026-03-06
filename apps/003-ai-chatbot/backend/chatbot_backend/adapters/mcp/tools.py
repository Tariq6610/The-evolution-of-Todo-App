from typing import Any

from chatbot_backend.domain.entities.priority import Priority
from chatbot_backend.domain.entities.task_status import TaskStatus
from chatbot_backend.domain.services.todo_service import TodoService


class MCPTaskTools:
    """
    MCP (Model Context Protocol) tools for task management.
    These tools are called by the AI agent to perform task operations.
    """

    PRIORITY_MAP = {
        "low": Priority.LOW,
        "medium": Priority.MEDIUM,
        "high": Priority.HIGH,
    }

    def __init__(self, todo_service: TodoService):
        """
        Initialize the MCP tools with the todo service.

        Args:
            todo_service: Service for task operations
        """
        self.todo_service = todo_service

    def add_task(self, params: dict[str, Any]) -> dict[str, Any]:
        """
        Create a new task.

        Args:
            params: Dictionary containing task parameters
                - title (str, required): Task title
                - description (str, optional): Task description
                - priority (str, optional): Task priority (low, medium, high)
                - due_date (str, optional): Task due date (ISO format)

        Returns:
            Dictionary with the created task information
        """
        try:
            # Extract parameters
            title = params.get("title")
            if not title:
                return {"error": "Title is required"}

            description = params.get("description")

            # Map priority string to Priority enum
            priority_str = params.get("priority", "medium").lower()
            priority = self.PRIORITY_MAP.get(priority_str, Priority.MEDIUM)

            # Note: We need user_id to save the task, which should come from the context
            user_id = params.get("user_id")  # This should be passed securely from context
            if not user_id:
                return {"error": "User ID is required"}

            created_task = self.todo_service.create_task_for_user(
                title=title, user_id=user_id, description=description, priority=priority
            )

            return {
                "success": True,
                "task": {
                    "id": created_task.id,
                    "title": created_task.title,
                    "description": created_task.description,
                    "status": created_task.status.value,
                    "priority": created_task.priority.value,
                    "created_at": created_task.created_at.isoformat(),
                },
            }
        except Exception as e:
            return {"error": f"Failed to create task: {str(e)}"}

    def list_tasks(self, params: dict[str, Any]) -> dict[str, Any]:
        """
        Retrieve user's tasks with optional filtering.

        Args:
            params: Dictionary containing filter parameters
                - user_id (str, required): ID of the user whose tasks to retrieve
                - status (str, optional): Filter by status (all, pending, completed)
                - priority (str, optional): Filter by priority (all, low, medium, high)
                - limit (int, optional): Maximum number of tasks to return
                - offset (int, optional): Number of tasks to skip

        Returns:
            Dictionary with list of tasks
        """
        try:
            user_id = params.get("user_id")
            if not user_id:
                return {"error": "User ID is required"}

            # Get filters
            status_filter = params.get("status")
            priority_filter = params.get("priority")
            limit = params.get("limit")
            offset = params.get("offset", 0)

            # Get all tasks for the user
            all_tasks = self.todo_service.get_all_tasks_for_user(user_id)

            # Apply filters
            filtered_tasks = all_tasks

            if status_filter and status_filter != "all":
                if status_filter == "pending":
                    filtered_tasks = [t for t in filtered_tasks if t.status == TaskStatus.PENDING]
                elif status_filter == "completed":
                    filtered_tasks = [t for t in filtered_tasks if t.status == TaskStatus.COMPLETED]

            if priority_filter and priority_filter != "all":
                if priority_filter == "low":
                    filtered_tasks = [t for t in filtered_tasks if t.priority == Priority.LOW]
                elif priority_filter == "medium":
                    filtered_tasks = [t for t in filtered_tasks if t.priority == Priority.MEDIUM]
                elif priority_filter == "high":
                    filtered_tasks = [t for t in filtered_tasks if t.priority == Priority.HIGH]

            # Apply pagination
            if limit:
                filtered_tasks = filtered_tasks[offset : offset + int(limit)]
            else:
                filtered_tasks = filtered_tasks[offset:]

            # Convert tasks to dictionary format
            tasks_list = []
            for task in filtered_tasks:
                tasks_list.append(
                    {
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "status": task.status.value,
                        "priority": task.priority.value,
                        "created_at": task.created_at.isoformat(),
                        "updated_at": task.updated_at.isoformat(),
                    }
                )

            return {
                "success": True,
                "tasks": tasks_list,
                "total_count": len(tasks_list),
            }
        except Exception as e:
            return {"error": f"Failed to list tasks: {str(e)}"}

    def complete_task(self, params: dict[str, Any]) -> dict[str, Any]:
        """
        Mark a task as complete.

        Args:
            params: Dictionary containing task parameters
                - user_id (str, required): ID of the user
                - task_id (str, required): ID of the task to complete

        Returns:
            Dictionary with the updated task information
        """
        try:
            user_id = params.get("user_id")
            task_id = params.get("task_id")

            if not user_id:
                return {"error": "User ID is required"}
            if not task_id:
                return {"error": "Task ID is required"}

            # Get the existing task
            task = self.todo_service.get_task(task_id)
            if not task:
                return {"error": f"Task with ID {task_id} not found"}

            # Verify the task belongs to the user
            if not self.todo_service.task_exists_for_user(task_id, user_id):
                return {"error": f"Task with ID {task_id} does not belong to user {user_id}"}

            updated_task = self.todo_service.toggle_task_status_for_user(
                task_id=task_id, user_id=user_id
            )

            return {
                "success": True,
                "task": {
                    "id": updated_task.id,
                    "title": updated_task.title,
                    "description": updated_task.description,
                    "status": updated_task.status.value,
                    "priority": updated_task.priority.value,
                    "updated_at": updated_task.updated_at.isoformat(),
                },
            }
        except Exception as e:
            return {"error": f"Failed to complete task: {str(e)}"}

    def delete_task(self, params: dict[str, Any]) -> dict[str, Any]:
        """
        Remove a task.

        Args:
            params: Dictionary containing task parameters
                - user_id (str, required): ID of the user
                - task_id (str, required): ID of the task to delete

        Returns:
            Dictionary with success status
        """
        try:
            user_id = params.get("user_id")
            task_id = params.get("task_id")

            if not user_id:
                return {"error": "User ID is required"}
            if not task_id:
                return {"error": "Task ID is required"}

            # Verify the task belongs to the user
            if not self.todo_service.task_exists_for_user(task_id, user_id):
                return {"error": f"Task with ID {task_id} does not belong to user {user_id}"}

            # Delete the task
            self.todo_service.delete_task_for_user(task_id, user_id)

            return {
                "success": True,
                "message": f"Task with ID {task_id} deleted successfully",
            }
        except Exception as e:
            return {"error": f"Failed to delete task: {str(e)}"}

    def update_task(self, params: dict[str, Any]) -> dict[str, Any]:
        """
        Modify an existing task.

        Args:
            params: Dictionary containing task parameters
                - user_id (str, required): ID of the user
                - task_id (str, required): ID of the task to update
                - title (str, optional): New task title
                - description (str, optional): New task description
                - status (str, optional): New task status (pending, completed)
                - priority (str, optional): New task priority (low, medium, high)
                - due_date (str, optional): New task due date (ISO format)

        Returns:
            Dictionary with the updated task information
        """
        try:
            user_id = params.get("user_id")
            task_id = params.get("task_id")

            if not user_id:
                return {"error": "User ID is required"}
            if not task_id:
                return {"error": "Task ID is required"}

            # Get the existing task
            existing_task = self.todo_service.get_task(task_id)
            if not existing_task:
                return {"error": f"Task with ID {task_id} not found"}

            # Verify the task belongs to the user
            if not self.todo_service.task_exists_for_user(task_id, user_id):
                return {"error": f"Task with ID {task_id} does not belong to user {user_id}"}

            # Update the task
            updated_task = self.todo_service.update_task_for_user(
                task_id=task_id,
                user_id=user_id,
                title=params.get("title"),
                description=params.get("description"),
                priority=self.PRIORITY_MAP.get(params.get("priority", "").lower())
                if "priority" in params
                else None,
            )

            # Note: status changes should realistically be toggles, but since update_task_for_user
            # does not directly accept status, we will toggle it if the status needs to change.
            if "status" in params:
                status_str = params["status"].lower()
                if (status_str == "completed" and existing_task.status != TaskStatus.COMPLETED) or (
                    status_str == "pending" and existing_task.status != TaskStatus.PENDING
                ):
                    updated_task = self.todo_service.toggle_task_status_for_user(task_id, user_id)

            return {
                "success": True,
                "task": {
                    "id": updated_task.id,
                    "title": updated_task.title,
                    "description": updated_task.description,
                    "status": updated_task.status.value,
                    "priority": updated_task.priority.value,
                    "updated_at": updated_task.updated_at.isoformat(),
                },
            }
        except Exception as e:
            return {"error": f"Failed to update task: {str(e)}"}
