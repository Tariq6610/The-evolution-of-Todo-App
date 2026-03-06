from datetime import UTC, datetime

from pydantic import BaseModel, Field

from .message import Message


class Conversation(BaseModel):
    """
    Conversation entity for AI chatbot.

    Attributes:
        id: Unique conversation identifier (UUID string format)
        user_id: Identifier of the user who owns this conversation
        title: Optional title for the conversation
        messages: List of messages in the conversation
        created_at: Timestamp when conversation was created
        updated_at: Timestamp when conversation was last modified
    """

    id: str = Field(..., description="Unique conversation identifier (UUID)")
    user_id: str = Field(..., description="Identifier of the user who owns this conversation")
    title: str | None = Field(default=None, description="Optional title for the conversation")
    messages: list[Message] = Field(
        default_factory=list, description="List of messages in the conversation"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Creation timestamp",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Last update timestamp",
    )


class ConversationSummary(BaseModel):
    """
    Conversation summary entity for managing long conversations.

    Attributes:
        id: Unique summary identifier (UUID string format)
        conversation_id: Reference to the conversation being summarized
        summary: Text summary of the conversation
        message_count: Number of messages when summary was created
        created_at: Timestamp when summary was created
    """

    id: str = Field(..., description="Unique summary identifier (UUID)")
    conversation_id: str = Field(..., description="Reference to the conversation being summarized")
    summary: str = Field(..., description="Text summary of the conversation")
    message_count: int = Field(..., description="Number of messages when summary was created")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Creation timestamp",
    )
