# Data Model: Phase II - Full-Stack Web Application

## Entities

### User
Represents an authenticated user account.
- **id**: UUID (Primary Key)
- **email**: String (Unique, Indexed)
- **password_hash**: String
- **full_name**: Optional[String]
- **is_active**: Boolean (Default: True)
- **created_at**: DateTime (UTC)
- **updated_at**: DateTime (UTC)

### Task
Represents a todo item belonging to a user.
- **id**: UUID (Primary Key)
- **user_id**: UUID (Foreign Key -> User.id, Indexed)
- **title**: String (1-500 chars, Required)
- **description**: Optional[String]
- **status**: Enum (TaskStatus: pending | completed)
- **priority**: Enum (Priority: low | medium | high)
- **tags**: List[String] (JSONB in Postgres)
- **due_date**: Optional[DateTime]
- **created_at**: DateTime (UTC)
- **updated_at**: DateTime (UTC)

## Relationships

- **User -> Task**: 1-to-Many
  - A user can have many tasks.
  - A task belongs to exactly one user.
  - Deleting a user should cascade delete their tasks (or archive them).

## State Transitions

### Task Status
- **PENDING**: Initial state upon creation.
- **COMPLETED**: Task marked as finished. User can toggle back to PENDING.

## Validation Rules

1. **User Registration**:
   - Email must be valid format.
   - Password must meet complexity requirements (handled by service layer).
2. **Task Creation**:
   - Title cannot be empty or whitespace-only.
   - User ID must exist and belong to the authenticated session.
3. **Task Modification**:
   - Only the owner (user_id) can modify or delete a task.
   - Timestamps must update on every modification.
