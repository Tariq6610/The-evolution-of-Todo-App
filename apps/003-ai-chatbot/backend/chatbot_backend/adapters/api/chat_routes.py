import os
from typing import Any

from fastapi import APIRouter, Depends, WebSocket
from pydantic import BaseModel
from sqlmodel import Session

from chatbot_backend.adapters.db.chat_repository import SQLModelChatRepository
from chatbot_backend.adapters.db.session import get_session
from chatbot_backend.adapters.db.task_repository import SQLModelTaskRepository
from chatbot_backend.adapters.mcp.server import MCPServer
from chatbot_backend.domain.services.conversation_service import ConversationService
from chatbot_backend.domain.services.todo_service import TodoService

try:
    from openai import OpenAI
except ImportError:
    # Fallback for environments without openai installed
    class OpenAI:  # type: ignore[no-redef]
        def __init__(self, **kwargs: Any):
            pass


import json

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str


def get_conversation_service(
    session: Session = Depends(get_session),
) -> ConversationService:
    """
    Dependency to get the conversation service.
    """
    chat_repo = SQLModelChatRepository(session)
    task_repo = SQLModelTaskRepository(session)
    return ConversationService(chat_repo, task_repo)


def get_todo_service(session: Session = Depends(get_session)) -> TodoService:
    """
    Dependency to get the todo service.
    """
    task_repo = SQLModelTaskRepository(session)
    return TodoService(task_repo)


