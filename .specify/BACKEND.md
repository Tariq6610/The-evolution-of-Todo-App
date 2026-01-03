# Backend Agent - Quick Start

**Specialized in backend development using FastAPI, SQLModel, Neon PostgreSQL, and modern Python best practices**

---

## What Was Created

```
✅ Backend Agent Configuration
   → Expert in FastAPI, SQLModel, Neon DB, Pydantic v2
   → Clean architecture (hexagonal, domain layer, repository pattern)
   → Async/await patterns throughout

✅ 4 Backend Skills
   → /sp.backend.create-endpoint - RESTful API endpoints
   → /sp.backend.create-model - SQLModel database models
   → /sp.backend.create-repository - Repository pattern implementation
   → /sp.backend.create-service - Business service layer
   → /sp.backend.create-auth - JWT authentication
```

---

## Agent Capabilities

### Core Technologies

- **FastAPI** - Modern async Python web framework
- **SQLModel** - SQLAlchemy ORM with Pydantic v2 validation
- **Neon PostgreSQL** - Serverless PostgreSQL database
- **Pydantic v2** - Data validation and settings
- **Pytest** - Testing framework with async support
- **Alembic** - Database migrations
- **Uvicorn** - ASGI server for production
- **PyJWT** - JWT authentication tokens

### Design Principles

1. **Hexagonal Architecture** - Domain logic isolated from adapters
2. **Async/Await** - Non-blocking database operations
3. **Transaction Management** - Database integrity
4. **Error Handling** - Consistent responses
5. **API Versioning** - RESTful design patterns
6. **Security** - Input validation, SQL injection prevention
7. **Performance** - Query optimization, connection pooling

---

## Architecture Layers

```
app/api/          # REST API endpoints (FastAPI routers)
├── core/         # Domain layer (business logic, entities)
├── db/           # Database layer (repositories, sessions, models)
└── config/       # Configuration (settings, database)
```

### Layer Responsibilities

| Layer | Purpose | No Dependencies |
|--------|-----------|----------------|
| API | HTTP endpoints, request/response | Domain, DB |
| Core | Business rules, use cases | DB (via repositories) |
| DB | CRUD operations, sessions | Neon PostgreSQL only |

---

## When to Invoke This Agent

Invoke this agent for:

1. **Database Operations**
   > "Create task CRUD operations with SQLModel"
   > "Implement database migrations with Alembic"

2. **API Development**
   > "Create REST API for task management"
   > "Add pagination to task list endpoint"
   > "Implement JWT authentication"

3. **Business Logic**
   > "Implement task filtering and sorting logic"
   > "Add task due date reminders"

4. **Data Modeling**
   > "Design database schema for new feature"
   > "Create relationships between models"

5. **Testing**
   > "Write unit tests for task service"
   > "Create integration tests for API endpoints"

6. **Performance**
   > "Optimize slow database queries"
   > "Add database indexing"
   > "Implement query caching"

---

## How It Works (with UI/UX Agent)

```
Implementation Agent
    │ Backend Work
    │  ↓
Backend Agent executes
    │  ├─→ Creates database models
    │  ├─→ Implements REST API
    │  └─→ Handles business logic
    │
    │ ↓ Needs UI?
    │  ↓
UI/UX Agent invoked
    │  ↓ Creates beautiful UI components
    │  ↓ Integration complete ✅
```

**Backend Agent Role:** Handles all backend/database/logic operations.

---

## Database Best Practices

### Async/Await (Non-Blocking)

```python
# ✅ Good - Async/await for I/O operations
async def get_task(session: Session, task_id: int) -> Task:
    task = await session.get(Task, task_id)
    return task

# ❌ Bad - Blocking database operations
def get_task(session: Session, task_id: int) -> Task:
    task = session.get(Task, task_id)
    return task  # Blocks entire application!
```

### Connection Pooling

```python
# Neon database connection pooling
DATABASE_URL = "postgresql://user:pass@ep-cool-neon-123456.us-east-2.aws.neon.tech/neondb?sslmode=require"

# Async engine with pooling
engine = create_async_engine(DATABASE_URL, pool_size=20, max_overflow=10)
```

---

## API Best Practices

### RESTful Endpoints

```python
# GET /api/v1/tasks - List tasks
# POST /api/v1/tasks - Create task
# GET /api/v1/tasks/{id} - Get specific task
# PUT /api/v1/tasks/{id} - Update task
# DELETE /api/v1/tasks/{id} - Delete task
```

### Query Parameters

```python
# Pagination
GET /api/v1/tasks?skip=0&limit=100

# Filtering
GET /api/v1/tasks?status=pending&priority=high
```

### Error Responses

```python
# Consistent error format
{
    "detail": "Task not found",
    "error_code": "TASK_NOT_FOUND",
    "status": 404
}
```

---

## Skills Created

| Skill | Description |
|-------|-------------|
| `/sp.backend.create-endpoint` | Create RESTful API endpoint |
| `/sp.backend.create-model` | Create SQLModel database model |
| `/sp.backend.create-repository` | Create repository pattern |
| `/sp.backend.create-service` | Create business service |
| `/sp.backend.create-auth` | Add authentication flow |

---

## Skills Reference

### Backend Skills

All backend skills use these patterns:
- Async/await for all I/O operations
- Dependency injection for repositories
- Proper HTTP status codes
- SQL injection prevention (parameterized queries)
- Transaction management for multi-step operations
- Clean error handling
- Type hints everywhere

### Skill Invocation

```
Backend Agent creates:
  - Database models with SQLModel
  - Repositories with CRUD operations
  - Services with business logic
  - API endpoints with FastAPI
  - Authentication with JWT

/sp.implement skill routes tasks appropriately
  → Backend Agent handles backend/database work
  → UI/UX Agent handles UI/UX work
  → Infrastructure Agent validates everything automatically
```

---

## Success Criteria

Backend agent succeeds when:
- ✅ All database operations use async/await
- ✅ API follows RESTful conventions
- ✅ Proper HTTP status codes used
- ✅ Dependencies injected via Depends()
- ✅ SQLModel models with proper relationships
- ✅ Repositories follow domain/repository pattern
- ✅ Input validation with Pydantic
- ✅ Error handling consistent
- ✅ Transactions used for data integrity
- ✅ No SQL injection vulnerabilities
- ✅ Unit tests pass (80%+ coverage)
- ✅ Integration tests pass
- ✅ JWT authentication implemented securely

---

## Full Documentation

- **Agent Info**: `.claude/agents/backend.md`
- **Skills**: `.claude/skills/backend-*.md`

**Status**: ✅ Implemented and Ready
**Version**: 1.0.0
**Date**: 2026-01-01
