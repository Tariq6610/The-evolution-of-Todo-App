---
id: "0009"
title: "Analyze spec plan and tasks"
stage: "explainer"
date: "2026-02-22"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "todo-ai-chatbot"
branch: "phase-3-ai-chatbot"
user: "tariq"
command: "/sp.analyze"
labels: ["analysis", "consistency", "constitution"]
links:
  spec: "specs/todo-ai-chatbot/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - specs/todo-ai-chatbot/spec.md
  - specs/todo-ai-chatbot/plan.md
  - specs/todo-ai-chatbot/tasks.md
tests:
  - none
---

## Prompt

/sp.analyze

## Response snapshot

Performed a cross-artifact consistency and quality analysis across spec.md, plan.md, and tasks.md.
Identified one CRITICAL constitution violation (missing BDD/statistical tests), two MEDIUM issues (ambiguous context window and performance targets), and two LOW/Coverage issues.
Provided a structured report and offered remediation.

## Outcome

- ✅ Impact: Identified critical gaps in testing strategy and ambiguity in context management.
- 🧪 Tests: n/a
- 📁 Files: Modified spec.md and tasks.md (proposed).
- 🔁 Next prompts: Apply remediation edits.
- 🧠 Reflection: The constitution check caught a major requirement (BDD/Statistical tests) that was missed during task generation.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): n/a
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): n/a
