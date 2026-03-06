import json
from collections.abc import Callable
from typing import Any, cast

from fastapi import WebSocket, WebSocketDisconnect

from chatbot_backend.adapters.mcp.tools import MCPTaskTools
from chatbot_backend.domain.services.todo_service import TodoService


class MCPServer:
    """
    MCP (Model Context Protocol) server implementation.
    Handles tool registration and execution for AI agents.
    """

    def __init__(self, todo_service: TodoService):
        """
        Initialize the MCP server with the todo service.

        Args:
            todo_service: Service for task operations
        """
        self.todo_service = todo_service
        self.tools = MCPTaskTools(todo_service)
        self.registered_tools: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {}

        # Register the available tools
        self._register_tools()

    def _register_tools(self) -> None:
        """
        Register the available MCP tools.
        """
        self.registered_tools = {
            "add_task": self.tools.add_task,
            "list_tasks": self.tools.list_tasks,
            "complete_task": self.tools.complete_task,
            "delete_task": self.tools.delete_task,
            "update_task": self.tools.update_task,
        }

    def get_tool_specification(self) -> dict[str, Any]:
        """
        Get the specification of all registered tools.

        Returns:
            Dictionary containing tool specifications
        """
        return {
            "tools": [
                {
                    "name": "add_task",
                    "description": "Create a new task",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "Task title"},
                            "description": {
                                "type": "string",
                                "description": "Task description",
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                                "description": "Task priority",
                            },
                        },
                        "required": ["title"],
                    },
                },
                {
                    "name": "list_tasks",
                    "description": "Retrieve user's tasks with optional filtering",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "status": {
                                "type": "string",
                                "enum": ["all", "pending", "completed"],
                                "description": "Filter by status",
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["all", "low", "medium", "high"],
                                "description": "Filter by priority",
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of tasks to return",
                            },
                            "offset": {
                                "type": "integer",
                                "description": "Number of tasks to skip",
                            },
                        },
                        "required": [],
                    },
                },
                {
                    "name": "complete_task",
                    "description": "Mark a task as complete",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "string",
                                "description": "ID of the task to complete",
                            }
                        },
                        "required": ["task_id"],
                    },
                },
                {
                    "name": "delete_task",
                    "description": "Remove a task",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "string",
                                "description": "ID of the task to delete",
                            }
                        },
                        "required": ["task_id"],
                    },
                },
                {
                    "name": "update_task",
                    "description": "Modify an existing task",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "string",
                                "description": "ID of the task to update",
                            },
                            "title": {
                                "type": "string",
                                "description": "New task title",
                            },
                            "description": {
                                "type": "string",
                                "description": "New task description",
                            },
                            "status": {
                                "type": "string",
                                "enum": ["pending", "completed"],
                                "description": "New task status",
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                                "description": "New task priority",
                            },
                        },
                        "required": ["task_id"],
                    },
                },
            ]
        }

    async def execute_tool(self, tool_name: str, parameters: dict[str, Any]) -> dict[str, Any]:
        """
        Execute a registered tool with the given parameters.

        Args:
            tool_name: Name of the tool to execute
            parameters: Parameters for the tool

        Returns:
            Result of the tool execution
        """
        if not tool_name:
            return {
                "error": "Tool name is required",
                "available_tools": list(self.registered_tools.keys()),
            }

        if not isinstance(parameters, dict):
            return {
                "error": f"Parameters must be a dictionary, got {type(parameters).__name__}",
                "available_tools": list(self.registered_tools.keys()),
            }

        if tool_name not in self.registered_tools:
            return {
                "error": f"Tool '{tool_name}' not found",
                "available_tools": list(self.registered_tools.keys()),
            }

        try:
            # Execute the tool
            tool_func = self.registered_tools[tool_name]

            # Validate required parameters based on tool specification
            tool_spec = self._get_tool_spec_by_name(tool_name)
            if tool_spec and "input_schema" in tool_spec:
                required_fields = tool_spec["input_schema"].get("required", [])
                for field in required_fields:
                    if field not in parameters:
                        return {
                            "error": f"Missing required parameter '{field}' for tool '{tool_name}'",
                            "available_tools": list(self.registered_tools.keys()),
                        }

            result = tool_func(parameters)

            # Validate result structure
            if not isinstance(result, dict):
                return {
                    "error": (
                        f"Tool '{tool_name}' returned invalid result type: {type(result).__name__}"
                    ),
                    "available_tools": list(self.registered_tools.keys()),
                }

            return result
        except Exception as e:
            return {
                "error": f"Error executing tool '{tool_name}': {str(e)}",
                "available_tools": list(self.registered_tools.keys()),
            }

    def _get_tool_spec_by_name(self, tool_name: str) -> dict[str, Any] | None:
        """
        Helper method to get tool specification by name.

        Args:
            tool_name: Name of the tool

        Returns:
            Tool specification if found, None otherwise
        """
        tools_spec = self.get_tool_specification()
        for tool in tools_spec.get("tools", []):
            if tool.get("name") == tool_name:
                return cast(dict[str, Any], tool)
        return None

    async def handle_websocket_connection(self, websocket: WebSocket) -> None:
        """
        Handle a WebSocket connection for MCP communication.

        Args:
            websocket: WebSocket connection
        """
        await websocket.accept()

        try:
            while True:
                # Receive message from the client
                data = await websocket.receive_text()

                try:
                    message = json.loads(data)

                    # Handle different types of messages
                    message_type = message.get("type")

                    if message_type == "call_tool":
                        tool_name = message.get("name")
                        parameters = message.get("arguments", {})

                        # Execute the tool
                        result = await self.execute_tool(tool_name, parameters)

                        # Send result back to client
                        response = {"type": "call_tool_result", "result": result}
                        await websocket.send_text(json.dumps(response))

                    elif message_type == "list_tools":
                        # Send tool specifications back to client
                        response = {
                            "type": "list_tools_result",
                            "tools": self.get_tool_specification()["tools"],
                        }
                        await websocket.send_text(json.dumps(response))

                    else:
                        # Unknown message type
                        response = {
                            "type": "error",
                            "message": f"Unknown message type: {message_type}",
                        }
                        await websocket.send_text(json.dumps(response))

                except json.JSONDecodeError:
                    response = {"type": "error", "message": "Invalid JSON received"}
                    await websocket.send_text(json.dumps(response))
                except Exception as e:
                    response = {
                        "type": "error",
                        "message": f"Error processing message: {str(e)}",
                    }
                    await websocket.send_text(json.dumps(response))

        except WebSocketDisconnect:
            print("WebSocket disconnected")
        except Exception as e:
            print(f"Unexpected error in WebSocket handler: {str(e)}")
