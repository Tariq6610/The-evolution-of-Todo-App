---
description: "Task list for feature implementation"
---

# Tasks: Phase I - In-Memory Console Todo App

**Input**: Design documents from `/specs/001-console-todo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: TDD is REQUIRED by constitution - tests must be written FIRST and FAIL before implementation

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, etc.)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan
- [X] T002 Initialize Python project with pytest, pytest-cov, mypy, ruff, pydantic dependencies
- [X] T003 [P] Configure mypy strict mode in pyproject.toml
- [X] T004 [P] Configure ruff linting and formatting in pyproject.toml
- [X] T005 [P] Create pytest configuration (pytest.ini or pyproject.toml section)
- [X] T006 [P] Create pytest conftest.py fixture for test isolation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T007 [P] Create TaskStatus enum in src/domain/entities/task_status.py
- [X] T008 [P] Create Priority enum in src/domain/entities/priority.py
- [X] T009 [P] Create Task entity with Pydantic BaseModel in src/domain/entities/task.py (depends on T007, T008)
- [X] T010 [P] Create StoragePort interface in src/domain/ports/storage_port.py
- [X] T011 [P] Create TaskInputPort interface in src/domain/ports/task_input_port.py
- [X] T012 [P] Create TaskOutputPort interface in src/domain/ports/task_output_port.py
- [X] T013 [P] Create TodoService business logic stub in src/domain/services/todo_service.py (depends on T009, T010, T011, T012)
- [X] T014 [P] Create InMemoryStorage adapter in src/adapters/storage/in_memory_storage.py (implements StoragePort)
- [X] T015 [P] Create MenuSystem utility in src/adapters/cli/menu_system.py
- [X] T016 [P] Create ConsoleAdapter stub in src/adapters/cli/console_adapter.py
- [X] T017 Create main.py entry point with basic structure
- [X] T018 Configure error handling infrastructure

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new tasks to their todo list and view all tasks

**Independent Test**: Create a task with title and optional description, then view all tasks to verify it appears with correct details. Deliver a simple task tracker.

### Tests for User Story 1 (TDD - Write FAILING Tests First) ⚠️

> **CRITICAL: Constitution mandates TDD - Write these tests FIRST, ensure they FAIL, then implement**

- [X] T019 [P] [US1] Write failing test for Task entity creation with validation in tests/unit/domain/test_task.py
- [X] T020 [P] [US1] Write failing test for TaskStatus enum in tests/unit/domain/test_task_status.py
- [X] T021 [P] [US1] Write failing test for Priority enum in tests/unit/domain/test_priority.py
- [X] T022 [P] [US1] Write failing test for TodoService.create_task() with title validation in tests/unit/domain/test_todo_service.py
- [X] T023 [P] [US1] Write failing test for TodoService.get_all_tasks() returning empty list in tests/unit/domain/test_todo_service.py
- [X] T024 [P] [US1] Write failing test for InMemoryStorage.save() and get_all() in tests/unit/adapters/test_in_memory_storage.py
- [X] T025 [P] [US1] Write failing test for MenuSystem.show_menu() display format in tests/unit/adapters/test_menu_system.py
- [X] T026 [P] [US1] Write failing test for ConsoleAdapter.add_task_flow() input handling in tests/unit/adapters/test_console_adapter.py

**Verify**: Run pytest - confirm all tests FAIL before proceeding

### Implementation for User Story 1

- [X] T027 [US1] Implement TaskStatus enum values (PENDING, COMPLETED) in src/domain/entities/task_status.py
- [X] T028 [US1] Implement Priority enum values (LOW, MEDIUM, HIGH) in src/domain/entities/priority.py
- [X] T029 [US1] Implement Task entity Pydantic model with all fields and validation in src/domain/entities/task.py (depends on T027, T028)
- [X] T030 [US1] Implement Task.mark_completed(), mark_pending(), toggle_status() methods in src/domain/entities/task.py
- [X] T031 [US1] Implement StoragePort interface with abstract methods in src/domain/ports/storage_port.py
- [X] T032 [US1] Implement TaskInputPort interface with abstract methods in src/domain/ports/task_input_port.py
- [X] T033 [US1] Implement TaskOutputPort interface with abstract methods in src/domain/ports/task_output_port.py
- [X] T034 [US1] Implement TodoService.__init__() with storage injection in src/domain/services/todo_service.py
- [X] T035 [US1] Implement TodoService.create_task() with title validation and ID generation in src/domain/services/todo_service.py (depends on T031, T034)
- [X] T036 [US1] Implement TodoService.get_all_tasks() returning list in src/domain/services/todo_service.py
- [X] T037 [US1] Implement InMemoryStorage with dict[str, Task] in src/adapters/storage/in_memory_storage.py
- [X] T038 [US1] Implement InMemoryStorage.save() with UUID generation in src/adapters/storage/in_memory_storage.py
- [X] T039 [US1] Implement InMemoryStorage.get_all() returning all tasks in src/adapters/storage/in_memory_storage.py
- [X] T040 [US1] Implement InMemoryStorage.get() by task_id in src/adapters/storage/in_memory_storage.py
- [X] T041 [US1] Implement MenuSystem.show_menu() with numbered options 0-5 in src/adapters/cli/menu_system.py
- [X] T042 [US1] Implement MenuSystem.get_user_choice() with input validation in src/adapters/cli/menu_system.py
- [X] T043 [US1] Implement MenuSystem.get_task_title_input() with empty/whitespace validation in src/adapters/cli/menu_system.py
- [X] T044 [US1] Implement MenuSystem.get_task_description_input() with optional handling in src/adapters/cli/menu_system.py
- [X] T045 [US1] Implement ConsoleAdapter.add_task_flow() collecting inputs and calling TodoService in src/adapters/cli/console_adapter.py (depends on T043, T044)
- [X] T046 [US1] Implement ConsoleAdapter.view_all_tasks_flow() displaying tasks with task count in src/adapters/cli/console_adapter.py
- [X] T047 [US1] Wire ConsoleAdapter to TodoService and InMemoryStorage in src/main.py
- [X] T048 [US1] Add main loop in main.py showing menu and handling Add/View options

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Mark Tasks as Complete (Priority: P1) 🎯 MVP

**Goal**: Enable users to toggle task completion status (pending ↔ completed)

**Independent Test**: Create a task, mark it complete, verify status changes and timestamp updates. Deliver task progress tracking.

### Tests for User Story 2 (TDD - Write FAILING Tests First) ⚠️

- [X] T049 [P] [US2] Write failing test for Task.toggle_status() state transition in tests/unit/domain/test_task.py
- [X] T050 [P] [US2] Write failing test for TodoService.toggle_task_status() in tests/unit/domain/test_todo_service.py
- [X] T051 [P] [US2] Write failing test for ConsoleAdapter.toggle_status_flow() in tests/unit/adapters/test_console_adapter.py

**Verify**: Run pytest - confirm new tests FAIL before proceeding

### Implementation for User Story 2

- [X] T052 [US2] Implement TaskStatus enum COMPLETED value in src/domain/entities/task_status.py
- [X] T053 [US2] Implement Task.toggle_status() switching between PENDING and COMPLETED in src/domain/entities/task.py
- [X] T054 [US2] Implement TodoService.toggle_task_status() calling Task.toggle_status() in src/domain/services/todo_service.py
- [X] T055 [US2] Implement ConsoleAdapter.toggle_status_flow() getting task ID and calling service in src/adapters/cli/console_adapter.py
- [X] T056 [US2] Add Toggle Status option to main loop in main.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Task Details (Priority: P2)

**Goal**: Enable users to modify existing task properties (title, description, priority, tags)

**Independent Test**: Create a task, update its title/description/priority/tags, verify changes persist and timestamp updates. Deliver a flexible task manager.

### Tests for User Story 3 (TDD - Write FAILING Tests First) ⚠️

- [X] T057 [P] [US3] Write failing test for Task field updates in tests/unit/domain/test_task.py
- [X] T058 [P] [US3] Write failing test for TodoService.update_task() partial updates in tests/unit/domain/test_todo_service.py
- [X] T059 [P] [US3] Write failing test for InMemoryStorage.update() in tests/unit/adapters/test_in_memory_storage.py
- [X] T060 [P] [US3] Write failing test for MenuSystem.get_priority_selection() in tests/unit/adapters/test_menu_system.py
- [X] T061 [P] [US3] Write failing test for MenuSystem.get_tags_input() in tests/unit/adapters/test_menu_system.py
- [X] T062 [P] [US3] Write failing test for ConsoleAdapter.update_task_flow() in tests/unit/adapters/test_console_adapter.py

**Verify**: Run pytest - confirm new tests FAIL before proceeding

### Implementation for User Story 3

- [X] T063 [US3] Add tags field to Task entity in src/domain/entities/task.py
- [X] T064 [US3] Implement MenuSystem.get_priority_selection() with 1/2/3 input in src/adapters/cli/menu_system.py
- [X] T065 [US3] Implement MenuSystem.get_tags_input() parsing comma-separated list in src/adapters/cli/menu_system.py
- [X] T066 [US3] Implement InMemoryStorage.update() partial field update in src/adapters/storage/in_memory_storage.py
- [X] T067 [US3] Implement TodoService.update_task() with partial updates in src/domain/services/todo_service.py
- [X] T068 [US3] Implement ConsoleAdapter.update_task_flow() collecting partial inputs in src/adapters/cli/console_adapter.py
- [X] T069 [US3] Add Update Task option to main loop in main.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P2)

**Goal**: Enable users to remove tasks from their list

**Independent Test**: Create a task, delete it, verify it's removed and other tasks unaffected. Deliver a maintainable task list.

### Tests for User Story 4 (TDD - Write FAILING Tests First) ⚠️

- [X] T070 [P] [US4] Write failing test for InMemoryStorage.delete() in tests/unit/adapters/test_in_memory_storage.py
- [X] T071 [P] [US4] Write failing test for TodoService.delete_task() in tests/unit/domain/test_todo_service.py
- [X] T072 [P] [US4] Write failing test for ConsoleAdapter.delete_task_flow() in tests/unit/adapters/test_console_adapter.py

**Verify**: Run pytest - confirm new tests FAIL before proceeding

### Implementation for User Story 4

- [X] T073 [US4] Implement InMemoryStorage.delete() removing task by ID in src/adapters/storage/in_memory_storage.py
- [X] T074 [US4] Implement TodoService.delete_task() with not-found error in src/domain/services/todo_service.py
- [X] T075 [US4] Implement ConsoleAdapter.delete_task_flow() with confirmation in src/adapters/cli/console_adapter.py
- [X] T076 [US4] Add Delete Task option to main loop in main.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T077 [P] Add exit confirmation to main.py
- [X] T078 [P] Implement task count display in view_all_tasks() in src/adapters/cli/console_adapter.py
- [X] T079 [P] Add improved error messages for all invalid inputs in src/adapters/cli/menu_system.py
- [X] T080 [P] Ensure all timestamps update on modification in src/domain/entities/task.py
- [X] T081 [P] Run mypy strict mode check on all src/ - fix all type errors
- [X] T082 [P] Run ruff format on all code
- [X] T083 [P] Run ruff check on all code - fix all linting issues
- [X] T084 [P] Run pytest with coverage - ensure 100% domain logic coverage
- [ ] T085 Run application manual test following quickstart.md guide
- [ ] T086 [P] Update README.md with project description and usage instructions

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P2)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable

### Within Each User Story

- Tests MUST be written and FAIL before implementation (TDD constitution mandate)
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (TDD - must FAIL first):
Task: "Write failing test for Task entity creation with validation in tests/unit/domain/test_task.py"
Task: "Write failing test for TaskStatus enum in tests/unit/domain/test_task_status.py"
Task: "Write failing test for Priority enum in tests/unit/domain/test_priority.py"
Task: "Write failing test for TodoService.create_task() with title validation in tests/unit/domain/test_todo_service.py"

# Launch all models for User Story 1 together (after tests FAIL):
Task: "Implement TaskStatus enum values (PENDING, COMPLETED) in src/domain/entities/task_status.py"
Task: "Implement Priority enum values (LOW, MEDIUM, HIGH) in src/domain/entities/priority.py"
Task: "Implement Task entity Pydantic model with all fields and validation in src/domain/entities/task.py"
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. Complete Phase 4: User Story 2
5. **STOP and VALIDATE**: Test both P1 stories independently
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (TDD constitution mandate)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- **TDD is NON-NEGOTIABLE**: Tests written FIRST, must FAIL, then implement
- **Type hints MANDATORY**: All functions must have strict type annotations
- **100% domain logic coverage**: All domain code must be tested
