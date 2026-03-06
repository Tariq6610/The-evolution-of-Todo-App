import uuid
from datetime import UTC, datetime
from enum import Enum

from sqlmodel import Field, Relationship, SQLModel


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"


class ConversationTable(SQLModel, table=True):
    __tablename__ = "conversations"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(sa_column_kwargs={"nullable": False})
    title: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # Relationship to messages
    messages: list["MessageTable"] = Relationship(back_populates="conversation")


class MessageTable(SQLModel, table=True):
    __tablename__ = "messages"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    conversation_id: str = Field(foreign_key="conversations.id", nullable=False)
    role: str = Field(sa_column_kwargs={"nullable": False})  # MessageRole enum value
    content: str | None = Field(default=None)
    tool_calls: str | None = Field(default=None)  # JSON string for tool calls
    tool_results: str | None = Field(default=None)  # JSON string for tool results
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # Relationship to conversation
    conversation: ConversationTable = Relationship(back_populates="messages")


class ConversationSummaryTable(SQLModel, table=True):
    __tablename__ = "conversation_summaries"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    conversation_id: str = Field(foreign_key="conversations.id", nullable=False)
    summary: str = Field(sa_column_kwargs={"nullable": False})
    message_count: int = Field(sa_column_kwargs={"nullable": False})
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # Relationship to conversation
    conversation: ConversationTable = Relationship()
