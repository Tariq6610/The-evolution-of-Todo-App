from abc import ABC, abstractmethod

from chatbot_backend.domain.entities.conversation import (
    Conversation,
    ConversationSummary,
)
from chatbot_backend.domain.entities.message import Message


class ChatRepositoryPort(ABC):
    """
    Abstract port for chat repository operations.
    Defines the interface for storing and retrieving chat conversations and messages.
    """

    @abstractmethod
    def create_conversation(self, user_id: str, title: str | None = None) -> Conversation:
        """
        Create a new conversation for a user.

        Args:
            user_id: ID of the user creating the conversation
            title: Optional title for the conversation

        Returns:
            Created Conversation object
        """
        pass

    @abstractmethod
    def get_conversation(self, conversation_id: str) -> Conversation | None:
        """
        Get a conversation by its ID.

        Args:
            conversation_id: ID of the conversation to retrieve

        Returns:
            Conversation object if found, None otherwise
        """
        pass

    @abstractmethod
    def get_conversations_for_user(self, user_id: str) -> list[Conversation]:
        """
        Get all conversations for a specific user.

        Args:
            user_id: ID of the user whose conversations to retrieve

        Returns:
            List of Conversation objects
        """
        pass

    @abstractmethod
    def save_message(self, conversation_id: str, message: Message) -> Message:
        """
        Save a message to a conversation.

        Args:
            conversation_id: ID of the conversation to add the message to
            message: Message object to save

        Returns:
            Saved Message object
        """
        pass

    @abstractmethod
    def get_messages_for_conversation(
        self,
        conversation_id: str,
        limit: int | None = None,
        offset: int | None = 0,
    ) -> list[Message]:
        """
        Get messages for a specific conversation.

        Args:
            conversation_id: ID of the conversation
            limit: Maximum number of messages to return (None for all)
            offset: Number of messages to skip

        Returns:
            List of Message objects
        """
        pass

    @abstractmethod
    def get_recent_messages_for_conversation(
        self, conversation_id: str, limit: int = 10
    ) -> list[Message]:
        """
        Get the most recent messages for a specific conversation.

        Args:
            conversation_id: ID of the conversation
            limit: Maximum number of recent messages to return (default 10)

        Returns:
            List of Message objects, ordered with most recent first
        """
        pass

    @abstractmethod
    def update_conversation_title(self, conversation_id: str, title: str) -> Conversation:
        """
        Update the title of a conversation.

        Args:
            conversation_id: ID of the conversation to update
            title: New title for the conversation

        Returns:
            Updated Conversation object
        """
        pass

    @abstractmethod
    def delete_conversation(self, conversation_id: str) -> bool:
        """
        Delete a conversation.

        Args:
            conversation_id: ID of the conversation to delete

        Returns:
            True if deletion was successful, False otherwise
        """
        pass

    @abstractmethod
    def save_conversation_summary(
        self, conversation_id: str, summary: str, message_count: int
    ) -> ConversationSummary:
        """
        Save a summary for a conversation.

        Args:
            conversation_id: ID of the conversation to summarize
            summary: Text summary of the conversation
            message_count: Number of messages when summary was created

        Returns:
            Created ConversationSummary object
        """
        pass

    @abstractmethod
    def get_latest_conversation_summary(self, conversation_id: str) -> ConversationSummary | None:
        """
        Get the latest summary for a conversation.

        Args:
            conversation_id: ID of the conversation

        Returns:
            Latest ConversationSummary object if found, None otherwise
        """
        pass
