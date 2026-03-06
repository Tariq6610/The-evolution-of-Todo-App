"""Unit tests for ConversationService."""

from unittest.mock import Mock

import pytest

from chatbot_backend.domain.entities.conversation import Conversation
from chatbot_backend.domain.entities.message import Message, MessageRole
from chatbot_backend.domain.services.conversation_service import ConversationService


class TestConversationService:
    """Test cases for ConversationService."""

    def test_create_conversation(self) -> None:
        """Should create a new conversation for a user."""
        mock_chat_repo = Mock()
        mock_task_repo = Mock()

        conversation = Conversation(id="conv-123", user_id="user-123", title="Test Conversation")
        mock_chat_repo.create_conversation.return_value = conversation

        service = ConversationService(mock_chat_repo, mock_task_repo)
        result = service.create_conversation("user-123", "Test Conversation")

        assert result is not None
        assert result.id == "conv-123"
        assert result.user_id == "user-123"
        assert result.title == "Test Conversation"
        mock_chat_repo.create_conversation.assert_called_once_with("user-123", "Test Conversation")

    def test_get_conversation(self) -> None:
        """Should get a conversation by ID."""
        mock_chat_repo = Mock()
        mock_task_repo = Mock()

        conversation = Conversation(id="conv-123", user_id="user-123", title="Test Conversation")
        mock_chat_repo.get_conversation.return_value = conversation

        service = ConversationService(mock_chat_repo, mock_task_repo)
        result = service.get_conversation("conv-123")

        assert result is not None
        assert result.id == "conv-123"
        mock_chat_repo.get_conversation.assert_called_once_with("conv-123")

    def test_get_conversation_returns_none_when_not_found(self) -> None:
        """Should return None when conversation is not found."""
        mock_chat_repo = Mock()
        mock_task_repo = Mock()

        mock_chat_repo.get_conversation.return_value = None

        service = ConversationService(mock_chat_repo, mock_task_repo)
        result = service.get_conversation("nonexistent")

        assert result is None
        mock_chat_repo.get_conversation.assert_called_once_with("nonexistent")

    def test_get_conversations_for_user(self) -> None:
        """Should get all conversations for a user."""
        mock_chat_repo = Mock()
        mock_task_repo = Mock()

        conversations = [
            Conversation(id="conv-1", user_id="user-123", title="Conv 1"),
            Conversation(id="conv-2", user_id="user-123", title="Conv 2"),
        ]
        mock_chat_repo.get_conversations_for_user.return_value = conversations

        service = ConversationService(mock_chat_repo, mock_task_repo)
        result = service.get_conversations_for_user("user-123")

        assert len(result) == 2
        assert result[0].id == "conv-1"
        assert result[1].id == "conv-2"
        mock_chat_repo.get_conversations_for_user.assert_called_once_with("user-123")

    def test_add_user_message(self) -> None:
        """Should add a user message to a conversation."""
        mock_chat_repo = Mock()
        mock_task_repo = Mock()

        message = Message(id="msg-123", role=MessageRole.USER, content="Hello, world!")
        mock_chat_repo.save_message.return_value = message

        service = ConversationService(mock_chat_repo, mock_task_repo)
        result = service.add_user_message("conv-123", "Hello, world!")

        assert result.id == "msg-123"
        assert result.role == MessageRole.USER
        assert result.content == "Hello, world!"
        mock_chat_repo.save_message.assert_called_once()

    def test_add_assistant_message(self) -> None:
        """Should add an assistant message to a conversation."""
        mock_chat_repo = Mock()
        mock_task_repo = Mock()

        message = Message(id="msg-123", role=MessageRole.ASSISTANT, content="Hello, user!")
        mock_chat_repo.save_message.return_value = message

        service = ConversationService(mock_chat_repo, mock_task_repo)
        result = service.add_assistant_message("conv-123", "Hello, user!")

        assert result.id == "msg-123"
        assert result.role == MessageRole.ASSISTANT
        assert result.content == "Hello, user!"
        mock_chat_repo.save_message.assert_called_once()

    def test_add_tool_call_message(self) -> None:
        """Should add a tool call message to a conversation."""
        mock_chat_repo = Mock()
        mock_task_repo = Mock()

        tool_call_data = {
            "name": "add_task",
            "arguments": {"title": "Test task", "user_id": "user-123"},
        }

        message = Message(
            id="msg-123",
            role=MessageRole.TOOL_CALL,
            content="Tool call executed",
            tool_calls=tool_call_data,
        )
        mock_chat_repo.save_message.return_value = message

        service = ConversationService(mock_chat_repo, mock_task_repo)
        result = service.add_tool_call_message("conv-123", tool_call_data)

        assert result.id == "msg-123"
        assert result.role == MessageRole.TOOL_CALL
        assert result.content == "Tool call executed"
        assert result.tool_calls == tool_call_data
        mock_chat_repo.save_message.assert_called_once()

    def test_add_tool_result_message(self) -> None:
        """Should add a tool result message to a conversation."""
        mock_chat_repo = Mock()
        mock_task_repo = Mock()

        tool_result_data = {
            "call_id": "call-123",
            "result": {"success": True, "task": {"id": "task-123"}},
        }

        message = Message(
            id="msg-123",
            role=MessageRole.TOOL_RESULT,
            content="Tool call result",
            tool_results=tool_result_data,
        )
        mock_chat_repo.save_message.return_value = message

        service = ConversationService(mock_chat_repo, mock_task_repo)
        result = service.add_tool_result_message("conv-123", tool_result_data)

        assert result.id == "msg-123"
        assert result.role == MessageRole.TOOL_RESULT
        assert result.content == "Tool call result"
        assert result.tool_results == tool_result_data
        mock_chat_repo.save_message.assert_called_once()

    def test_get_recent_messages(self) -> None:
        """Should get the most recent messages from a conversation."""
        mock_chat_repo = Mock()
        mock_task_repo = Mock()

        recent_messages = [
            Message(id=f"msg-{i}", role=MessageRole.USER, content=f"Message {i}")
            for i in range(5, 15)
        ]
        mock_chat_repo.get_recent_messages_for_conversation.return_value = recent_messages

        service = ConversationService(mock_chat_repo, mock_task_repo)
        result = service.get_recent_messages("conv-123", limit=10)

        assert len(result) == 10
        assert result[0].id == "msg-5"
        assert result[-1].id == "msg-14"
        mock_chat_repo.get_recent_messages_for_conversation.assert_called_once_with("conv-123", 10)

    def test_get_recent_messages_when_fewer_than_limit(self) -> None:
        """Should return all messages when fewer than the limit exist."""
        mock_chat_repo = Mock()
        mock_task_repo = Mock()

        all_messages = [
            Message(id=f"msg-{i}", role=MessageRole.USER, content=f"Message {i}") for i in range(5)
        ]
        mock_chat_repo.get_recent_messages_for_conversation.return_value = all_messages

        service = ConversationService(mock_chat_repo, mock_task_repo)
        result = service.get_recent_messages("conv-123", limit=10)

        assert len(result) == 5
        mock_chat_repo.get_recent_messages_for_conversation.assert_called_once_with("conv-123", 10)

    def test_update_conversation_title(self) -> None:
        """Should update the title of a conversation."""
        mock_chat_repo = Mock()
        mock_task_repo = Mock()

        updated_conversation = Conversation(
            id="conv-123", user_id="user-123", title="Updated Title"
        )
        mock_chat_repo.update_conversation_title.return_value = updated_conversation

        service = ConversationService(mock_chat_repo, mock_task_repo)
        result = service.update_conversation_title("conv-123", "Updated Title")

        assert result is not None
        assert result.id == "conv-123"
        assert result.title == "Updated Title"
        mock_chat_repo.update_conversation_title.assert_called_once_with(
            "conv-123", "Updated Title"
        )

    def test_get_conversation_context(self) -> None:
        """Should get conversation context for the AI agent."""
        mock_chat_repo = Mock()
        mock_task_repo = Mock()

        conversation = Conversation(id="conv-123", user_id="user-123", title="Test Conversation")
        recent_messages = [Message(id="msg-1", role=MessageRole.USER, content="Hello")]

        mock_chat_repo.get_conversation.return_value = conversation
        mock_chat_repo.get_recent_messages_for_conversation.return_value = recent_messages
        mock_chat_repo.get_latest_conversation_summary.return_value = None

        service = ConversationService(mock_chat_repo, mock_task_repo)
        context = service.get_conversation_context("conv-123", max_messages=10)

        assert context["conversation_id"] == "conv-123"
        assert context["user_id"] == "user-123"
        assert len(context["recent_messages"]) == 1
        assert context["summary"] is None
        assert context["has_summary"] is False
        mock_chat_repo.get_recent_messages_for_conversation.assert_called_once_with("conv-123", 10)

    def test_get_conversation_context_with_summary(self) -> None:
        """Should include summary in context when available."""
        mock_chat_repo = Mock()
        mock_task_repo = Mock()

        conversation = Conversation(id="conv-123", user_id="user-123", title="Test Conversation")
        recent_messages = [Message(id="msg-1", role=MessageRole.USER, content="Hello")]

        mock_chat_repo.get_conversation.return_value = conversation
        mock_chat_repo.get_recent_messages_for_conversation.return_value = recent_messages
        mock_chat_repo.get_latest_conversation_summary.return_value = Mock()
        mock_chat_repo.get_latest_conversation_summary.return_value.summary = "Test summary"

        service = ConversationService(mock_chat_repo, mock_task_repo)
        context = service.get_conversation_context("conv-123", max_messages=10)

        assert context["summary"] == "Test summary"
        assert context["has_summary"] is True

    def test_get_conversation_context_raises_error_when_conversation_not_found(
        self,
    ) -> None:
        """Should raise ValueError when conversation is not found."""
        mock_chat_repo = Mock()
        mock_task_repo = Mock()

        mock_chat_repo.get_conversation.return_value = None

        service = ConversationService(mock_chat_repo, mock_task_repo)

        with pytest.raises(ValueError, match="Conversation with ID nonexistent not found"):
            service.get_conversation_context("nonexistent", max_messages=10)
