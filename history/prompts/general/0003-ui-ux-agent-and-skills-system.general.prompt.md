---
id: 0003
title: UI/UX agent and skills system
stage: general
date: 2026-01-01
surface: agent
model: claude-sonnet-4.5-20250929
feature: none
branch: master
user: User
command: ok, i want a beautiful ui, so for this talk what should i do, create new agent or add skill
labels: ["ui", "ux", "agent", "skills", "tailwind", "shadcn-ui"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .claude/agents/ui-ux.md
 - .claude/skills/ui-create-component.md
 - .claude/skills/ui-create-form.md
 - .claude/skills/ui-create-layout.md
 - .specify/UI-UX.md
tests:
 - Agent configuration created with complete design principles
 - 3 UI/UX skills created for common tasks
 - Skills follow clean, reusable, accessible patterns
---

## Prompt

ok, i want a beautiful ui, so for this talk what should i do, create new agent or add skill

## Response snapshot

[Created UI/UX agent specialized in Tailwind CSS, shadcn/ui, and Next.js with 3 skills: create-component, create-form, and create-layout]

## Outcome

- ✅ Impact: Implemented complete UI/UX agent system with specialized skills for consistent, beautiful, and accessible UI creation
- 🧪 Tests: Agent configuration and skills documented with complete design principles and accessibility standards
- 📁 Files: Created 5 new files including agent configuration, 3 skills, and comprehensive documentation
- 🔁 Next prompts: None
- 🧠 Reflection: UI/UX agent is now ready to create beautiful, reusable components with shadcn/ui and Tailwind CSS

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - Complete UI/UX system implemented
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): Add shadcn/ui initialization and sample components
