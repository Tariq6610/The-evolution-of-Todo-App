# UI/UX Agent Updates - Next.js 14+ & Tailwind CSS v3

**Date**: 2026-01-01

---

## What Was Updated

Updated UI/UX agent configuration and documentation with latest features from:
- **Next.js 14+** - App Router, Server Components, Server Actions
- **Tailwind CSS v3** - Modern responsive patterns, focus-visible states

---

## Key Changes

### 1. Updated Core Technologies

**Added:**
- Next.js 14+ with App Router, Server Components, Server Actions
- React Hook Form + Zod for form validation
- Lucide React (modern icon library)
- Tailwind CSS v3 patterns

### 2. Server Components Pattern

**New Best Practices Added:**

```tsx
// Server Component (default, no "use client")
export default async function DashboardPage() {
  const tasks = await getTasks()
  return <TaskList tasks={tasks} />
}

// Client Component (interactive)
"use client"

export function TaskList({ tasks }: { tasks: Task[] }) {
  const [selected, setSelected] = useState(null)
  // Interactive state
}
```

### 3. Server Actions Pattern

**'use server' Directive:**
```tsx
// app/actions/tasks.ts
'use server'

export async function createTask(formData: FormData) {
  'use server'
  // Database operations
  revalidatePath('/dashboard')
}
```

### 4. Cache Management

**Next.js Cache API:**
```tsx
import { cacheTag, updateTag } from 'next/cache'

export const TASKS_CACHE_TAG = 'tasks'

export async function invalidateTasks() {
  'use server'
  updateTag(TASKS_CACHE_TAG)
}
```

### 5. Modern Tailwind CSS Patterns

**Responsive Breakpoints (v3):**
```tsx
// Updated breakpoints
<div className="p-4 md:p-6 lg:p-8 xl:p-12">
  {/* Modern responsive padding */}
</div>

// Focus-visible for accessibility
<button className="focus-visible:outline-none focus-visible:ring-2">
  {/* Ring only on keyboard focus */}
</button>
```

### 6. Focus Management Best Practices

**Accessibility Enhancement:**
```tsx
// Good: focus-visible (keyboard-only focus)
<button className="focus-visible:ring-2 focus-visible:ring-offset-2">
  Click Me
</button>

// Avoid: Regular focus (appears on all interactions)
<button className="focus:ring-2">
  Focuses on mouse click too
</button>
```

### 7. Component "use client" Directive

**When to Add:**
- Interactive components (useState, useEffect, event handlers)
- Browser APIs (localStorage, window)
- Animations and transitions

**When NOT to Add:**
- Static UI with props
- Server-side data fetching
- Form actions (use 'use server' instead)

### 8. Updated shadcn/ui Component List

**Added New Components:**
- `ScrollArea` - Scrollable content areas
- `Avatar` - User profile images
- `Command` - Quick actions search (command palette)

---

## Example: Modern Server Component

```tsx
// app/dashboard/page.tsx
import { getTasks } from '@/lib/data'
import { TaskList } from './task-list'
import { CreateTaskForm } from './create-task-form'
import { cacheTag } from 'next/cache'

export default async function DashboardPage() {
  'use server'
  cacheTag('tasks')  // Cache this page

  const tasks = await getTasks()

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Dashboard</h1>
      <TaskList initialTasks={tasks} />
      <CreateTaskForm />
    </div>
  )
}
```

---

## Example: Modern Client Component

```tsx
// components/features/task-list.tsx
"use client"

import * as React from "react"
import { TaskCard } from "./task-card"

export function TaskList({ initialTasks }: { initialTasks: Task[] }) {
  const [tasks, setTasks] = useState(initialTasks)

  const toggleTask = (id: string) => {
    setTasks(tasks.map(t =>
      t.id === id
        ? { ...t, status: t.status === 'completed' ? 'pending' : 'completed' }
        : t
    ))
  }

  return (
    <div className="space-y-2">
      {tasks.map(task => (
        <TaskCard
          key={task.id}
          task={task}
          onToggle={toggleTask}
        />
      ))}
    </div>
  )
}
```

