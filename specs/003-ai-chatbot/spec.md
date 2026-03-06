# Todo AI Chatbot Feature Specification

## Overview
Phase III: Todo AI Chatbot - An AI-powered chatbot for managing todos using natural language, MCP (Model Context Protocol), and OpenAI Agents SDK.

## Objective
Build an AI-powered chatbot for managing todos using natural language, MCP (Model Context Protocol), and OpenAI Agents SDK.

## Core Architecture
- **Backend**: Python FastAPI
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **AI logic**: OpenAI Agents SDK
- **Tool interface**: Official MCP SDK
- **Frontend**: OpenAI ChatKit
- **Authentication**: Better Auth

## Critical Design Requirements

### Stateless Design
- The FastAPI server must be completely stateless
- No conversation, session, or user state may be stored in memory
- Every chat request must reconstruct context from the database
- All user messages, assistant responses, and tool calls must be persisted
- MCP tools must also be stateless and rely exclusively on the database

### Chat Flow
1. Receive POST /api/{user_id}/chat
2. Load conversation summary (if exists)
3. Load the last 10 messages from database
4. Store the new user message
5. Run the OpenAI Agent with MCP tools
6. Persist assistant response, tool calls, and tool results
7. Return response to client
8. Forget everything (ready for next request)

### Conversation Context Rules
- Store all messages in the database
- Only send last 10 messages + optional summary to the agent
- Never load full history into the agent
- Implement summarization when message count exceeds a threshold of 20 messages
- Each user has their own persistent conversation history

### MCP Tooling Requirements
- Implement MCP server using Official MCP SDK
- Expose tools: add_task, list_tasks, complete_task, delete_task, update_task
- Tools must validate user_id ownership
- Tools must read/write tasks using SQLModel
- Tools must return structured outputs exactly as specified

### Agent Behavior
- Use tools whenever task state is involved
- Never hallucinate task state
- Always confirm successful actions conversationally
- Gracefully handle errors (task not found, invalid input)

## Components

### Backend (/backend)
- FastAPI server with stateless design
- OpenAI Agents SDK integration
- MCP server implementation
- Database models for conversations and messages
- Authentication integration

### Frontend (/frontend)
- OpenAI ChatKit UI as a floating widget
- Integration with backend API
- User authentication flow
- Floating button to open/close chat panel overlay
- Branded widget with customizable colors to match application theme

### Database Schema
- Conversations table
- Messages table
- Message types (user, assistant, tool_call, tool_result)
- Conversation summaries

### MCP Tools
- add_task: Create a new task
- list_tasks: Retrieve user's tasks
- complete_task: Mark a task as complete
- delete_task: Remove a task
- update_task: Modify an existing task

## Acceptance Criteria
- Users can interact with the AI chatbot using natural language
- The chatbot can create, read, update, and delete tasks
- All conversations are persisted in the database
- The system handles errors gracefully
- The server remains stateless throughout operation
- MCP tools properly integrate with the existing task management system

## Constraints
- Server must remain stateless at all times
- All user data must be properly authenticated and authorized
- Conversation history must be efficiently managed to prevent performance issues
- MCP tools must follow the official specification

## Non-functional Requirements
- Scalability: Support multiple concurrent users (verified by load tests)
- Performance: Respond to user messages within 2 seconds (p95) as per constitution
- Security: Proper authentication and authorization for all operations
- Reliability: Handle failures gracefully and maintain data integrity

## Clarifications

### Session 2026-02-06
- Q: How should the chatbot UI be presented to users? → A: Widget-based floating UI
- Q: Where should the floating chat button be positioned? → A: Bottom-right corner
- Q: How should the chatbot handle multiple conversations? → A: Per-user persistent widget
- Q: How should the widget be styled? → A: Branded widget with customizable colors

## Interaction & UX Flow
- Floating button triggers the chatbot widget
- Button positioned in bottom-right corner of screen
- Clicking the button opens a chat panel overlay
- User can interact with the AI chatbot in the widget
- Widget can be minimized or closed as needed