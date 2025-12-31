# The Evolution of Todo - Phase I: Console App

A command-line todo application built with Python following Spec-Driven Development (SDD) principles.

## Features

- **Add Tasks**: Create tasks with title, optional description, priority, and tags
- **View Tasks**: Display all tasks with their details and status
- **Update Tasks**: Modify task title, description, priority, and tags
- **Delete Tasks**: Remove tasks with confirmation
- **Toggle Status**: Mark tasks as complete/incomplete
- **Priority Levels**: Low, Medium, High
- **Tags**: Categorize tasks with multiple tags

## Architecture

This application follows **Hexagonal Architecture** (Ports & Adapters pattern):

```
src/
├── domain/           # Pure business logic (reusable across phases)
│   ├── entities/     # Task, TaskStatus, Priority
│   ├── services/     # TodoService (business rules)
│   └── ports/        # Interface contracts
├── adapters/         # Infrastructure implementations
│   ├── storage/      # In-memory storage adapter
│   └── cli/          # Console presentation adapter
└── main.py           # Application entry point
```

## Requirements

- Python 3.11 or higher
- pip

## Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -e ".[dev]"
```

## Running the Application

```bash
# From project root
PYTHONPATH=. python src/main.py
```

Or add to `.bashrc`/`.zshrc`:
```bash
export PYTHONPATH="${PYTHONPATH}:/path/to/project"
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/unit/domain/test_task.py -v
```

### Code Quality

```bash
# Type checking (strict mode)
mypy src

# Linting
ruff check src

# Formatting
ruff format src
```

### TDD Workflow

1. Write a failing test
2. Run tests to confirm failure
3. Implement the minimal code
4. Run tests to confirm pass
5. Refactor for cleanliness
6. Repeat

## Project Structure

```
specs/001-console-todo/
├── spec.md              # Feature specification
├── plan.md              # Architecture decisions
├── data-model.md        # Entity definitions
├── contracts/           # CLI interface contracts
├── tasks.md             # Implementation tasks
├── quickstart.md        # Development guide
└── checklists/          # Quality checklists

src/
├── domain/              # Pure business logic
├── adapters/            # Infrastructure
└── main.py              # Entry point

tests/
├── unit/
│   ├── domain/          # Domain logic tests
│   └── adapters/        # Adapter tests
└── conftest.py          # Pytest fixtures
```

## License

MIT

## Phase Evolution

This is **Phase I** of "The Evolution of Todo" project:

- **Phase I**: Console app with in-memory storage
- **Phase II**: Web app with database persistence
- **Phase III**: AI-enhanced features
- **Phase V**: Cloud-native with event streaming
