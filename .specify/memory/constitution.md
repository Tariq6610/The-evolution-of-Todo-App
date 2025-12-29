# The Evolution of Todo - Project Constitution

## Vision Statement

**The Evolution of Todo** is a progressive application that demonstrates software engineering best practices by evolving a simple todo application through five distinct phases—from a Python console app to a cloud-native, AI-powered distributed system. Each phase builds upon the previous, showcasing modern development patterns, testing strategies, and deployment methodologies.

---

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

All code MUST be generated from specifications. Manual code writing is strictly prohibited.

- **Specification First**: Every feature begins with a detailed spec document
- **Refinement Loop**: Refine specs until Claude Code generates correct output
- **Traceability**: All implementation decisions trace back to spec requirements
- **No Manual Code**: Developers write specs, not code; AI generates implementation

### II. Phase-Based Evolution

The project evolves through distinct phases, each as a separate feature branch:

| Phase | Description | Stack | Feature Level |
|-------|-------------|-------|---------------|
| **I** | In-Memory Python Console App | Python, pytest | Basic |
| **II** | Full-Stack Web Application | Next.js, FastAPI, SQLModel, Neon DB | Basic + Intermediate |
| **III** | AI-Powered Todo Chatbot | OpenAI ChatKit, Agents SDK, MCP SDK | All Levels |
| **IV** | Local Kubernetes Deployment | Docker, Minikube, Helm, kubectl-ai | All Levels |
| **V** | Advanced Cloud Deployment | Kafka, Dapr, DigitalOcean DOKS | All Levels + Extensions |

- Each phase is a **separate feature branch** merged to master upon completion
- Phases are **additive**—never break existing functionality
- Future phases may be added beyond Phase V

### III. Feature Levels

Features are organized into three progressive levels:

**Basic Level (Core Essentials)** - Foundation for MVP:
- Add Task – Create new todo items
- Delete Task – Remove tasks from the list
- Update Task – Modify existing task details
- View Task List – Display all tasks
- Mark as Complete – Toggle task completion status

**Intermediate Level (Organization & Usability)** - Polish and practicality:
- Priorities & Tags/Categories – Assign levels (high/medium/low) or labels
- Search & Filter – Search by keyword; filter by status, priority, or date
- Sort Tasks – Reorder by due date, priority, or alphabetically

**Advanced Level (Intelligent Features)** - AI and automation:
- Recurring Tasks – Auto-reschedule repeating tasks
- Due Dates & Time Reminders – Deadlines with notifications
- Natural Language Interface – AI-powered task management (Phase III+)

### IV. Hexagonal Architecture (Ports & Adapters)

All code follows Hexagonal Architecture for maximum portability across phases:

```
┌─────────────────────────────────────────────────────────┐
│                    ADAPTERS (Outside)                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Console   │  │   Web API   │  │  AI/Chat    │     │
│  │   (Phase I) │  │  (Phase II) │  │ (Phase III) │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         │                │                │             │
│  ┌──────▼────────────────▼────────────────▼──────┐     │
│  │              PORTS (Interfaces)                │     │
│  │   TaskInputPort    TaskOutputPort              │     │
│  │   StoragePort      NotificationPort            │     │
│  └──────────────────────┬────────────────────────┘     │
│                         │                               │
│  ┌──────────────────────▼────────────────────────┐     │
│  │              DOMAIN (Core Logic)               │     │
│  │   Task Entity    TodoService    BusinessRules  │     │
│  │   (Shared across ALL phases)                   │     │
│  └──────────────────────┬────────────────────────┘     │
│                         │                               │
│  ┌──────────────────────▼────────────────────────┐     │
│  │              PORTS (Interfaces)                │     │
│  │   RepositoryPort   EventPort                   │     │
│  └──────┬──────────────┬──────────────┬──────────┘     │
│         │              │              │                 │
│  ┌──────▼──────┐ ┌─────▼─────┐ ┌─────▼──────┐         │
│  │  In-Memory  │ │  Neon DB  │ │   Kafka    │         │
│  │  (Phase I)  │ │ (Phase II)│ │ (Phase V)  │         │
│  └─────────────┘ └───────────┘ └────────────┘         │
└─────────────────────────────────────────────────────────┘
```

- **Domain Layer**: Pure business logic, no framework dependencies
- **Ports**: Interfaces defining how domain interacts with outside world
- **Adapters**: Implementations that plug into ports (swappable per phase)

### V. Shared Core Domain Models

Domain models are defined once and reused/extended across all phases:

```python
# Core entities (defined in Phase I, used everywhere)
Task:
  - id: UUID
  - title: str
  - description: Optional[str]
  - status: TaskStatus (pending | completed)
  - priority: Priority (low | medium | high)
  - tags: List[str]
  - due_date: Optional[datetime]
  - recurrence: Optional[RecurrenceRule]
  - created_at: datetime
  - updated_at: datetime
```

- Models are **technology-agnostic** in the domain layer
- Adapters handle serialization/ORM mapping per phase
- Schema evolution follows backward compatibility

### VI. Phase-Aware Testing Strategy

Testing approach varies by phase complexity:

#### Phase I: Test-Driven Development (TDD)
- Write failing unit tests FIRST
- Red-Green-Refactor cycle strictly enforced
- Focus on small, isolated functions
- 100% coverage of domain logic
- Tools: pytest, pytest-cov

#### Phase II: BDD + Test-Along
- BDD (Given-When-Then) for user flows
- Integration tests for API/UI
- Test-Along for evolving features
- Tools: pytest-bdd, Playwright, httpx

#### Phase III: BDD as Executable Specs
- Conversational behavior in Gherkin
- Behavioral assertions for AI responses
- Statistical tests for non-deterministic output
- Tools: pytest-bdd, custom AI validators

