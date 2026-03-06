"""Unit tests for chat-related entities."""

from datetime import UTC, datetime

from chatbot_backend.domain.entities.conversation import (
    Conversation,
    ConversationSummary,
)
from chatbot_backend.domain.entities.message import Message, MessageRole


class TestConversation:
    """Test cases for Conversation entity."""

    def test_conversation_creation(self) -> None:
        """Should create a Conversation with required fields."""
        conv = Conversation(id="conv-123", user_id="user-123", title="Test Conversation")

        assert conv.id == "conv-123"
        assert conv.user_id == "user-123"
        assert conv.title == "Test Conversation"
        assert isinstance(conv.created_at, datetime)
        assert isinstance(conv.updated_at, datetime)

    def test_conversation_creation_with_defaults(self) -> None:
        """Should create a Conversation with default values."""
        conv = Conversation(id="conv-123", user_id="user-123")

        assert conv.id == "conv-123"
        assert conv.user_id == "user-123"
        assert conv.title is None
        assert isinstance(conv.created_at, datetime)
        assert isinstance(conv.updated_at, datetime)

    def test_conversation_timestamps_auto_generated(self) -> None:
        """Should auto-generate created_at and updated_at timestamps."""
        before = datetime.now(UTC)

        conv = Conversation(id="conv-123", user_id="user-123")

        after = datetime.now(UTC)

        assert before <= conv.created_at <= after
        assert before <= conv.updated_at <= after


class TestConversationSummary:
    """Test cases for ConversationSummary entity."""

    def test_conversation_summary_creation(self) -> None:
        """Should create a ConversationSummary with required fields."""
        summary = ConversationSummary(
            id="summary-123",
            conversation_id="conv-123",
            summary="This is a summary",
            message_count=10,
        )

        assert summary.id == "summary-123"
        assert summary.conversation_id == "conv-123"
        assert summary.summary == "This is a summary"
        assert summary.message_count == 10
        assert isinstance(summary.created_at, datetime)

    def test_conversation_summary_timestamp_auto_generated(self) -> None:
        """Should auto-generate created_at timestamp."""
        before = datetime.now(UTC)

        summary = ConversationSummary(
            id="summary-123",
            conversation_id="conv-123",
            summary="This is a summary",
            message_count=10,
        )

        after = datetime.now(UTC)

        assert before <= summary.created_at <= after


class TestMessage:
    """Test cases for Message entity."""

    def test_message_creation(self) -> None:
        """Should create a Message with required fields."""
        message = Message(id="msg-123", role=MessageRole.USER, content="Hello, world!")

        assert message.id == "msg-123"
        assert message.role == MessageRole.USER
        assert message.content == "Hello, world!"
        assert message.tool_calls is None
        assert message.tool_results is None
        assert isinstance(message.created_at, datetime)

    def test_message_creation_with_tool_calls(self) -> None:
        """Should create a Message with tool calls."""
        tool_calls_data = {
            "name": "add_task",
            "arguments": {"title": "Test task", "user_id": "user-123"},
        }

        message = Message(
            id="msg-123",
            role=MessageRole.TOOL_CALL,
            content="Tool call executed",
            tool_calls=tool_calls_data,
        )

        assert message.id == "msg-123"
        assert message.role == MessageRole.TOOL_CALL
        assert message.content == "Tool call executed"
        assert message.tool_calls == tool_calls_data
        assert message.tool_results is None

    def test_message_creation_with_tool_results(self) -> None:
        """Should create a Message with tool results."""
        tool_results_data = {
            "call_id": "call-123",
            "result": {"success": True, "task": {"id": "task-123"}},
        }

        message = Message(
            id="msg-123",
            role=MessageRole.TOOL_RESULT,
            content="Tool call result",
            tool_results=tool_results_data,
        )

        assert message.id == "msg-123"
        assert message.role == MessageRole.TOOL_RESULT
        assert message.content == "Tool call result"
        assert message.tool_results == tool_results_data
        assert message.tool_calls is None

    def test_message_timestamp_auto_generated(self) -> None:
        """Should auto-generate created_at timestamp."""
        before = datetime.now(UTC)

        message = Message(id="msg-123", role=MessageRole.USER, content="Hello, world!")

        after = datetime.now(UTC)

        assert before <= message.created_at <= after


class TestMessageRoleEnum:
    """Test cases for MessageRole enum values."""

    def test_user_role(self) -> None:
        """Should have USER role value."""
        assert MessageRole.USER.value == "user"

    def test_assistant_role(self) -> None:
        """Should have ASSISTANT role value."""
        assert MessageRole.ASSISTANT.value == "assistant"

    def test_tool_call_role(self) -> None:
        """Should have TOOL_CALL role value."""
        assert MessageRole.TOOL_CALL.value == "tool_call"

    def test_tool_result_role(self) -> None:
        """Should have TOOL_RESULT role value."""
        assert MessageRole.TOOL_RESULT.value == "tool_result"


class TestMessageMethods:
    """Test cases for Message methods and properties."""

    def test_message_has_required_attributes(self) -> None:
        """Should have all required attributes."""
        message = Message(id="msg-123", role=MessageRole.USER, content="Hello, world!")

        # Check that all expected attributes exist
        assert hasattr(message, "id")
        assert hasattr(message, "role")
        assert hasattr(message, "content")
        assert hasattr(message, "tool_calls")
        assert hasattr(message, "tool_results")
        assert hasattr(message, "created_at")

    def test_message_tool_calls_can_be_none(self) -> None:
        """Should allow tool_calls to be None."""
        message = Message(id="msg-123", role=MessageRole.USER, content="Hello, world!")

        assert message.tool_calls is None

    def test_message_tool_results_can_be_none(self) -> None:
        """Should allow tool_results to be None."""
        message = Message(id="msg-123", role=MessageRole.USER, content="Hello, world!")

        assert message.tool_results is None

    def test_different_roles_have_different_values(self) -> None:
        """Should have distinct values for different roles."""
        roles = [
            MessageRole.USER,
            MessageRole.ASSISTANT,
            MessageRole.TOOL_CALL,
            MessageRole.TOOL_RESULT,
        ]
        unique_roles = set(roles)

        assert len(unique_roles) == 4  # All roles are unique
