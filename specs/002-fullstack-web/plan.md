# Implementation Plan: Phase II - Full-Stack Web Application

**Branch**: `002-fullstack-web` | **Date**: 2025-12-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-fullstack-web/spec.md`

## Summary

Evolve the Todo application from a Phase I console app to a Phase II full-stack web application. The technical approach involves building a modern web architecture with a Next.js frontend and a FastAPI backend, utilizing SQLModel for ORM and Neon DB (serverless PostgreSQL) for persistent, multi-user storage. Authentication will be managed via JWT to ensure secure data isolation between users.

## Technical Context

**Language/Version**: Python 3.11+, TypeScript 5.0+
**Primary Dependencies**: Next.js 14, FastAPI 0.100+, SQLModel, Pydantic v2, JWT, Tailwind CSS
**Storage**: Neon DB (PostgreSQL) - Migration from SQLite to Neon DB
**Testing**: pytest (backend), Playwright (frontend/E2E), pytest-bdd
**Target Platform**: Cloud (Vercel for frontend, Render/Railway for backend)
**Project Type**: web (frontend + backend)
**Performance Goals**: < 200ms API response p95, < 2s initial page load
**Constraints**: < 200ms p95, strict type checking (mypy/TypeScript), multi-user isolation
**Scale/Scope**: Up to 100 concurrent users, 1000 tasks per user

## Neon DB Migration Plan

### Overview
Migrate from SQLite (development) to Neon DB (production) for enhanced scalability, reliability, and multi-user support. The application is already configured to work with PostgreSQL/Neon DB through conditional connection logic in session.py.

### Migration Strategy
1. **Setup Neon DB Instance**: Create new Neon DB project and database
2. **Configure Connection**: Update environment variables with Neon DB connection string
3. **Connection Handling**: Leverage existing SSL configuration logic in session.py which automatically adds sslmode=require for PostgreSQL connections
4. **Environment Configuration**: Update .env files for development and production
5. **Testing**: Verify all database operations work with Neon DB
6. **Deployment**: Deploy to production with Neon DB connection

### Database Schema Compatibility
- Current SQLModel entities are compatible with PostgreSQL/Neon DB
- The session.py already handles PostgreSQL connection parameters correctly
- Foreign key constraints and indexes will be properly handled by SQLModel
- No schema changes required as SQLModel abstracts database differences

### SSL and Security Configuration
- The existing session.py automatically appends sslmode=require for PostgreSQL connections
- This ensures secure connections to Neon DB
- No additional SSL configuration needed in application code

### Migration Steps Checklist
- [ ] Create Neon DB account and project
- [ ] Obtain connection string from Neon DB dashboard
- [ ] Update DATABASE_URL in .env with Neon DB connection string
- [ ] Test connection locally
- [ ] Run existing tests to verify functionality
- [ ] Deploy to staging/production environment

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Constitution Principle | Compliance Status | Notes |
|---------------------|-------------------|-------|
| Spec-Driven Development | ✅ PASS | Spec exists and covers all Phase II requirements |
| Phase-Based Evolution | ✅ PASS | Phase II stack and features align with roadmap |
| Hexagonal Architecture | ✅ PASS | Plan preserves domain/adapter separation |
| Shared Core Domain Models | ✅ PASS | Task entity will be extended, not broken |
| Phase-Aware Testing | ✅ PASS | BDD + Test-Along strategy specified |
| Code Quality Standards | ✅ PASS | Strict typing and linting enforced for both stacks |

## Project Structure

### Documentation (this feature)

```text
specs/002-fullstack-web/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (OpenAPI spec)
└── tasks.md             # Phase 2 output (to be generated)
```

### Source Code (repository root)

```text
backend/                 # Python FastAPI service
├── src/
│   ├── domain/          # Pure logic (shared/extended from Phase I)
│   ├── adapters/
│   │   ├── db/          # SQLModel/Neon DB implementation
│   │   └── api/         # FastAPI endpoints
│   └── ports/           # Interfaces (shared/extended from Phase I)
└── tests/
    ├── unit/
    └── integration/

