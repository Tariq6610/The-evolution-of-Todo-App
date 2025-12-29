---
id: 0003
title: Phase I Console Todo Tasks
stage: tasks
date: 2025-12-29
surface: agent
model: sonnet-4-5
feature: 001-console-todo
branch: 001-console-todo
user: tariq
command: sp.tasks
labels: ["tasks", "phase-1", "tdd", "implementation"]
links:
  spec: specs/001-console-todo/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-console-todo/tasks.md
  - history/prompts/001-console-todo/0003-phase-i-console-todo-tasks.tasks.prompt.md
tests:
  - 23 TDD test tasks specified (write failing tests first)
---

## Prompt

$ARGUMENTS

## Response snapshot

Generated comprehensive task breakdown for Phase I console todo app following TDD principles.

**Total Tasks**: 86 tasks across 7 phases
**Test Tasks**: 23 TDD tests (write failing tests first)
**User Stories**: 4 stories organized by priority (P1, P1, P2, P2)

**Phase Breakdown**:

**Phase 1: Setup** (6 tasks)
- Project structure creation
- Python environment setup with pytest, pytest-cov, mypy, ruff, pydantic
- mypy and ruff configuration in pyproject.toml
- pytest configuration
- conftest.py fixture for test isolation

**Phase 2: Foundational** (12 tasks) - BLOCKING
- TaskStatus enum creation
- Priority enum creation
- Task entity with Pydantic model
- StoragePort, TaskInputPort, TaskOutputPort interfaces
- TodoService business logic stub
- InMemoryStorage adapter
- MenuSystem utility
- ConsoleAdapter stub
- main.py entry point
- Error handling infrastructure

**Phase 3: User Story 1 - Create and View Tasks (P1) MVP** (30 tasks)
- 8 TDD tests (failing tests first)
- TaskStatus, Priority enum implementation
- Task entity with methods (mark_completed, mark_pending, toggle_status)
- Port interfaces implementation
- TodoService methods (create_task, get_all_tasks)
- InMemoryStorage methods (save, get_all, get)
- MenuSystem methods (show_menu, get_user_choice, get_task_title_input, get_task_description_input)
- ConsoleAdapter flows (add_task_flow, view_all_tasks_flow)
- main.py wiring

**Phase 4: User Story 2 - Mark Tasks as Complete (P1) MVP** (8 tasks)
- 3 TDD tests
- TaskStatus COMPLETED value
- Task.toggle_status() implementation
- TodoService.toggle_task_status()
- ConsoleAdapter.toggle_status_flow()
- main loop option

**Phase 5: User Story 3 - Update Task Details (P2)** (13 tasks)
- 6 TDD tests
- tags field to Task entity
- MenuSystem methods (get_priority_selection, get_tags_input)
- InMemoryStorage.update()
- TodoService.update_task()
- ConsoleAdapter.update_task_flow()
- main loop option

**Phase 6: User Story 4 - Delete Tasks (P2)** (7 tasks)
- 3 TDD tests
- InMemoryStorage.delete()
- TodoService.delete_task()
- ConsoleAdapter.delete_task_flow()
- main loop option

**Phase 7: Polish & Cross-Cutting** (10 tasks)
- Exit confirmation
- Task count display
- Error message improvements
- Timestamp update on all modifications
- mypy strict mode compliance
- ruff format and check
- pytest with 100% domain coverage
- Manual testing per quickstart.md
- README.md documentation

**MVP Scope**: Phases 1-4 (User Stories 1 & 2) - 56 tasks total

**TDD Compliance**:
- All user stories have test tasks BEFORE implementation
- Tests specified to FAIL first
- Red-Green-Refactor cycle mandated by constitution

**Independent Test Criteria**:
- US1: Create task, view list - simple task tracker
- US2: Toggle completion status - task progress tracker
- US3: Update task details - flexible task manager
- US4: Delete tasks - maintainable task list

**Parallel Opportunities**:
- All Setup tasks marked [P] can run in parallel
- Foundational tasks marked [P] can run in parallel
- All test tasks marked [P] can run in parallel
- Models within story marked [P] can run in parallel
- Different user stories can be worked on in parallel

**File Paths**:
- All tasks specify exact file paths (src/domain/entities/, src/domain/services/, src/adapters/storage/, src/adapters/cli/, tests/)

## Outcome

- ✅ Impact: Complete task breakdown ready for TDD implementation
- 🧪 Tests: 23 TDD test tasks specified (write failing tests first)
- 📁 Files: tasks.md created with 86 tasks organized by user story
- 🔁 Next prompts: Ready for `/sp.implement` to begin TDD implementation
- 🧠 Reflection: Tasks follow constitution mandates (TDD, strict typing, hexagonal architecture)

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - All tasks follow checklist format, TDD tests specified, file paths explicit
- Prompt variant (if applicable): N/A - Initial tasks generation
- Next experiment: Validate that generated implementation follows TDD cycle during `/sp.implement`
