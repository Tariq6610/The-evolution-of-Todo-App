# Implementation Plan: Phase I - In-Memory Console Todo App

**Branch**: `001-console-todo` | **Date**: 2025-12-29 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-console-todo/spec.md`

## Summary

Implement a command-line todo application using Python with in-memory storage. Features include basic CRUD operations (add, view, update, delete tasks) and completion status toggling. Architecture follows Hexagonal pattern (Ports & Adapters) to enable seamless migration to future phases (web, AI, cloud). Testing uses TDD with pytest for 100% domain logic coverage. Code quality enforced via strict type hints (mypy) and ruff linting/formatting.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: pytest, pytest-cov, mypy, ruff
**Storage**: In-memory (Python dict/list for task storage)
**Testing**: pytest, pytest-cov (TDD - Red-Green-Refactor cycle)
**Target Platform**: Linux/MacOS/Windows console (Python CLI)
**Project Type**: single (CLI application)
**Performance Goals**: < 100ms for all operations (per constitution), < 2s to display 100 tasks
**Constraints**: Strict type hints required, mypy strict mode, ruff formatting enforced, TDD mandatory
**Scale/Scope**: Single-user console app, in-memory storage (ephemeral), 1,000+ tasks supported

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Constitution Principle | Compliance Status | Notes |
|---------------------|-------------------|--------|
| Spec-Driven Development | ✅ PASS | All code will be generated from spec |
| Phase-Based Evolution | ✅ PASS | Phase I feature branch created, Basic level features only |
| Hexagonal Architecture | ✅ PASS | Design follows Ports & Adapters pattern |
| Shared Core Domain Models | ✅ PASS | Task entity designed for reuse across all phases |
| Phase-Aware Testing | ✅ PASS | TDD with pytest as specified for Phase I |
| Code Quality Standards | ✅ PASS | mypy strict, ruff linting/formatting specified |

**GATE RESULT**: ✅ ALL CHECKS PASSED - Proceed to Phase 0

---

## Post-Design Constitution Re-Check

*Re-verification after Phase 1 design artifacts created.*

| Constitution Principle | Compliance Status | Post-Design Notes |
|---------------------|-------------------|------------------|
| Spec-Driven Development | ✅ PASS | Design artifacts fully derived from spec |
| Phase-Based Evolution | ✅ PASS | Phase I scope clear, Basic features only |
| Hexagonal Architecture | ✅ PASS | Ports & Adapters explicitly designed in data-model.md |
| Shared Core Domain Models | ✅ PASS | Task entity defined as Pydantic model, reusable |
| Phase-Aware Testing | ✅ PASS | TDD with pytest specified in research.md |
| Code Quality Standards | ✅ PASS | mypy strict, ruff configured in research.md |

**POST-DESIGN GATE RESULT**: ✅ ALL CHECKS PASSED - Ready for task generation

---

## Project Structure

### Documentation (this feature)

```text
specs/001-console-todo/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (CLI interface contracts)
└── tasks.md             # Phase 2 output (from /sp.tasks)
```

### Source Code (repository root)

```text
src/
├── domain/
│   ├── entities/
│   │   ├── task.py          # Task entity (shared across phases)
│   │   ├── task_status.py    # TaskStatus enum
│   │   └── priority.py       # Priority enum
│   ├── services/
│   │   └── todo_service.py  # Business logic (pure domain)
│   └── ports/
│       ├── task_input_port.py      # Interface for task operations
│       ├── task_output_port.py     # Interface for task queries
│       └── storage_port.py        # Interface for persistence
├── adapters/
│   ├── storage/
│   │   └── in_memory_storage.py  # In-memory storage adapter
│   └── cli/
│       ├── console_adapter.py       # CLI presentation adapter
│       └── menu_system.py         # Interactive menu
└── main.py                     # Application entry point

tests/
├── unit/
│   ├── domain/
│   │   ├── test_task.py
│   │   └── test_todo_service.py
│   └── adapters/
│       ├── test_in_memory_storage.py
│       └── test_console_adapter.py
└── conftest.py                 # pytest fixtures
```

**Structure Decision**: Single project structure with hexagonal architecture separation. Domain layer contains pure business logic (entities, services, ports). Adapters layer contains infrastructure implementations (storage, CLI). This structure ensures portability - the entire domain can be reused in future phases with only adapter replacements needed.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A - No violations detected |

---