---

## Example: Server Action with Cache Invalidation

```tsx
// app/actions/tasks.ts
'use server'

import { db } from '@/lib/db'
import { revalidatePath, updateTag } from 'next/cache'

export async function createTask(formData: FormData) {
  'use server'

  const title = formData.get('title') as string
  const description = formData.get('description') as string

  await db.insert('tasks', {
    title,
    description,
    status: 'pending',
  })

  // Invalidate cache and refresh UI
  revalidatePath('/dashboard')
  updateTag('tasks')

  return { success: true }
}
```

---

## Example: Form with Zod Validation

```tsx
// components/forms/task-form.tsx
"use client"

import * as React from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  Form,
  FormControl,
  FormField,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"

const taskSchema = z.object({
  title: z.string().min(1, "Title is required").max(100, "Too long"),
  description: z.string().max(500, "Too long").optional(),
})

export function TaskForm() {
  const form = useForm<z.infer<typeof taskSchema>>({
    resolver: zodResolver(taskSchema),
    defaultValues: { title: "" },
  })

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        <FormField
          control={form.control}
          name="title"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Title</FormLabel>
              <FormControl>
                <Input placeholder="What needs to be done?" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Create Task</Button>
      </form>
    </Form>
  )
}
```

---

## Updated Checklists

### Component Checklist (Updated)

- [ ] TypeScript types for all props
- [ ] Uses shadcn/ui base components where appropriate
- [ ] Tailwind classes follow design system
- [ ] Responsive design (mobile-first)
- [ ] Accessibility with focus-visible: (not focus:)
- [ ] Proper semantic HTML
- [ ] Reusable and composable
- [ ] Has variants if needed (using CVA)
- [ ] Proper forwardRef if DOM element
- [ ] "use client" if interactive
- [ ] No "use client" if static/Server Component

### Form Checklist (Updated)

- [ ] Zod schema with proper validation
- [ ] React Hook Form integration
- [ ] Label for every input
- [ ] ARIA attributes for accessibility
- [ ] Error messages display properly
- [ ] Submit button with loading state
- [ ] 'use server' directive for form actions
- [ ] Cache invalidation on mutations

---

## Migration Guide

### From Old Next.js Patterns

**Old (Pages Router):**
```tsx
// pages/dashboard.tsx
export default function Dashboard() {
  return <div>...</div>
}
```

**New (App Router):**
```tsx
// app/dashboard/page.tsx
export default async function Dashboard() {
  return <div>...</div>
}
```

### From Old Tailwind Patterns

**Old Focus States:**
```tsx
<button className="focus:ring-2">
  {/* Focused on mouse AND keyboard */}
</button>
```

**New Focus States:**
```tsx
<button className="focus-visible:ring-2">
  {/* Focused on keyboard only */}
</button>
```

---

## Resources

### Documentation
- Next.js 14+ App Router: https://nextjs.org/docs/app
- Server Components: https://nextjs.org/docs/app/building-your-application/rendering
- Server Actions: https://nextjs.org/docs/app/building-your-application/data-fetching
- Tailwind CSS v3: https://tailwindcss.com/docs

### Key Differences

| Feature | Old Version | New Version (14+) |
|----------|------------|----------------|
| Router | Pages Router | App Router |
| Data Fetching | useEffect, fetch | Server Components, Server Actions |
| Forms | Manual state | React Hook Form + Zod |
| Caching | Manual | cacheTag(), updateTag() |
| Focus States | focus: | focus-visible: |
| Components | Everything client | Server + Client split |

---

**Status**: ✅ Updated with Next.js 14+ and Tailwind CSS v3 best practices
**Files Updated**: `.claude/agents/ui-ux.md`, `.specify/UI-UX.md`
