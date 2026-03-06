"""Unit tests for MCPServer."""

import json
from contextlib import suppress
from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi import WebSocket, WebSocketDisconnect

from chatbot_backend.adapters.mcp.server import MCPServer
from chatbot_backend.adapters.mcp.tools import MCPTaskTools
from chatbot_backend.domain.services.todo_service import TodoService


class TestMCPServer:
    """Test cases for MCPServer."""

    def test_initialization(self) -> None:
        """Should initialize the MCP server with todo service."""
        mock_todo_service = Mock(spec=TodoService)

        server = MCPServer(mock_todo_service)

        assert server.todo_service == mock_todo_service
        assert isinstance(server.tools, MCPTaskTools)
        assert (
            len(server.registered_tools) == 5
        )  # add_task, list_tasks, complete_task, delete_task, update_task
        assert "add_task" in server.registered_tools
        assert "list_tasks" in server.registered_tools
        assert "complete_task" in server.registered_tools
        assert "delete_task" in server.registered_tools
        assert "update_task" in server.registered_tools

    def test_get_tool_specification(self) -> None:
        """Should return the specification of all registered tools."""
        mock_todo_service = Mock(spec=TodoService)

        server = MCPServer(mock_todo_service)
        spec = server.get_tool_specification()

        assert "tools" in spec
        assert len(spec["tools"]) == 5

        # Check that each tool has the required properties
        tool_names = [tool["name"] for tool in spec["tools"]]
        assert "add_task" in tool_names
        assert "list_tasks" in tool_names
        assert "complete_task" in tool_names
        assert "delete_task" in tool_names
        assert "update_task" in tool_names

        # Check add_task tool structure
        add_task_tool = next(tool for tool in spec["tools"] if tool["name"] == "add_task")
        assert "description" in add_task_tool
        assert "input_schema" in add_task_tool
        assert add_task_tool["input_schema"]["type"] == "object"
        assert "properties" in add_task_tool["input_schema"]

    @pytest.mark.asyncio
    async def test_execute_tool_success(self) -> None:
        """Should execute a registered tool with the given parameters."""
        mock_todo_service = Mock(spec=TodoService)

        server = MCPServer(mock_todo_service)

        # Mock the tool function to return a known result
        mock_tool_result = {
            "success": True,
            "task": {"id": "task-123", "title": "Test Task"},
        }
        mock_add_task = Mock(return_value=mock_tool_result)
        server.registered_tools["add_task"] = mock_add_task

        result = await server.execute_tool(
            "add_task", {"title": "Test Task", "user_id": "user-123"}
        )

        assert result == mock_tool_result
        mock_add_task.assert_called_once_with({"title": "Test Task", "user_id": "user-123"})

    @pytest.mark.asyncio
    async def test_execute_tool_not_found(self) -> None:
        """Should return an error when tool is not found."""
        mock_todo_service = Mock(spec=TodoService)

        server = MCPServer(mock_todo_service)

        result = await server.execute_tool("nonexistent_tool", {"param": "value"})

        assert "error" in result
        assert "nonexistent_tool" in result["error"]
        assert "available_tools" in result
        assert isinstance(result["available_tools"], list)

    @pytest.mark.asyncio
    async def test_execute_tool_exception_handling(self) -> None:
        """Should handle exceptions during tool execution."""
        mock_todo_service = Mock(spec=TodoService)

        server = MCPServer(mock_todo_service)

        # Mock the tool function to raise an exception
        server.registered_tools["add_task"] = Mock(side_effect=Exception("Test error"))

        result = await server.execute_tool(
            "add_task", {"title": "Test Task", "user_id": "user-123"}
        )

        assert "error" in result
        assert "Test error" in result["error"]

    @pytest.mark.asyncio
    async def test_handle_websocket_connection_call_tool(self) -> None:
        """Should handle tool call requests via WebSocket."""
        mock_todo_service = Mock(spec=TodoService)

        server = MCPServer(mock_todo_service)

        # Mock the execute_tool method
        mock_execute_tool = AsyncMock(return_value={"success": True, "result": "test"})

        # Create a mock WebSocket
        mock_websocket = AsyncMock(spec=WebSocket)
        mock_websocket.receive_text.side_effect = [
            json.dumps(
                {
                    "type": "call_tool",
                    "name": "add_task",
                    "arguments": {"title": "Test Task", "user_id": "user-123"},
                }
            ),
            WebSocketDisconnect(),
        ]

        with (
            patch.object(server, "execute_tool", mock_execute_tool),
            suppress(WebSocketDisconnect),
        ):
            await server.handle_websocket_connection(mock_websocket)

        # Verify the tool was called
        mock_execute_tool.assert_called_once_with(
            "add_task", {"title": "Test Task", "user_id": "user-123"}
        )
        # Verify the response was sent
        mock_websocket.send_text.assert_called()

    @pytest.mark.asyncio
    async def test_handle_websocket_connection_list_tools(self) -> None:
        """Should handle list tools requests via WebSocket."""
        mock_todo_service = Mock(spec=TodoService)

        server = MCPServer(mock_todo_service)

        # Mock the get_tool_specification method
        mock_spec = {"tools": [{"name": "add_task", "description": "Adds a task"}]}

        # Create a mock WebSocket
        mock_websocket = AsyncMock(spec=WebSocket)
        # Simulate disconnect after one message
        mock_websocket.receive_text.side_effect = [
            json.dumps({"type": "list_tools"}),
            WebSocketDisconnect(),
        ]

        with (
            patch.object(server, "get_tool_specification", return_value=mock_spec),
            suppress(WebSocketDisconnect),
        ):
            await server.handle_websocket_connection(mock_websocket)

        # Verify the response was sent
        mock_websocket.send_text.assert_called()

    @pytest.mark.asyncio
    async def test_handle_websocket_connection_invalid_json(self) -> None:
        """Should handle invalid JSON in WebSocket messages."""
        mock_todo_service = Mock(spec=TodoService)

        server = MCPServer(mock_todo_service)

        # Create a mock WebSocket
        mock_websocket = AsyncMock(spec=WebSocket)
        mock_websocket.receive_text.return_value = "{invalid json"

        # Simulate disconnect after one message
        mock_websocket.receive_text.side_effect = [
            "{invalid json",
            WebSocketDisconnect(),
        ]

        with suppress(BaseException):
            await server.handle_websocket_connection(mock_websocket)

        # Verify an error response was sent
        mock_websocket.send_text.assert_called()

    @pytest.mark.asyncio
    async def test_handle_websocket_connection_unknown_message_type(self) -> None:
        """Should handle unknown message types in WebSocket messages."""
        mock_todo_service = Mock(spec=TodoService)

        server = MCPServer(mock_todo_service)

        # Create a mock WebSocket
        mock_websocket = AsyncMock(spec=WebSocket)
        mock_websocket.receive_text.return_value = json.dumps({"type": "unknown_type"})

        # Simulate disconnect after one message
        mock_websocket.receive_text.side_effect = [
            json.dumps({"type": "unknown_type"}),
            WebSocketDisconnect(),
        ]

        with suppress(BaseException):
            await server.handle_websocket_connection(mock_websocket)

        # Verify an error response was sent
        mock_websocket.send_text.assert_called()


class TestMCPServerWebSocketDisconnect:
    """Test cases for WebSocket disconnection handling."""

    @pytest.mark.asyncio
    async def test_handle_websocket_connection_disconnect(self) -> None:
        """Should handle WebSocket disconnection gracefully."""
        mock_todo_service = Mock(spec=TodoService)

        server = MCPServer(mock_todo_service)

        # Create a mock WebSocket that raises WebSocketDisconnect immediately
        mock_websocket = AsyncMock(spec=WebSocket)
        mock_websocket.receive_text.side_effect = WebSocketDisconnect()

        # Should not raise an exception
        await server.handle_websocket_connection(mock_websocket)

        # Verify accept was called
        mock_websocket.accept.assert_called_once()
