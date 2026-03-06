"""Unit tests for chat routes."""

from typing import Any
from unittest.mock import Mock, patch

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from chatbot_backend.adapters.api.chat_routes import (
    get_conversation_service,
    get_todo_service,
)
from chatbot_backend.adapters.db.session import get_session
from chatbot_backend.adapters.mcp.server import MCPServer
from chatbot_backend.domain.entities.conversation import Conversation
from chatbot_backend.domain.entities.message import Message, MessageRole
from chatbot_backend.domain.services.conversation_service import ConversationService
from chatbot_backend.domain.services.todo_service import TodoService
from chatbot_backend.main import app


class TestChatRoutes:
    """Test cases for chat routes."""

    def setup_method(self) -> None:
        """Setup test client with mocked dependencies."""
        self.client = TestClient(app)

        # Create mocks for dependencies
        self.mock_session = Mock(spec=Session)
        self.mock_conversation_service = Mock(spec=ConversationService)
        self.mock_todo_service = Mock(spec=TodoService)
        self.mock_mcp_server = Mock(spec=MCPServer)

    def test_chat_route_dependency_injection(self) -> None:
        """Should inject dependencies correctly."""
        # Override dependencies
        app.dependency_overrides[get_session] = lambda: self.mock_session
        app.dependency_overrides[get_conversation_service] = lambda: self.mock_conversation_service
        app.dependency_overrides[get_todo_service] = lambda: self.mock_todo_service

        # Mock conversation service methods
        conv = Conversation(id="conv-123", user_id="user-123", title="Test Conv")
        self.mock_conversation_service.get_conversations_for_user.return_value = [conv]
        user_message = Message(id="msg-1", role=MessageRole.USER, content="Hello")
        self.mock_conversation_service.add_user_message.return_value = user_message
        assistant_message = Message(id="msg-2", role=MessageRole.ASSISTANT, content="Hi there")
        self.mock_conversation_service.add_assistant_message.return_value = assistant_message
        self.mock_conversation_service.get_recent_messages.return_value = [user_message]

        # Mock the OpenAI client
        with patch("chatbot_backend.adapters.api.chat_routes.OpenAI") as mock_openai_class:
            mock_openai_instance = Mock()
            mock_openai_class.return_value = mock_openai_instance

            # Mock the API response
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message = Mock()
            mock_response.choices[0].message.content = "Hi there"
            mock_response.choices[0].message.tool_calls = None
            mock_openai_instance.chat.completions.create.return_value = mock_response

            # Mock environment variables
            with patch(
                "chatbot_backend.adapters.api.chat_routes.os.getenv",
                return_value="fake-api-key",
            ):
                # Make the request
                response = self.client.post("/api/v1/chat/user-123", json={"message": "Hello"})

                # Assertions
                assert response.status_code == 200
                data = response.json()
                assert data["response"] == "Hi there"
                assert data["conversation_id"] == "conv-123"

        # Clean up
        app.dependency_overrides.clear()

    def test_get_user_conversations(self) -> None:
        """Should return user's conversations."""
        app.dependency_overrides[get_conversation_service] = lambda: self.mock_conversation_service

        conv = Conversation(id="conv-123", user_id="user-123", title="Test Conv")
        self.mock_conversation_service.get_conversations_for_user.return_value = [conv]

        response = self.client.get("/api/v1/chat/conversations/user-123")

        assert response.status_code == 200
        data = response.json()
        assert "conversations" in data
        assert len(data["conversations"]) == 1
        assert data["conversations"][0]["id"] == "conv-123"

        app.dependency_overrides.clear()

    def test_get_conversation(self) -> None:
        """Should return a specific conversation."""
        app.dependency_overrides[get_conversation_service] = lambda: self.mock_conversation_service

        conv = Conversation(id="conv-123", user_id="user-123", title="Test Conv")
        self.mock_conversation_service.get_conversation.return_value = conv

        response = self.client.get("/api/v1/chat/conversation/conv-123")

        assert response.status_code == 200
        data = response.json()
        assert "conversation" in data
        assert data["conversation"]["id"] == "conv-123"

        app.dependency_overrides.clear()

    def test_get_conversation_not_found(self) -> None:
        """Should return error when conversation is not found."""
        app.dependency_overrides[get_conversation_service] = lambda: self.mock_conversation_service

        self.mock_conversation_service.get_conversation.return_value = None

        response = self.client.get("/api/v1/chat/conversation/nonexistent")

        assert response.status_code == 200  # The route returns 200 with error in body
        data = response.json()
        assert "error" in data

        app.dependency_overrides.clear()


