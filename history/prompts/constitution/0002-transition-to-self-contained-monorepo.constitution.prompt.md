---
id: "0002"
title: "Transition to self-contained monorepo"
stage: "constitution"
date: "2025-12-31"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "002-fullstack-web"
user: "tariq"
command: "go ahead and update them"
labels: ["architecture", "monorepo", "constitution"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - CLAUDE.md
tests:
  - none
---

## Prompt

go ahead and update them

## Response snapshot

I've updated the Constitution and CLAUDE.md to formalize the self-contained monorepo structure.

### Key points for the update:
1.  **Directory Mapping**: Define `/apps/00X-name/` as the root for phase-specific code.
2.  **Self-Containment**: Explicitly state that each phase must include its own domain logic, adapters, and tests.
3.  **Branching**: `main` contains all merged phases; development happens in `phase-N` branches.

## Outcome

- ✅ Impact: Project structure now supports sequential phase snapshots in a single repository.
- 🧪 Tests: none
- 📁 Files: updated constitution and global rules
- 🔁 Next prompts: Start moving/creating phase directories
- 🧠 Reflection: Option A (Self-Contained) is best for educational clarity but requires discipline with duplication.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): n/a
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): n/a
