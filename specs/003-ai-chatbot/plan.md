# Todo AI Chatbot Implementation Plan

## Architecture Overview

### System Components
- **Frontend**: OpenAI ChatKit-based UI integrated with the existing Todo app
- **Backend**: FastAPI server with OpenAI Agents SDK integration
- **MCP Server**: Model Context Protocol server for task management tools
- **Database**: Neon PostgreSQL with tables for conversations and messages
- **Authentication**: Integration with Better Auth system

### Service Boundaries
- **Chat Service**: Handles conversation flow and persistence
- **MCP Service**: Provides tools for task management operations
- **Storage Service**: Manages conversation and message persistence
- **Authentication Service**: Validates user permissions

## Technical Implementation

### Backend Architecture (Python/FastAPI)

#### Core Services
1. **Conversation Manager**
   - Loads conversation history from database
   - Maintains conversation context
   - Handles message persistence

2. **Agent Orchestrator**
   - Integrates with OpenAI Agents SDK
   - Coordinates tool usage
   - Manages conversation flow

3. **MCP Server**
   - Implements MCP protocol
   - Exposes task management tools
   - Validates user permissions

#### Database Schema
```sql
-- Conversations table
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Messages table
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id),
    role VARCHAR(50) NOT NULL, -- 'user', 'assistant', 'tool_call', 'tool_result'
    content TEXT,
    tool_calls JSONB, -- for tool call messages
    tool_results JSONB, -- for tool result messages
    created_at TIMESTAMP DEFAULT NOW()
);

-- Conversation Summaries table
CREATE TABLE conversation_summaries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id),
    summary TEXT,
    message_count INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Frontend Architecture (OpenAI ChatKit)

#### UI Components
1. **Chat Interface**
   - Real-time message display
   - Typing indicators
   - Error handling

2. **Conversation History**
   - List of past conversations
   - Ability to switch between conversations

3. **Authentication Integration**
   - User login/logout
   - Session management

### MCP Tool Specifications

#### Tool: add_task
- **Description**: Creates a new task
- **Parameters**:
  - title (string, required)
  - description (string, optional)
  - priority (enum: low, medium, high, optional)
  - due_date (string, ISO format, optional)
- **Returns**: Created task object

#### Tool: list_tasks
- **Parameters**:
  - status (enum: all, pending, completed, optional)
  - priority (enum: all, low, medium, high, optional)
  - limit (integer, optional)
  - offset (integer, optional)
- **Returns**: Array of task objects

#### Tool: complete_task
- **Parameters**:
  - task_id (string, required)
- **Returns**: Updated task object

#### Tool: delete_task
- **Parameters**:
  - task_id (string, required)
- **Returns**: Boolean indicating success

#### Tool: update_task
- **Parameters**:
  - task_id (string, required)
  - title (string, optional)
  - description (string, optional)
  - status (enum: pending, completed, optional)
  - priority (enum: low, medium, high, optional)
  - due_date (string, ISO format, optional)
- **Returns**: Updated task object

## Implementation Phases

### Phase 1: Infrastructure Setup
- Set up project structure with backend and frontend directories
- Configure database connections
- Set up authentication integration
- Implement basic conversation persistence

### Phase 2: MCP Server Development
- Implement MCP protocol server
- Create task management tools
- Integrate with existing task database
- Add user validation and permissions

### Phase 3: Agent Integration
- Integrate OpenAI Agents SDK
- Connect agent with MCP tools
- Implement conversation flow
- Add message persistence

### Phase 4: Frontend Development
- Integrate OpenAI ChatKit
- Connect to backend API
- Implement conversation history
- Add authentication flows

### Phase 5: Testing and Optimization
- Unit tests for all components
- Integration tests
- Performance optimization
- Error handling improvements

## State Management Strategy

### Stateless Server Design
- All state stored in database
- Conversation context reconstructed on each request
- No in-memory session state
- MCP tools operate statelessly

### Conversation Context Management
- Last N messages loaded per request (configurable)
- Conversation summaries created when message count exceeds threshold
- Efficient querying for conversation history
- Automatic cleanup of old conversations (if needed)

## Security Considerations
- User authentication for all API endpoints
- Authorization checks for all operations
- Input validation for all user inputs
- SQL injection prevention with parameterized queries
- Rate limiting for API endpoints

## Performance Considerations
- Database indexing for efficient queries
- Connection pooling for database access
- Efficient message loading (pagination)
- Caching for frequently accessed data (if needed)

## Deployment Strategy
- Containerized deployment with Docker
- Environment-specific configurations
- Health check endpoints
- Monitoring and logging setup