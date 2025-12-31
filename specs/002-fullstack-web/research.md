# Research: Phase II - Full-Stack Web Application

## Decision: Technical Stack and Architecture

The application will transition from a single-user console app to a multi-user full-stack web application using the following stack:
- **Frontend**: Next.js 14 (App Router) with Tailwind CSS
- **Backend**: FastAPI 0.100+ with SQLModel
- **Database**: Neon DB (Serverless PostgreSQL)
- **Auth**: JWT (JSON Web Tokens) with OAuth2PasswordBearer
- **Architecture**: Hexagonal (Ports & Adapters)

### Rationale

1. **Multi-User Isolation**: Every table will include a `user_id` field. FastAPI dependency injection will be used to extract the `current_user` from the JWT and automatically scope all database queries to that user.
2. **Next.js App Router**: Provides a robust foundation for building modern, high-performance web interfaces with Server Components for SEO/Initial Load and Client Components for interactivity.
3. **SQLModel**: Combines the power of SQLAlchemy with the simplicity of Pydantic, making it ideal for the domain-driven approach of the project while maintaining strict type safety.
4. **Hexagonal Architecture**: By keeping the domain logic pure and using ports for storage, we can reuse the core business rules from Phase I with minimal modification, only swapping the `InMemoryStorage` adapter for a `SQLModelAdapter`.

### Alternatives Considered

1. **Django**: Rejected because it is too "opinionated" and makes it harder to maintain a pure Hexagonal Architecture compared to the modular approach of FastAPI.
2. **Prisma (Node.js)**: Considered for the backend, but rejected to maintain continuity with the Python-based domain logic developed in Phase I.
3. **Firebase/Supabase**: Rejected to provide more granular control over the service architecture and to demonstrate the transition to a custom backend service.

## Research Findings

### 1. Data Isolation Pattern
- **Pattern**: Repository Pattern with User Context.
- **Implementation**: The repository methods will accept a `user_id` and always include it in the `WHERE` clause.
- **Verification**: Tests will explicitly check that User A cannot retrieve or modify User B's tasks by guessing IDs.

### 2. Authentication Flow
- **Flow**: User login -> Backend issues JWT -> Frontend stores JWT (HttpOnly cookie recommended) -> Frontend includes JWT in `Authorization` header for API calls.
- **FastAPI Integration**: Use `OAuth2PasswordBearer` and a `get_current_user` dependency.

### 3. Frontend Architecture
- **State Management**: Use Next.js Server Actions for mutations and TanStack Query (React Query) for client-side state/caching where appropriate.
- **UI Framework**: Tailwind CSS for responsive, modern styling.

### 4. Testing Strategy
- **Backend BDD**: Use `pytest-bdd` to define user features in Gherkin syntax.
- **Frontend E2E**: Use Playwright for full end-to-end testing of authentication and task management flows.
- **Integration**: Real database tests against a test Neon branch or a local PostgreSQL instance.