#### Phase IV-V: Integration & Contract Tests
- System behavior over unit tests
- Contract tests between services
- Deployment smoke tests
- Failure simulation tests
- Tools: pytest, k8s test frameworks, contract testing

### VII. Code Quality Standards (NON-NEGOTIABLE)

**Python (All Phases)**:
- Type hints: MANDATORY on all functions and methods
- Type checker: mypy with strict mode
- Linter: ruff (replaces flake8, isort, black)
- Formatter: ruff format
- Docstrings: Google style for public APIs

**TypeScript/JavaScript (Phase II+)**:
- TypeScript: strict mode enabled
- Linter: ESLint with recommended rules
- Formatter: Prettier
- No `any` types without explicit justification

**Configuration**:
```toml
# pyproject.toml standards
[tool.mypy]
strict = true
warn_return_any = true
warn_unused_ignores = true

[tool.ruff]
line-length = 88
select = ["E", "F", "I", "N", "W", "UP", "B", "C4", "SIM"]
```

---

## Development Workflow

### Branch Strategy

```
master (stable, production-ready)
  │
  ├── phase-1-console-app
  │     └── Merged when Phase I complete
  │
  ├── phase-2-fullstack-web
  │     └── Merged when Phase II complete
  │
  ├── phase-3-ai-chatbot
  │     └── Merged when Phase III complete
  │
  ├── phase-4-kubernetes
  │     └── Merged when Phase IV complete
  │
  └── phase-5-cloud-deployment
        └── Merged when Phase V complete
```

### Feature Branch Workflow (MANDATORY)

**BEFORE starting any new phase/feature**, the following workflow MUST be executed:

1. **Create Feature Branch**:
   ```bash
   git checkout -b phase-<number>-<feature-name>
   # Example: git checkout -b phase-1-console-app
   ```

2. **Create Feature Specification**:
   - Run `/sp.specify` with feature description
   - Review and refine spec until complete

3. **Create Implementation Plan**:
   - Run `/sp.plan` to generate architecture/design
   - Document architectural decisions

4. **Generate Tasks**:
   - Run `/sp.tasks` to break down implementation
   - Ensure tasks are testable and atomic

5. **Implement with TDD/BDD**:
   - Follow phase-appropriate testing strategy
   - All code generated from specs (no manual coding)

6. **Commit and Create PR (MANDATORY AFTER EVERY FEATURE)**:
   - **ALWAYS run** `/sp.git.commit_pr` after completing ANY feature
   - This commits changes and creates a PR for review
   - Ensure all Definition of Done criteria met

7. **Merge to Master**:
   - After approval and all checks pass
   - Feature becomes part of stable codebase

**Post-Feature Completion Rule (NON-NEGOTIABLE)**:
- After completing **ANY** feature (phase, sub-feature, user story), you MUST:
  1. Ask to execute `/sp.git.commit_pr`
  2. Ensure all tests pass
  3. Ensure code quality checks pass
  4. Review and approve the PR
- No feature is considered "complete" without a PR

**Branch Naming Convention**:
- `phase-<N>-<short-description>`
- Examples: `phase-1-console-app`, `phase-2-fullstack-web`, `phase-3-ai-chatbot`

**Never Start Work Without**:
- ✅ Feature branch created
- ✅ Spec document reviewed
- ✅ Plan documented
- ✅ Tasks defined

### Definition of Done (Per Phase)

A phase is complete when:
- [ ] All spec requirements implemented
- [ ] All tests passing (phase-appropriate strategy)
- [ ] Code quality checks pass (mypy, ruff, eslint)
- [ ] CI/CD pipeline green
- [ ] Specs serve as documentation
- [ ] ADRs created for significant decisions
- [ ] PHR recorded for all prompts
- [ ] Feature branch merged to master

### CI/CD Requirements

- All tests MUST pass before merge
- Code quality gates enforced
- Automated deployment (Phase IV+)
- No manual interventions in pipeline

---

## Documentation Standards

### Specs as Documentation

- **Primary Documentation**: Specs, tests, and ADRs
- Feature specs describe WHAT and WHY
- Tests describe HOW (executable documentation)
- ADRs capture significant architectural decisions
- PHRs maintain prompt history for traceability

### Required Artifacts Per Phase

```
specs/<phase-name>/
  ├── spec.md          # Feature specification
  ├── plan.md          # Architecture/design plan
  ├── tasks.md         # Implementation tasks
  └── features/        # BDD feature files (Phase II+)
      └── *.feature

history/
  ├── prompts/<phase-name>/  # PHRs for this phase
  └── adr/                   # Architecture Decision Records
```

---

## Security & Performance

### Security Requirements

- No hardcoded secrets or tokens
- Use environment variables (.env) for configuration
- Secrets managed via proper secret management (Phase IV+)
- Input validation on all user inputs
- SQL injection prevention (parameterized queries)
- XSS prevention in web interfaces

### Performance Guidelines

- Response time targets per phase
- Phase I: < 100ms for all operations
- Phase II: < 200ms API responses
- Phase III: < 2s for AI responses
- Phase IV-V: Defined SLOs per service

---

## Governance

### Constitution Authority

- This constitution supersedes all other practices
- Amendments require:
  1. Documentation of change rationale
  2. Impact assessment on existing phases
  3. ADR for significant changes
  4. Update to all affected specs

### Compliance Verification

- All PRs must verify constitution compliance
- CI checks enforce code quality standards
- Spec review before implementation begins
- No exceptions without documented justification

---

**Version**: 1.0.0 | **Ratified**: 2025-12-29 | **Last Amended**: 2025-12-29
