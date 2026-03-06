import json
from datetime import UTC, datetime

from sqlmodel import Session, desc, select

from chatbot_backend.adapters.db.chat_models import (
    ConversationSummaryTable,
    ConversationTable,
    MessageTable,
)
from chatbot_backend.domain.entities.conversation import (
    Conversation,
    ConversationSummary,
)
from chatbot_backend.domain.entities.message import Message, MessageRole
from chatbot_backend.domain.ports.chat_repository_port import ChatRepositoryPort


class SQLModelChatRepository(ChatRepositoryPort):
    """
    SQLModel implementation of ChatRepositoryPort.
    Handles database operations for conversations and messages.
    """

    def __init__(self, session: Session):
        self.session = session

    def create_conversation(self, user_id: str, title: str | None = None) -> Conversation:
        """
        Create a new conversation for a user.
        """
        db_conversation = ConversationTable(user_id=user_id, title=title)
        self.session.add(db_conversation)
        self.session.commit()
        self.session.refresh(db_conversation)

        return self._db_conversation_to_domain(db_conversation, include_messages=False)

    def get_conversation(self, conversation_id: str) -> Conversation | None:
        """
        Get a conversation by its ID.
        """
        db_conversation = self.session.get(ConversationTable, conversation_id)
        if not db_conversation:
            return None

        return self._db_conversation_to_domain(db_conversation, include_messages=False)

    def get_conversations_for_user(self, user_id: str) -> list[Conversation]:
        """
        Get all conversations for a specific user.
        """
        statement = select(ConversationTable).where(ConversationTable.user_id == user_id)
        results = self.session.exec(statement)
        conversations = []

        for db_conversation in results:
            conversations.append(
                self._db_conversation_to_domain(db_conversation, include_messages=False)
            )

        return conversations

    def save_message(self, conversation_id: str, message: Message) -> Message:
        """
        Save a message to a conversation.
        """
        # Verify conversation exists
        db_conversation = self.session.get(ConversationTable, conversation_id)
        if not db_conversation:
            raise ValueError(f"Conversation with ID {conversation_id} not found")

        # Prepare tool calls and results as JSON strings
        tool_calls_json = json.dumps(message.tool_calls) if message.tool_calls else None
        tool_results_json = json.dumps(message.tool_results) if message.tool_results else None

        db_message = MessageTable(
            conversation_id=conversation_id,
            role=message.role.value,
            content=message.content,
            tool_calls=tool_calls_json,
            tool_results=tool_results_json,
            created_at=message.created_at,
        )

        self.session.add(db_message)
        self.session.commit()
        self.session.refresh(db_message)

        # Update conversation's updated_at timestamp
        db_conversation.updated_at = datetime.now(UTC)
        self.session.add(db_conversation)
        self.session.commit()

        return self._db_message_to_domain(db_message)

    def get_messages_for_conversation(
        self,
        conversation_id: str,
        limit: int | None = None,
        offset: int | None = 0,
    ) -> list[Message]:
        """
        Get messages for a specific conversation with optimized query.

        Args:
            conversation_id: ID of the conversation
            limit: Maximum number of messages to return
            offset: Number of messages to skip

        Returns:
            List of Message objects, ordered by creation date (oldest first)
        """
        statement = (
            select(MessageTable)
            .where(MessageTable.conversation_id == conversation_id)
            .order_by(MessageTable.created_at)  # type: ignore[arg-type]
        )

        if limit is not None:
            statement = statement.offset(offset).limit(limit)
        elif offset is not None and offset > 0:
            statement = statement.offset(offset)

        results = self.session.exec(statement)
        messages = []

        for db_message in results:
            messages.append(self._db_message_to_domain(db_message))

        return messages

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
        statement = (
            select(MessageTable)
            .where(MessageTable.conversation_id == conversation_id)
            .order_by(desc(MessageTable.created_at))
        )
        statement = statement.limit(limit)

        results = self.session.exec(statement)
        messages = []

        # Since we ordered by desc (most recent first), we get them in reverse chronological order
        # Then reverse to maintain chronological order but with most recent first
        for db_message in results:
            messages.append(self._db_message_to_domain(db_message))

        return messages

    def update_conversation_title(self, conversation_id: str, title: str) -> Conversation:
        """
        Update the title of a conversation.
        """
        db_conversation = self.session.get(ConversationTable, conversation_id)
        if not db_conversation:
            raise ValueError(f"Conversation with ID {conversation_id} not found")

        db_conversation.title = title
        db_conversation.updated_at = datetime.now(UTC)

        self.session.add(db_conversation)
        self.session.commit()
        self.session.refresh(db_conversation)

        return self._db_conversation_to_domain(db_conversation)

    def delete_conversation(self, conversation_id: str) -> bool:
        """
        Delete a conversation.
        """
        db_conversation = self.session.get(ConversationTable, conversation_id)
        if not db_conversation:
            return False

        # Delete all associated messages first
        message_statement = select(MessageTable).where(
            MessageTable.conversation_id == conversation_id
        )
        messages = self.session.exec(message_statement).all()
        for message in messages:
            self.session.delete(message)

        # Delete any associated summaries
        summary_statement = select(ConversationSummaryTable).where(
            ConversationSummaryTable.conversation_id == conversation_id
        )
        summaries = self.session.exec(summary_statement).all()
        for summary in summaries:
            self.session.delete(summary)

        # Finally delete the conversation
        self.session.delete(db_conversation)
        self.session.commit()

        return True

    def save_conversation_summary(
        self, conversation_id: str, summary: str, message_count: int
    ) -> ConversationSummary:
        """
        Save a summary for a conversation.
        """
        # Verify conversation exists
        db_conversation = self.session.get(ConversationTable, conversation_id)
        if not db_conversation:
            raise ValueError(f"Conversation with ID {conversation_id} not found")

        db_summary = ConversationSummaryTable(
            conversation_id=conversation_id,
            summary=summary,
            message_count=message_count,
        )

        self.session.add(db_summary)
        self.session.commit()
        self.session.refresh(db_summary)

        return self._db_summary_to_domain(db_summary)

    def get_latest_conversation_summary(self, conversation_id: str) -> ConversationSummary | None:
        """
        Get the latest summary for a conversation.
        """
        statement = (
            select(ConversationSummaryTable)
            .where(ConversationSummaryTable.conversation_id == conversation_id)
            .order_by(desc(ConversationSummaryTable.created_at))
        )
        statement = statement.limit(1)

        result = self.session.exec(statement).first()
        if not result:
            return None

        return self._db_summary_to_domain(result)

    def _db_conversation_to_domain(
        self, db_conversation: ConversationTable, include_messages: bool = False
    ) -> Conversation:
        """
        Convert database ConversationTable to domain Conversation.

        Args:
            db_conversation: The database conversation object
            include_messages: Whether to include messages in the domain object (expensive operation)
        """
        messages = []
        if include_messages:
            # Only load messages when explicitly requested
            messages = self.get_messages_for_conversation(db_conversation.id)

        return Conversation(
            id=db_conversation.id,
            user_id=db_conversation.user_id,
            title=db_conversation.title,
            messages=messages,
            created_at=db_conversation.created_at,
            updated_at=db_conversation.updated_at,
        )

    def _db_message_to_domain(self, db_message: MessageTable) -> Message:
        """
        Convert database MessageTable to domain Message.
        """
        # Parse JSON fields
        tool_calls = json.loads(db_message.tool_calls) if db_message.tool_calls else None
        tool_results = json.loads(db_message.tool_results) if db_message.tool_results else None

        return Message(
            id=db_message.id,
            role=MessageRole(db_message.role),
            content=db_message.content,
            tool_calls=tool_calls,
            tool_results=tool_results,
            created_at=db_message.created_at,
        )

    def _db_summary_to_domain(self, db_summary: ConversationSummaryTable) -> ConversationSummary:
        """
        Convert database ConversationSummaryTable to domain ConversationSummary.
        """
        return ConversationSummary(
            id=db_summary.id,
            conversation_id=db_summary.conversation_id,
            summary=db_summary.summary,
            message_count=db_summary.message_count,
            created_at=db_summary.created_at,
        )
