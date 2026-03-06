# Todo AI Chatbot - Phase III

A complete full-stack web application with AI-powered chatbot for managing todo tasks with user authentication and persistent storage.

## Tech Stack

### Backend
- **Framework**: FastAPI 0.100+
- **Database**: SQLModel (SQLAlchemy + Pydantic)
- **Database Provider**: Neon (PostgreSQL)
- **Authentication**: JWT-based with bcrypt password hashing
- **Validation**: Pydantic v2
- **Security**: Python-Jose for JWT handling
- **AI Integration**: OpenAI Agents SDK
- **MCP (Model Context Protocol)**: Custom implementation

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Styling**: Tailwind CSS
- **Type Safety**: TypeScript
- **API Client**: Axios with interceptors
- **State Management**: React Context API

## New AI Chatbot Features

### AI-Powered Task Management
- Natural language processing for task creation, updates, and management
- Integration with OpenAI Agents SDK for intelligent responses
- MCP (Model Context Protocol) tools for task operations

### MCP Tools Available
- `add_task`: Create new tasks using natural language
- `list_tasks`: Retrieve user's tasks with filtering options
- `complete_task`: Mark tasks as complete
- `delete_task`: Remove tasks from the list
- `update_task`: Modify existing task details

### Conversation Management
- Persistent conversation history
- Context-aware responses
- Conversation summaries for long interactions
- Real-time WebSocket support

## Architecture

The application follows Hexagonal Architecture (Ports and Adapters pattern):

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Layer      │    │   Database      │
│   (React)       │◄──►│   (FastAPI)      │◄──►│   (PostgreSQL)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                               │
                        ┌──────────────────┐
                        │  Domain Layer    │
                        │  (Pure Business │
                        │   Logic)         │
                        └──────────────────┘
```

## Features

### User Authentication
- User registration with email validation
- Secure login with JWT tokens
- Password hashing with bcrypt
- Session management via localStorage

### Task Management
- Create, read, update, and delete tasks
- Toggle task completion status
- Task prioritization (low, medium, high)
- Task descriptions and tagging

### AI Chatbot Features
- Natural language task management
- Context-aware conversations
- Persistent conversation history
- Real-time chat interface

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login existing user

### Tasks
- `GET /api/v1/tasks/` - Get all tasks for authenticated user
- `POST /api/v1/tasks/` - Create new task
- `GET /api/v1/tasks/{id}` - Get specific task
- `PUT /api/v1/tasks/{id}` - Update task
- `DELETE /api/v1/tasks/{id}` - Delete task
- `PATCH /api/v1/tasks/{id}/toggle-status` - Toggle task status

### Chat
- `POST /api/v1/chat/{user_id}` - Send message to AI assistant
- `GET /api/v1/chat/conversations/{user_id}` - Get user's conversations
- `GET /api/v1/chat/conversation/{conversation_id}` - Get specific conversation
- `WS /api/v1/chat/ws/{user_id}` - Real-time WebSocket chat

## Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- Neon DB account (recommended) or PostgreSQL
- OpenAI API key

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd apps/003-ai-chatbot/backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database URL, JWT secret, and OpenAI API key
   ```

5. Start the backend server:
   ```bash
   uvicorn src.main:app --reload
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd apps/003-ai-chatbot/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API URL
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db
# For Neon DB, use the connection string from your Neon dashboard:
# DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
JWT_SECRET_KEY=your-super-secret-jwt-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30
OPENAI_API_KEY=your-openai-api-key
```

### Neon DB Setup
1. Create a free Neon account at [neon.tech](https://neon.tech)
2. Create a new project in the Neon dashboard
3. Copy the connection string from the "Connection Details" section
4. Update your `.env` file with the Neon DB connection string
5. The application automatically handles SSL requirements for Neon DB connections

### Frontend (.env)
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## Development

### Backend
- Code formatted with Ruff
- Type-checked with mypy
- Run tests with pytest

### Frontend
- Code formatted with ESLint and Prettier
- Type-checked with TypeScript
- Run tests with Jest/React Testing Library

## Testing Strategy

The application follows a BDD + Test-Along strategy:
- Unit tests for domain models and services
- Integration tests for API endpoints
- Component tests for UI elements
- End-to-end tests for user flows

## Security
- Passwords are hashed using bcrypt (max 72 bytes)
- JWT tokens with configurable expiration
- Input validation with Pydantic
- SQL injection prevention via SQLModel/SQLAlchemy
- CORS configured for frontend integration

## Deployment
The application is designed to be deployed with:
- Backend: Any Python WSGI/ASGI hosting (Heroku, AWS, etc.)
- Frontend: Static hosting (Vercel, Netlify, etc.)
- Database: Neon DB or any PostgreSQL provider

## Docker Deployment

For easier local development and deployment, we provide a Docker Compose configuration that sets up all services.

### Prerequisites
- Docker Engine (v20.10.0 or later)
- Docker Compose (v2.0.0 or later)
- OpenAI API key

### Setup
1. Copy the example environment files:
   ```bash
   cd backend
   cp .env.example .env
   cd ../frontend
   cp .env.local.example .env.local
   cd ..
   ```

2. Configure your environment variables:
   - Edit `backend/.env` and set your OpenAI API key
   - Edit `frontend/.env.local` if needed

3. Build and start the services:
   ```bash
   docker-compose up --build
   ```

### Services
- **Frontend**: Access the chat interface at `http://localhost:4000`
- **Backend API**: The API is available at `http://localhost:7860`
- **Database**: PostgreSQL is accessible at `localhost:5434` (internally at `db:5432`)

### Commands
- Start services: `docker-compose up --build`
- Start in detached mode: `docker-compose up --build -d`
- Stop services: `docker-compose down`
- View logs: `docker-compose logs -f`
- Rebuild and restart: `docker-compose up --build --force-recreate`