---
description: "Task list for Phase II implementation: Full-Stack Web Application"
---

# Tasks: Phase II - Full-Stack Web Application

**Input**: Design documents from `/specs/002-fullstack-web/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: BDD + Test-Along strategy is REQUIRED by constitution - tests must be written to verify user flows.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, etc.)
- Include exact file paths in descriptions

## Path Conventions

- **Mono-repo Snapshot**: `apps/002-fullstack-web/backend/`, `apps/002-fullstack-web/frontend/`
- All paths below are relative to `apps/002-fullstack-web/` unless otherwise specified.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create backend/ and frontend/ directory structure
- [x] T002 Initialize FastAPI backend with SQLModel and Pydantic v2
- [x] T003 Initialize Next.js 14 frontend with Tailwind CSS and TypeScript
- [x] T004 [P] Configure ruff and mypy for backend/ in pyproject.toml
- [x] T005 [P] Configure ESLint and Prettier for frontend/
- [x] T006 [P] Setup environment variable handling (.env) for both stacks

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T007 Configure Neon DB connection and SQLModel engine in backend/src/adapters/db/session.py
- [x] T008 [P] Setup FastAPI application and routing structure in backend/src/main.py
- [x] T009 [P] Implement Hexagonal ports/adapters structure for backend/ (shared with Phase I logic)
- [x] T010 [P] Setup Next.js app directory and basic layout in frontend/src/app/layout.tsx
- [x] T011 [P] Implement API client service module in frontend/src/services/api_client.ts
- [x] T012 Implement base error handling and logging for both stacks

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Registration & Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable users to create accounts and log in securely via JWT

**Independent Test**: Register a new user, log in, and verify the JWT is stored and used for subsequent requests.

### Tests for User Story 1 (BDD)

- [ ] T013 [P] [US1] Write Gherkin feature for Auth flows in frontend/tests/features/auth.feature
- [ ] T014 [P] [US1] Write failing unit tests for User model in backend/tests/unit/domain/test_user.py
- [ ] T015 [P] [US1] Write failing integration tests for Auth endpoints in backend/tests/integration/test_auth.py

### Implementation for User Story 1

- [x] T016 [P] [US1] Create User entity and SQLModel in backend/src/domain/entities/user.py
- [x] T017 [P] [US1] Implement password hashing utility in backend/src/adapters/security/password.py
- [x] T018 [P] [US1] Implement JWT token generation/validation in backend/src/adapters/security/jwt.py
- [x] T019 [US1] Implement AuthService and registration/login logic in backend/src/domain/services/auth_service.py
- [x] T020 [US1] Implement registration and login endpoints in backend/src/adapters/api/auth_routes.py
- [x] T021 [US1] Create Registration page in frontend/src/app/register/page.tsx
- [x] T022 [US1] Create Login page in frontend/src/app/login/page.tsx
- [x] T023 [US1] Implement Auth context/state management in frontend/src/context/auth_context.tsx

**Checkpoint**: Authentication system functional - can now proceed to task management

---

## Phase 4: User Story 2 - Task CRUD Operations (Priority: P1) 🎯 MVP

**Goal**: Enable multi-user persistent task management with data isolation

**Independent Test**: Create, view, update, and delete tasks under one user, verify they are stored in Neon DB and invisible to other users.

### Tests for User Story 2 (BDD)

- [ ] T024 [P] [US2] Write Gherkin feature for Task CRUD in frontend/tests/features/tasks.feature
- [ ] T025 [P] [US2] Write failing unit tests for Task entity (extended) in backend/tests/unit/domain/test_task.py
- [ ] T026 [P] [US2] Write failing integration tests for Task endpoints in backend/tests/integration/test_tasks.py

### Implementation for User Story 2

- [x] T027 [P] [US2] Update Task entity with user_id and persistence in backend/src/domain/entities/task.py
- [x] T028 [P] [US2] Implement TaskRepository using SQLModel in backend/src/adapters/db/task_repository.py
- [x] T029 [US2] Implement TaskService with multi-user isolation in backend/src/domain/services/task_service.py
- [x] T030 [US2] Implement Task CRUD endpoints with JWT protection in backend/src/adapters/api/task_routes.py
- [x] T031 [US2] Create Task List dashboard in frontend/src/app/dashboard/page.tsx
- [ ] T032 [US2] Create Add/Edit Task components in frontend/src/components/tasks/
- [ ] T033 [US2] Implement delete confirmation flow in frontend/src/components/tasks/DeleteDialog.tsx

---

## Phase 5: User Story 3 - Task Completion Toggle (Priority: P1)

**Goal**: Toggle task status between pending and completed

**Independent Test**: Toggle a task completion status in the UI, verify status change and timestamp update in DB.

- [x] T034 [P] [US3] Implement status toggle endpoint in backend/src/adapters/api/task_routes.py
- [x] T035 [US3] Implement toggle button and optimistic UI update in frontend/src/components/tasks/TaskItem.tsx

---

## Phase 6: User Story 4 - Search & Filter (Priority: P2)

**Goal**: Find tasks by keyword, priority, status, or tags

**Independent Test**: Filter by "High" priority and search for "Project", verify only matching tasks appear.

- [ ] T036 [P] [US4] Implement search/filter logic in backend TaskRepository query builder
- [ ] T037 [US4] Add filter bar and search input to frontend Dashboard

---

## Phase 7: User Story 5 - Sort Tasks (Priority: P2)

**Goal**: Sort task list by due date, priority, or title

**Independent Test**: Sort by "Due Date", verify tasks appear in chronological order.

- [ ] T038 [P] [US5] Implement dynamic sorting in backend task list endpoint
- [ ] T039 [US5] Add sort dropdown to frontend dashboard UI

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final quality assured delivery

- [ ] T040 [P] Implement responsive design for mobile views in Tailwind
- [ ] T041 [P] Run full mypy strict and TypeScript strict checks
- [ ] T042 [P] Run all backend tests and Playwright E2E tests
- [ ] T043 [P] Perform manual walkthrough using quickstart.md
- [x] T044 Update apps/002-fullstack-web/README.md with tech stack and setup

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Blocks all work
- **Foundational (Phase 2)**: Blocks all user stories
- **Phase 3-4 (Auth & CRUD)**: Essential MVP, should be completed before P2 features
- **Phase 5-7 (Advanced Features)**: Can be implemented after CRUD is stable

### User Story Dependencies

- **US2 (CRUD)** depends on **US1 (Auth)** for user_id association
- **US3, US4, US5** depend on **US2 (CRUD)** being functional

### Parallel Opportunities

- Backend and Frontend setup (T002, T003) can run in parallel
- Unit tests and Gherkin features can be written in parallel for each story
- Sort/Filter (US4, US5) can be developed in parallel once CRUD is done

---

## Implementation Strategy

### MVP First

1. Complete Setup and Foundational (Phases 1-2)
2. Implement Auth (Phase 3)
3. Implement core Task CRUD (Phase 4)
4. **STOP and VALIDATE**: Ensure multi-user isolation is 100% correct

### Incremental Delivery

1. Add Status Toggle
2. Add Search/Filter
3. Add Sort functionality

---

## Notes

- All code MUST follow Hexagonal Architecture (Domain/Ports/Adapters)
- No `any` in TypeScript; strictly typed Pydantic/SQLModel in Python
- Passwords MUST be hashed; JWT MUST be used for session management
- Use optimist UI updates where possible for better UX
