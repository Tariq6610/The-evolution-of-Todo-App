-- Performance indexes for chat functionality

-- Index on conversation user_id for faster user conversation lookups
CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id);

-- Index on message conversation_id for faster message retrieval by conversation
CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id);

-- Composite index on message conversation_id and created_at for faster chronological message retrieval
CREATE INDEX IF NOT EXISTS idx_messages_conversation_created ON messages(conversation_id, created_at);

-- Index on message created_at for faster recent message queries
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at DESC);

-- Index on conversation summaries conversation_id for faster summary lookups
CREATE INDEX IF NOT EXISTS idx_conversation_summaries_conversation_id ON conversation_summaries(conversation_id);