@router.post("/{user_id}")
async def chat(
    user_id: str,
    request: ChatRequest,
    conversation_service: ConversationService = Depends(get_conversation_service),
    todo_service: TodoService = Depends(get_todo_service),
) -> dict[str, Any]:
    """
    Handle a chat message from a user.
    This endpoint processes the user's message and returns a response from the AI agent.
    """
    message = request.message
    try:
        # Validate inputs
        if not user_id or not user_id.strip():
            return {"error": "User ID is required and cannot be empty"}

        if not message or not message.strip():
            return {"error": "Message is required and cannot be empty"}

        # Get or create a conversation for this user
        try:
            conversations = conversation_service.get_conversations_for_user(user_id)
        except Exception as e:
            return {"error": f"Failed to retrieve conversations: {str(e)}"}

        if conversations:
            # Use the most recent conversation
            conversation = conversations[0]  # Get most recent
        else:
            # Create a new conversation
            try:
                conversation = conversation_service.create_conversation(user_id, "New Conversation")
            except Exception as e:
                return {"error": f"Failed to create conversation: {str(e)}"}

        # Add the user's message to the conversation
        try:
            conversation_service.add_user_message(conversation.id, message)
        except Exception as e:
            return {"error": f"Failed to add user message: {str(e)}"}

        # Initialize the OpenAI client for Gemini
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            return {"error": "Gemini API key not configured"}

        openai_client = OpenAI(
            api_key=gemini_api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )

        # Get recent messages for context
        try:
            recent_messages = conversation_service.get_recent_messages(conversation.id, limit=10)
        except Exception as e:
            return {"error": f"Failed to retrieve recent messages: {str(e)}"}

        # Prepare messages for the AI agent
        ai_messages = []
        for msg in recent_messages:
            if msg.role.value == "user" and msg.content:
                ai_messages.append({"role": "user", "content": msg.content})
            elif msg.role.value == "assistant" and msg.content:
                ai_messages.append({"role": "assistant", "content": msg.content})

        # Add the current user message
        ai_messages.append({"role": "user", "content": message})

        # Initialize MCP server for tool access
        try:
            mcp_server = MCPServer(todo_service)
        except Exception as e:
            return {"error": f"Failed to initialize MCP server: {str(e)}"}

        # Define available tools for the agent
        try:
            tools = mcp_server.get_tool_specification()["tools"]
        except Exception as e:
            return {"error": f"Failed to get tool specifications: {str(e)}"}

        # Get tool definitions for OpenAI
        openai_tools = []
        for tool in tools:
            # Convert MCP tool specification to OpenAI format
            openai_tool = {
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": tool["input_schema"],
                },
            }
            openai_tools.append(openai_tool)

        # Process the response
        try:
            # Call the OpenAI agent with tools
            response = openai_client.chat.completions.create(
                model="gemini-2.0-flash",  # Using Gemini model via OpenAI SDK
                messages=ai_messages,
                tools=openai_tools,
                tool_choice="auto",
            )

            # Process the response
            response_message = response.choices[0].message

            # If the agent wants to call a tool
            if response_message.tool_calls:
                ai_messages.append(response_message.model_dump(exclude_none=True))
                # Process each tool call
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    try:
                        function_args = json.loads(tool_call.function.arguments)
                    except json.JSONDecodeError as e:
                        return {"error": f"Failed to parse tool arguments: {str(e)}"}

                    # Add the tool call to the conversation
                    try:
                        conversation_service.add_tool_call_message(
                            conversation.id,
                            {"name": function_name, "arguments": function_args},
                        )
                    except Exception as e:
                        return {"error": f"Failed to add tool call message: {str(e)}"}

                    # Execute the tool
                    user_id_from_context = (
                        user_id  # In a real app, this would come from auth context
                    )
                    tool_params = {**function_args, "user_id": user_id_from_context}

                    try:
                        tool_result = await mcp_server.execute_tool(function_name, tool_params)
                    except Exception as e:
                        # Log the error but continue
                        tool_result = {"error": f"Tool execution failed: {str(e)}"}

                    # Add the tool result to the conversation
                    try:
                        conversation_service.add_tool_result_message(
                            conversation.id,
                            {"call_id": tool_call.id, "result": tool_result},
                        )
                    except Exception as e:
                        return {"error": f"Failed to add tool result message: {str(e)}"}

                    # Now call the model again with the tool result
                    ai_messages.append(
                        {
                            "role": "tool",
                            "content": json.dumps(tool_result),
                            "tool_call_id": tool_call.id,
                            "name": function_name,
                        }
                    )

                # Get final response from AI with tool results
                try:
                    final_response = openai_client.chat.completions.create(
                        model="gemini-2.0-flash",
                        messages=ai_messages,
                        tools=openai_tools,
                        tool_choice="none",  # Don't call tools again
                    )

                    final_content = final_response.choices[0].message.content or ""

                    # Add the assistant's final response to the conversation
                    conversation_service.add_assistant_message(conversation.id, final_content)

                    return {
                        "conversation_id": conversation.id,
                        "response": final_content,
                        "tool_calls_executed": len(response_message.tool_calls),
                    }
                except Exception as e:
                    return {"error": f"Failed to get final response from AI: {str(e)}"}
            else:
                # No tool calls, just return the assistant's response
                assistant_content = response_message.content
                try:
                    conversation_service.add_assistant_message(conversation.id, assistant_content)
                except Exception as e:
                    return {"error": f"Failed to add assistant message: {str(e)}"}

                return {
                    "conversation_id": conversation.id,
                    "response": assistant_content,
                    "tool_calls_executed": 0,
                }

        except Exception as e:
            # In case of error, add an error message to the conversation
            error_message = f"Sorry, I encountered an error: {str(e)}"
            try:
                conversation_service.add_assistant_message(conversation.id, error_message)
            except Exception as inner_e:
                # If we can't even add the error message, log it
                print(f"Could not add error message to conversation: {inner_e}")

            return {
                "conversation_id": conversation.id,
                "response": error_message,
                "error": str(e),
            }

    except Exception as e:
        # Catch-all error handler
        return {"error": f"Unexpected error occurred: {str(e)}"}


@router.get("/conversations/{user_id}")
async def get_user_conversations(
    user_id: str,
    conversation_service: ConversationService = Depends(get_conversation_service),
) -> dict[str, Any]:
    """
    Get all conversations for a user.
    """
    conversations = conversation_service.get_conversations_for_user(user_id)
    return {"conversations": conversations}


@router.get("/conversation/{conversation_id}")
async def get_conversation(
    conversation_id: str,
    conversation_service: ConversationService = Depends(get_conversation_service),
) -> dict[str, Any]:
    """
    Get a specific conversation by ID.
    """
    conversation = conversation_service.get_conversation(conversation_id)
    if not conversation:
        return {"error": "Conversation not found"}

    return {"conversation": conversation}


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: str,
    todo_service: TodoService = Depends(get_todo_service),
) -> None:
    """
    WebSocket endpoint for real-time chat with MCP integration.
    """
    mcp_server = MCPServer(todo_service)
    await mcp_server.handle_websocket_connection(websocket)