frontend/                # Next.js 14 application
├── src/
│   ├── components/      # UI components (Atomic design)
│   ├── pages/           # Next.js app directory structure
│   └── services/        # API client services
└── tests/               # Playwright E2E tests
```

**Structure Decision**: Split repository into `backend/` and `frontend/` directories to facilitate independent scaling, testing, and deployment, while maintaining the Hexagonal Architecture within the backend to preserve the domain logic from Phase I.

## UI Enhancement Addendum

### Overview
This section describes the UI enhancement feature to be added to the existing Todo application. The enhancements include:

1. **Sidebar Navigation**: Add a collapsible sidebar to the dashboard for improved navigation
2. **Framer Motion Animations**: Implement smooth animations and transitions for better user experience
3. **Visual Design Improvements**: Modernize the UI with enhanced styling and visual feedback

### Technical Approach
- Add Framer Motion as a dependency for animations
- Create reusable sidebar component with responsive design
- Apply motion animations to key UI elements (task items, forms, modals)
- Enhance existing components with improved styling and transitions
- Maintain existing functionality while improving visual appeal

### Dependencies
- `framer-motion` for animations and transitions
- Existing Tailwind CSS for styling
- Existing React/Next.js components to be enhanced

### Implementation Strategy
1. Install Framer Motion dependency
2. Create sidebar component with navigation items
3. Integrate sidebar into dashboard layout
4. Add animations to task items and forms
5. Enhance overall visual design

## Dashboard Redesign Addendum

### Overview
Redesign the existing minimal dashboard into a beautiful, insight-driven, and action-oriented overview that summarizes without replicating the Tasks page.

### Design Goals
- **Summarize, not replicate** - Dashboard should provide overview, not full task lists
- **Immediate communication** - Show productivity status, what needs attention, and quick actions
- **Visual style** - Modern, calm, premium feel with motion-enhanced but not distracting interactions

### Required Sections

#### 1. Hero Summary Section (Top)
- Dynamic greeting (e.g., "Good afternoon, Tariq")
- Short productivity summary ("You've completed 18 of 25 tasks")
- Visual progress indicator (circular progress ring or progress bar)
- Subtle entrance animations with count-up numbers

#### 2. Compact Stats Overview
- Total Tasks, Completed, Pending, High Priority
- Compact cards with icons/indicators
- Animated number transitions
- Soft shadows and responsive layout

#### 3. Visual Insights (Lightweight Charts)
- Donut chart for task status distribution
- Bar/stacked chart for priority levels
- Minimal axes, clear color hierarchy
- Smooth entrance animation

#### 4. "Needs Attention" Panels
- High-priority tasks (top 3-5)
- Recently updated tasks
- Card-based layout, clear priority distinction
- Click to navigate to Tasks page

#### 5. Quick Actions Section
- Add new task, Add high-priority task, Navigate to tasks
- Icon-based buttons with hover/tap feedback
- Clean, uncluttered layout

#### 6. Smart Snapshot (Insight Card)
- One intelligent insight derived from data
- Examples: "Most pending tasks are Medium priority"
- Text-focused, optional icon
- No AI/prediction logic

### Technical Approach
- Use existing task data (no backend changes)
- Create reusable dashboard components:
  - `HeroSummary.tsx` - Dynamic greeting + progress
  - `StatsCard.tsx` - Compact stat cards
  - `TaskStatusChart.tsx` - Donut chart for status
  - `PriorityChart.tsx` - Bar chart for priorities
  - `AttentionPanel.tsx` - High-priority/recent tasks
  - `QuickActions.tsx` - Action buttons
  - `SmartInsight.tsx` - Insight card
  - `AnimatedCounter.tsx` - Number animations
- Implement entrance animations using Framer Motion
- Ensure responsive design for mobile/tablet

### Dependencies
- `recharts` for lightweight charts (already in use or add if needed)
- `framer-motion` for animations
- Existing Tailwind CSS for styling

### Visual Guidelines
- Card-based layout with consistent spacing
- Glassmorphism or soft elevated cards
- Framer Motion for: entrance animations, count-ups, progress transitions
- Avoid over-animation
- Excellent mobile and tablet responsiveness
- Graceful empty states with friendly messaging

### Out of Scope (Phase 2)
- Full task lists on dashboard
- Collaboration features
- Real-time updates
- Heavy analytics dashboards
- Backend schema changes

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |
