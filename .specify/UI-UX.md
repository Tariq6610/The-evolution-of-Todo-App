# UI/UX Agent - Quick Start

**Specialized in beautiful, accessible UI using Tailwind CSS, shadcn/ui, and Next.js 14**

---

## What Was Created

```
✅ .claude/agents/ui-ux.md                      # Agent configuration
✅ .claude/skills/ui-create-component.md        # Component creation skill
✅ .claude/skills/ui-create-form.md             # Form creation skill
✅ .claude/skills/ui-create-layout.md           # Layout creation skill
✅ .specify/UI-UX.md                            # Full documentation
```

---

## Agent Capabilities

### Technologies
- **Tailwind CSS v3** - Utility-first CSS with modern responsive patterns
- **shadcn/ui** - High-quality accessible components
- **Next.js 14+** - App Router, Server Components, Server Actions
- **TypeScript** - Type-safe components
- **CVA** - Component variant management
- **React Hook Form + Zod** - Form validation
- **Lucide React** - Modern icon library

### Design Principles
1. Clean, reusable components
2. Consistent design system
3. Mobile-first responsive
4. Accessibility first (WCAG 2.1 AA)
5. Modern aesthetics
6. Performance optimized

---

## Component Architecture

```
apps/002-fullstack-web/frontend/
├── components/
│   ├── ui/              # Base components (shadcn/ui)
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   ├── card.tsx
│   │   └── ...
│   │
│   ├── features/        # Domain-specific components
│   │   ├── task-list.tsx
│   │   ├── task-card.tsx
│   │   └── ...
│   │
│   └── layout/          # Page layouts
│       ├── header.tsx
│       └── sidebar.tsx
│
└── lib/
    └── utils.ts         # cn() utility for class merging
```

---

## Using the Skills

### Create a Component

```bash
# Invoke the skill
/sp.ui.create-component TaskCard --description "Display individual task with status, priority, and actions"
```

**Output**: Clean, reusable component in `components/features/TaskCard.tsx`

---

### Create a Form

```bash
# Invoke the skill
/sp.ui.create-form TaskForm --fields "title description priority tags" --description "Create or edit tasks"
```

**Output**: Form with validation using React Hook Form + Zod

---

### Create a Layout

```bash
# Invoke the skill
/sp.ui.create-layout Dashboard --type dashboard --description "Main dashboard with sidebar and content area"
```

**Output**: Responsive layout with navigation

---

## When to Invoke the UI/UX Agent

### Creating New UI
- "Create a beautiful task list component"
- "Design a responsive dashboard layout"
- "Make this page look better"

### Design System Work
- "Create a color scheme for our app"
- "Define button and input variants"

### Responsive Design
- "Make this layout mobile-responsive"
- "Add dark mode support"

### Accessibility
- "Ensure this component is WCAG 2.1 AA compliant"
- "Add keyboard navigation"

---

## Component Examples

### Base Component (shadcn/ui)
```tsx
// components/ui/button.tsx
import { cva, type VariantProps } from "class-variance-authority"

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground",
        outline: "border border-input",
      },
      size: {
        default: "h-10 px-4",
        sm: "h-9 px-3",
      },
    },
  }
)

export interface ButtonProps extends VariantProps<typeof buttonVariants> {
  className?: string
}
```

---

### Feature Component
```tsx
// components/features/task-list.tsx
export interface Task {
  id: string
  title: string
  status: "pending" | "completed"
  priority: "low" | "medium" | "high"
}

export function TaskList({ tasks, onToggle, onDelete }: TaskListProps) {
  return (
    <div className="space-y-2">
      {tasks.map((task) => (
        <TaskCard
          key={task.id}
          task={task}
          onToggle={() => onToggle(task.id)}
          onDelete={() => onDelete(task.id)}
        />
      ))}
    </div>
  )
}
```

---

## Design System

### Utility Function
```tsx
// lib/utils.ts
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

### Usage
```tsx
<div className={cn("base-class", isActive && "active-class")} />
```

---

### Responsive Design
```tsx
// Mobile first
<div className="p-4">          {/* Mobile */}
<div className="p-4 md:p-6">   {/* Tablet */}
<div className="p-4 md:p-6 lg:p-8"> {/* Desktop */}
```

---

### Typography
```tsx
<h1 className="text-4xl font-bold lg:text-5xl">Title</h1>
<p className="text-base lg:text-lg">Body text</p>
```

---

### Spacing
```tsx
<div className="p-4">      {/* 16px */}
<div className="p-6">      {/* 24px */}
<div className="space-y-2"> {/* Vertical gap */}
<div className="space-x-4"> {/* Horizontal gap */}
```

---

## Accessibility Checklist

Every component must have:
- [ ] Semantic HTML elements
- [ ] ARIA labels where needed
- [ ] Keyboard navigation
- [ ] Visible focus states
- [ ] Color contrast ≥ 4.5:1

**Example: Accessible Button**
```tsx
<button
  aria-label="Delete task"
  onClick={onDelete}
>
  <TrashIcon />
</button>
```

---

## Component Checklist

Before considering complete:
- [ ] TypeScript types for all props
- [ ] Uses shadcn/ui base components
- [ ] Tailwind classes follow design system
- [ ] Responsive design (mobile-first)
- [ ] Accessibility (ARIA, keyboard, focus)
- [ ] Proper semantic HTML
- [ ] Reusable and composable
- [ ] Variants using CVA (if needed)
- [ ] forwardRef (if DOM element)

---

## Skills Reference

| Skill | Description |
|-------|-------------|
| `/sp.ui.create-component` | Create reusable UI component |
| `/sp.ui.create-form` | Create form with validation |
| `/sp.ui.create-layout` | Create page layout |

---

## Installing shadcn/ui

```bash
# Install shadcn/ui CLI
npm install -D shadcn-ui

# Initialize in frontend
cd apps/002-fullstack-web/frontend
npx shadcn-ui@latest init

# Add components
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add input
```

---

## Workflow with Implementation Agent

```
Implementation Agent
    ↓
Completes backend logic
    ↓
Needs UI for feature
    ↓
Invokes: /sp.ui.create-component "TaskCard"
    ↓
UI/UX skill executes
    ↓
Returns beautiful component
    ↓
Implementation Agent integrates
```

**Result:** Implementation agent creates UI without design expertise.

---

## Success Criteria

UI/UX system succeeds when:
- ✅ All components follow consistent patterns
- ✅ shadcn/ui used appropriately
- ✅ Components are clean, reusable, and typed
- ✅ Design system enforced
- ✅ Accessibility meets WCAG 2.1 AA
- ✅ Responsive on all breakpoints
- ✅ Skills produce consistent, high-quality UI
- ✅ No manual coordination needed

---

## Full Documentation

See `.claude/agents/ui-ux.md` for:
- Complete component architecture
- Design system patterns
- shadcn/ui integration
- Accessibility standards
- Component examples

---

**Status**: ✅ Implemented and Ready
**Version**: 1.0.0
**Date**: 2026-01-01
