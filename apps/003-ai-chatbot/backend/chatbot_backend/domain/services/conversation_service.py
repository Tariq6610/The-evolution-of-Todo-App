import uuid
from typing import Any

from chatbot_backend.domain.entities.conversation import (
    Conversation,
    ConversationSummary,
)
from chatbot_backend.domain.entities.message import Message, MessageRole
from chatbot_backend.domain.ports.chat_repository_port import ChatRepositoryPort
from chatbot_backend.domain.ports.storage_port import StoragePort


class ConversationService:
    """
    Service class for managing conversations and messages.
    Handles business logic for chat operations.
    """

    def __init__(self, chat_repository: ChatRepositoryPort, task_repository: StoragePort):
        """
        Initialize the ConversationService.

        Args:
            chat_repository: Repository for chat operations
            task_repository: Repository for task operations (for MCP integration)
        """
        self.chat_repository = chat_repository
        self.task_repository = task_repository

    def create_conversation(self, user_id: str, title: str | None = None) -> Conversation:
        """
        Create a new conversation for a user.

        Args:
            user_id: ID of the user creating the conversation
            title: Optional title for the conversation

        Returns:
            Created Conversation object

        Raises:
            ValueError: If user_id is empty or invalid
        """
        if not user_id or not user_id.strip():
            raise ValueError("User ID cannot be empty or whitespace-only")

        return self.chat_repository.create_conversation(user_id, title)

    def get_conversation(self, conversation_id: str) -> Conversation | None:
        """
        Get a conversation by its ID.

        Args:
            conversation_id: ID of the conversation to retrieve

        Returns:
            Conversation object if found, None otherwise
        """
        if not conversation_id or not conversation_id.strip():
            raise ValueError("Conversation ID cannot be empty or whitespace-only")

        return self.chat_repository.get_conversation(conversation_id)

    def get_conversation_with_messages(self, conversation_id: str) -> Conversation | None:
        """
        Get a conversation by its ID with all its messages.

        Args:
            conversation_id: ID of the conversation to retrieve

        Returns:
            Conversation object with messages if found, None otherwise
        """
        if not conversation_id or not conversation_id.strip():
            raise ValueError("Conversation ID cannot be empty or whitespace-only")

        # This method would need to be implemented in the repository
        # For now, we'll get the conversation and then separately get messages
        conversation = self.chat_repository.get_conversation(conversation_id)
        if not conversation:
            return None

        # Get messages separately to avoid circular loading
        messages = self.chat_repository.get_messages_for_conversation(conversation_id)

        # Create a new conversation object with messages
        return Conversation(
            id=conversation.id,
            user_id=conversation.user_id,
            title=conversation.title,
            messages=messages,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
        )

    def get_conversations_for_user(self, user_id: str) -> list[Conversation]:
        """
        Get all conversations for a specific user.

        Args:
            user_id: ID of the user whose conversations to retrieve

        Returns:
            List of Conversation objects
        """
        return self.chat_repository.get_conversations_for_user(user_id)

    def add_user_message(self, conversation_id: str, content: str) -> Message:
        """
        Add a user message to a conversation.

        Args:
            conversation_id: ID of the conversation
            content: Content of the user's message

        Returns:
            Created Message object
        """
        message = Message(id=str(uuid.uuid4()), role=MessageRole.USER, content=content)
        return self.chat_repository.save_message(conversation_id, message)

    def add_assistant_message(self, conversation_id: str, content: str) -> Message:
        """
        Add an assistant message to a conversation.

        Args:
            conversation_id: ID of the conversation
            content: Content of the assistant's message

        Returns:
            Created Message object
        """
        message = Message(id=str(uuid.uuid4()), role=MessageRole.ASSISTANT, content=content)
        return self.chat_repository.save_message(conversation_id, message)

    def add_tool_call_message(self, conversation_id: str, tool_calls: dict[str, Any]) -> Message:
        """
        Add a tool call message to a conversation.

        Args:
            conversation_id: ID of the conversation
            tool_calls: Dictionary containing tool call information

        Returns:
            Created Message object
        """
        message = Message(
            id=str(uuid.uuid4()),
            role=MessageRole.TOOL_CALL,
            content="Tool call executed",
            tool_calls=tool_calls,
        )
        return self.chat_repository.save_message(conversation_id, message)

    def add_tool_result_message(
        self, conversation_id: str, tool_results: dict[str, Any]
    ) -> Message:
        """
        Add a tool result message to a conversation.

        Args:
            conversation_id: ID of the conversation
            tool_results: Dictionary containing tool result information

        Returns:
            Created Message object
        """
        message = Message(
            id=str(uuid.uuid4()),
            role=MessageRole.TOOL_RESULT,
            content="Tool call result",
            tool_results=tool_results,
        )
        return self.chat_repository.save_message(conversation_id, message)

    def get_recent_messages(self, conversation_id: str, limit: int = 10) -> list[Message]:
        """
        Get the most recent messages from a conversation.

        Args:
            conversation_id: ID of the conversation
            limit: Maximum number of messages to return

        Returns:
            List of recent Message objects
        """
        # Use the optimized method to get recent messages directly from the database
        return self.chat_repository.get_recent_messages_for_conversation(conversation_id, limit)

    def update_conversation_title(self, conversation_id: str, title: str) -> Conversation:
        """
        Update the title of a conversation.

        Args:
            conversation_id: ID of the conversation to update
            title: New title for the conversation

        Returns:
            Updated Conversation object
        """
        return self.chat_repository.update_conversation_title(conversation_id, title)

    def create_conversation_summary(
        self, conversation_id: str, summary: str, message_count: int
    ) -> ConversationSummary:
        """
        Create a summary for a conversation.

        Args:
            conversation_id: ID of the conversation
            summary: Text summary of the conversation
            message_count: Number of messages when summary was created

        Returns:
            Created ConversationSummary object
        """
        return self.chat_repository.save_conversation_summary(
            conversation_id, summary, message_count
        )

    def get_conversation_context(
        self, conversation_id: str, max_messages: int = 10
    ) -> dict[str, Any]:
        """
        Get conversation context for the AI agent.

        Args:
            conversation_id: ID of the conversation
            max_messages: Maximum number of recent messages to include

        Returns:
            Dictionary containing conversation context
        """
        conversation = self.chat_repository.get_conversation(conversation_id)
        if not conversation:
            raise ValueError(f"Conversation with ID {conversation_id} not found")

        # Get recent messages
        recent_messages = self.get_recent_messages(conversation_id, max_messages)

        # Get latest summary if available
        summary = self.chat_repository.get_latest_conversation_summary(conversation_id)

        return {
            "conversation_id": conversation_id,
            "user_id": conversation.user_id,
            "recent_messages": recent_messages,
            "summary": summary.summary if summary else None,
            "has_summary": summary is not None,
            "total_messages": len(conversation.messages),
        }
