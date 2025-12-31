# Full-Stack Todo Application

A complete full-stack web application for managing todo tasks with user authentication and persistent storage.

## Tech Stack

### Backend
- **Framework**: FastAPI 0.100+
- **Database**: SQLModel (SQLAlchemy + Pydantic)
- **Database Provider**: Neon (PostgreSQL)
- **Authentication**: JWT-based with bcrypt password hashing
- **Validation**: Pydantic v2
- **Security**: Python-Jose for JWT handling

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Styling**: Tailwind CSS
- **Type Safety**: TypeScript
- **API Client**: Axios with interceptors
- **State Management**: React Context API

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

## Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL (or Neon DB account)

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd apps/002-fullstack-web/backend
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
   # Edit .env with your database URL and JWT secret
   ```

5. Start the backend server:
   ```bash
   uvicorn src.main:app --reload
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd apps/002-fullstack-web/frontend
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
JWT_SECRET_KEY=your-super-secret-jwt-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30
```

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