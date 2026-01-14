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

- [x] T013 [P] [US1] Write Gherkin feature for Auth flows in frontend/tests/features/auth.feature
- [x] T014 [P] [US1] Write failing unit tests for User model in backend/tests/unit/domain/test_user.py
- [x] T015 [P] [US1] Write failing integration tests for Auth endpoints in backend/tests/integration/test_auth.py

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

- [x] T024 [P] [US2] Write Gherkin feature for Task CRUD in frontend/tests/features/tasks.feature
- [x] T025 [P] [US2] Write failing unit tests for Task entity (extended) in backend/tests/unit/domain/test_task.py
- [x] T026 [P] [US2] Write failing integration tests for Task endpoints in backend/tests/integration/test_tasks.py

### Implementation for User Story 2

- [x] T027 [P] [US2] Update Task entity with user_id and persistence in backend/src/domain/entities/task.py
- [x] T028 [P] [US2] Implement TaskRepository using SQLModel in backend/src/adapters/db/task_repository.py
- [x] T029 [US2] Implement TaskService with multi-user isolation in backend/src/domain/services/task_service.py
- [x] T030 [US2] Implement Task CRUD endpoints with JWT protection in backend/src/adapters/api/task_routes.py
- [x] T031 [US2] Create Task List dashboard in frontend/src/app/dashboard/page.tsx
- [x] T032 [US2] Update dashboard to use TaskForm and DeleteDialog components
- [x] T033 [US2] DeleteDialog component exists in frontend/src/components/tasks/DeleteDialog.tsx (integrated in dashboard)

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

- [x] T036 [P] [US4] Implement search/filter and sort logic in backend TaskRepository query builder
- [x] T037 [US4] Add filter bar and search input to frontend Dashboard

---

## Phase 7: User Story 5 - Sort Tasks (Priority: P2)

**Goal**: Sort task list by due date, priority, or title

**Independent Test**: Sort by "Due Date", verify tasks appear in chronological order.

- [x] T038 [P] [US5] Implement dynamic sorting in backend task list endpoint
- [x] T039 [US5] Add sort dropdown to frontend dashboard UI

---

## Phase 8: Neon DB Migration

**Purpose**: Migrate from SQLite (development) to Neon DB (production) for enhanced scalability and multi-user support

- [x] T040 [P] Create Neon DB project and database instance on Neon platform
- [x] T041 [P] Update backend .env file with Neon DB connection string in apps/002-fullstack-web/backend/.env
- [x] T042 [P] Test database connection with Neon DB by running the backend application
- [x] T043 [P] Verify all SQLModel operations work with PostgreSQL using existing tests
- [x] T044 [P] Update .env.example with PostgreSQL connection string format in apps/002-fullstack-web/backend/.env.example
- [x] T045 [P] Run existing tests to verify Neon DB compatibility in apps/002-fullstack-web/backend/tests/
- [x] T046 [P] Test all CRUD operations with Neon DB using integration tests
- [x] T047 [P] Verify multi-user data isolation with Neon DB using test scenarios
- [x] T048 [P] Update README.md with Neon DB setup instructions in apps/002-fullstack-web/README.md

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Final quality assured delivery

- [x] T049 [P] Implement responsive design for mobile views in Tailwind
- [x] T050 [P] Run full mypy strict and TypeScript strict checks
- [x] T051 [P] Run all backend tests and Playwright E2E tests
- [x] T052 [P] Perform manual walkthrough using quickstart.md
- [x] T053 Update apps/002-fullstack-web/README.md with tech stack and setup

---

## Phase 10: Dashboard Redesign (Priority: P2) 🎨

**Goal**: Transform the minimal dashboard into an insight-driven, action-oriented overview

**Independent Test**: Dashboard shows dynamic greeting, stats with animations, charts, attention panels, quick actions, and smart insights - all using existing task data without backend changes.

### Component Creation Tasks

- [x] T054 [P] [DASH] Create AnimatedCounter component in frontend/src/components/dashboard/AnimatedCounter.tsx
- [x] T055 [P] [DASH] Create HeroSummary component with greeting + progress ring in frontend/src/components/dashboard/HeroSummary.tsx
- [x] T056 [P] [DASH] Create StatsCard component with animations in frontend/src/components/dashboard/StatsCard.tsx
- [x] T057 [P] [DASH] Create TaskStatusChart (donut chart) using recharts in frontend/src/components/dashboard/TaskStatusChart.tsx
- [x] T058 [P] [DASH] Create PriorityChart (bar chart) using recharts in frontend/src/components/dashboard/PriorityChart.tsx
- [x] T059 [DASH] Create AttentionPanel component for high-priority/recent tasks in frontend/src/components/dashboard/AttentionPanel.tsx
- [x] T060 [DASH] Create QuickActions component with icon-based buttons in frontend/src/components/dashboard/QuickActions.tsx
- [x] T061 [DASH] Create SmartInsight component for intelligent insights in frontend/src/components/dashboard/SmartInsight.tsx

### Dashboard Integration Tasks

- [x] T062 [DASH] Redesign dashboard page layout in frontend/src/app/dashboard/page.tsx
- [x] T063 [DASH] Remove duplicate task list and filter bar from dashboard (keep Tasks page for full functionality)
- [x] T064 [DASH] Add entrance animations using Framer Motion for all sections
- [x] T065 [DASH] Implement responsive design for mobile and tablet
- [x] T066 [DASH] Add graceful empty states with friendly messaging

### Visual Polish Tasks

- [x] T067 [P] [DASH] Apply consistent card styling with soft shadows
- [x] T068 [P] [DASH] Implement dark mode support for all new components
- [x] T069 [DASH] Add hover effects and micro-interactions

**Checkpoint**: Dashboard provides meaningful overview without replicating Tasks page functionality

---

## Implementation Complete

All planned features for the Phase II Full-Stack Web Application have been implemented and documented.

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
