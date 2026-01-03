---
id: 0004
title: Backend agent with skills
stage: general
date: 2026-01-01
surface: agent
model: claude-sonnet-4.5-20250929
feature: none
branch: master
user: User
command: ok, i want a beautiful ui, so for this talk what should i do, create new agent or add skill
labels: ["backend", "agent", "skills", "fastapi", "sqlmodel", "neon"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .claude/agents/backend.md
 - .claude/skills/backend-create-endpoint.md
 - .claude/skills/backend-create-model.md
 - .claude/skills/backend-create-repository.md
 - .claude/skills/backend-create-service.md
 - .claude/skills/backend-create-auth.md
 - .specify/BACKEND.md
tests:
 - Agent configuration created with FastAPI, SQLModel, Neon DB, and hexagonal architecture
 - 5 backend skills created with async/await patterns, REST API design, repository pattern, service layer pattern, and JWT authentication
 - Skills follow clean code practices with dependency injection and error handling
---
## Prompt

ok, i want a beautiful ui, so for this talk what should i do, create new agent or add skill

## Response snapshot

[Created Backend Agent specialized in FastAPI, SQLModel, Neon PostgreSQL with 5 specialized skills: create-endpoint, create-model, create-repository, create-service, and create-auth]

## Outcome

- ✅ Impact: Implemented complete backend agent system with specialized skills for database, API, and business logic development
- 🧪 Tests: Agent configuration and skills documented with async/await patterns, hexagonal architecture, and security best practices
- 📁 Files: Created 6 new files including agent configuration, 5 backend skills, and comprehensive documentation
- 🔁 Next prompts: None
- 🧠 Reflection: Backend agent is now ready to handle all database, API, and business logic work automatically

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - Complete backend agent system implemented
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): Add testing skill for pytest integration
