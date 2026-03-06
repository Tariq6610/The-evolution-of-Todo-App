from datetime import UTC, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class MessageRole(str, Enum):
    """
    Role of the message in the conversation.
    """

    USER = "user"
    ASSISTANT = "assistant"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"


class Message(BaseModel):
    """
    Message entity for AI chatbot conversations.

    Attributes:
        id: Unique message identifier (UUID string format)
        role: Role of the message sender (user, assistant, tool_call, tool_result)
        content: Text content of the message
        tool_calls: Optional structured data for tool calls
        tool_results: Optional structured data for tool call results
        created_at: Timestamp when message was created
    """

    id: str = Field(..., description="Unique message identifier (UUID)")
    role: MessageRole = Field(..., description="Role of the message sender")
    content: str | None = Field(default=None, description="Text content of the message")
    tool_calls: dict[str, Any] | None = Field(
        default=None, description="Structured data for tool calls"
    )
    tool_results: dict[str, Any] | None = Field(
        default=None, description="Structured data for tool call results"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Creation timestamp",
    )
