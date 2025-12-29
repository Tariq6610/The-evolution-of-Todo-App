# Quickstart Guide: Phase I - In-Memory Console Todo App

**Feature**: 001-console-todo | **Date**: 2025-12-29

## Prerequisites

- Python 3.11 or higher installed
- pip (Python package manager)
- Git (for version control)

## Installation

1. **Clone the repository** (if not already):
```bash
git clone <repository-url>
cd "The evolution of Todo App"
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

If requirements.txt doesn't exist yet:
```bash
pip install pytest pytest-cov pydantic ruff mypy
```

## Running the Application

### Start the CLI App

```bash
python src/main.py
```

### Expected Output

```
=== Todo Menu ===
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Complete/Incomplete
0. Exit

Enter choice (0-5): _
```

## Basic Usage

### Adding a Task

1. Select option `1` from the menu
2. Enter task title (required):
   ```
   Enter task title: Buy groceries
   ```
3. Enter optional description:
   ```
   Enter task description (optional, press Enter to skip): Weekly shopping
   ```
4. Select priority:
   ```
   Select priority:
   1. Low
   2. Medium (default)
   3. High

   Enter choice (1-3) or press Enter for default:
   ```
5. Enter optional tags:
   ```
   Enter tags (comma-separated, optional, press Enter to skip): home,shopping
   ```
6. Task created with success message

### Viewing All Tasks

1. Select option `2` from the menu
2. All tasks displayed with details
3. Press Enter to return to menu

### Updating a Task

1. Select option `3` from the menu
2. Enter task ID (shown in task list)
3. View current task details
4. Enter new values (press Enter to skip/keep current):
   - New title
   - New description
   - New priority
   - New tags
5. Task updated with success message

### Deleting a Task

1. Select option `4` from the menu
2. Enter task ID
3. Confirm deletion
4. Task removed with success message

### Toggling Task Status

1. Select option `5` from the menu
2. Enter task ID
3. Status toggles between pending and completed
4. Success message shown

### Exiting

1. Select option `0` from the menu
2. Confirm exit
3. Application terminates

## Development Quickstart

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/domain/test_task.py

# Run with verbose output
pytest -v
```

### Code Quality Checks

```bash
# Type checking
mypy src

# Linting
ruff check src

# Formatting
ruff format src

# Format and check in one command
ruff format src && ruff check src
```

### TDD Workflow

1. Write a failing test for a new feature
2. Run tests to confirm failure:
   ```bash
   pytest tests/unit/domain/test_task.py -v
   ```
3. Implement the minimal code to make the test pass
4. Run tests again to confirm pass
5. Refactor code for cleanliness
6. Repeat for next feature

### Project Structure

```
src/
├── domain/          # Pure business logic (no framework deps)
│   ├── entities/    # Task, TaskStatus, Priority
│   ├── services/    # TodoService business rules
│   └── ports/       # Interface contracts
├── adapters/        # Infrastructure implementations
│   ├── storage/     # In-memory storage adapter
│   └── cli/         # Console presentation adapter
└── main.py          # Application entry point

tests/
├── unit/
│   ├── domain/      # Domain logic tests
│   └── adapters/    # Adapter tests
└── conftest.py      # Pytest fixtures
```

## Troubleshooting

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'src'`

**Solution**: Run from project root or set PYTHONPATH:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"  # Linux/Mac
set PYTHONPATH=%PYTHONPATH%;$(cd)      # Windows (PowerShell)
```

### Type Checking Errors

**Problem**: mypy reports errors

**Solution**: Ensure strict type hints on all functions:
```python
# Bad
def add_task(title, description=None):
    ...

# Good
def add_task(title: str, description: Optional[str] = None) -> Task:
    ...
```

### Linting Errors

**Problem**: ruff reports code style issues

**Solution**: Auto-fix where possible:
```bash
ruff check --fix src
```

## Architecture Notes

This application follows **Hexagonal Architecture**:

- **Domain Layer**: Pure business logic, reusable across all phases
- **Ports**: Interfaces defining contracts between layers
- **Adapters**: Implementations that plug into ports

This design enables:
- Swapping storage (in-memory → database in Phase II)
- Swapping presentation (CLI → web in Phase II)
- Domain logic never changes across phases

## Next Steps

After familiarizing with Phase I:

1. Review `spec.md` for detailed requirements
2. Review `plan.md` for architecture decisions
3. Review `data-model.md` for entity definitions
4. Review `contracts/cli-interface.md` for input/output contracts
5. Run `/sp.tasks` to generate implementation tasks

## Important Notes

⚠️ **In-Memory Storage**: All data is lost when application exits. This is by design for Phase I. Future phases will add persistent storage.

⚠️ **Single-User**: Phase I supports only one user. Multi-user support comes in Phase II.

✅ **Type Safety**: All code must pass mypy strict mode before merging.

✅ **Test Coverage**: Domain logic must achieve 100% test coverage.

✅ **TDD Required**: Tests must be written before implementation code.