class TestChatRouteFunctions:
    """Test individual functions from chat_routes module."""

    @pytest.fixture
    def mock_dependencies(self) -> dict[str, Any]:
        """Fixture to create mocked dependencies."""
        mock_session = Mock(spec=Session)
        mock_chat_repo = Mock()
        mock_task_repo = Mock()
        mock_conversation_service = Mock(spec=ConversationService)
        mock_todo_service = Mock(spec=TodoService)

        return {
            "session": mock_session,
            "chat_repo": mock_chat_repo,
            "task_repo": mock_task_repo,
            "conversation_service": mock_conversation_service,
            "todo_service": mock_todo_service,
        }

    def test_get_conversation_service(self, mock_dependencies: dict[str, Any]) -> None:
        """Should return conversation service with proper dependencies."""

        mock_session = mock_dependencies["session"]
        mock_chat_repo_class = Mock()
        mock_task_repo_class = Mock()
        mock_conv_service_class = Mock()

        with (
            patch(
                "chatbot_backend.adapters.api.chat_routes.SQLModelChatRepository",
                mock_chat_repo_class,
            ),
            patch(
                "chatbot_backend.adapters.api.chat_routes.SQLModelTaskRepository",
                mock_task_repo_class,
            ),
            patch(
                "chatbot_backend.adapters.api.chat_routes.ConversationService",
                mock_conv_service_class,
            ),
        ):
            # Mock the repositories
            mock_chat_repo_instance = Mock()
            mock_task_repo_instance = Mock()
            mock_chat_repo_class.return_value = mock_chat_repo_instance
            mock_task_repo_class.return_value = mock_task_repo_instance

            # Mock the service
            mock_conv_service_instance = Mock()
            mock_conv_service_class.return_value = mock_conv_service_instance

            # Import and call the function
            from chatbot_backend.adapters.api.chat_routes import (
                get_conversation_service,
            )

            result = get_conversation_service(mock_session)

            # Verify calls
            mock_chat_repo_class.assert_called_once_with(mock_session)
            mock_task_repo_class.assert_called_once_with(mock_session)
            mock_conv_service_class.assert_called_once_with(
                mock_chat_repo_instance, mock_task_repo_instance
            )
            assert result == mock_conv_service_instance

    def test_get_todo_service(self, mock_dependencies: dict[str, Any]) -> None:
        """Should return todo service with proper dependencies."""

        mock_session = mock_dependencies["session"]
        mock_task_repo_class = Mock()
        mock_todo_service_class = Mock()

        with (
            patch(
                "chatbot_backend.adapters.api.chat_routes.SQLModelTaskRepository",
                mock_task_repo_class,
            ),
            patch(
                "chatbot_backend.adapters.api.chat_routes.TodoService",
                mock_todo_service_class,
            ),
        ):
            # Mock the repository
            mock_task_repo_instance = Mock()
            mock_task_repo_class.return_value = mock_task_repo_instance

            # Mock the service
            mock_todo_service_instance = Mock()
            mock_todo_service_class.return_value = mock_todo_service_instance

            # Import and call the function
            from chatbot_backend.adapters.api.chat_routes import get_todo_service

            result = get_todo_service(mock_session)

            # Verify calls
            mock_task_repo_class.assert_called_once_with(mock_session)
            mock_todo_service_class.assert_called_once_with(mock_task_repo_instance)
            assert result == mock_todo_service_instance
