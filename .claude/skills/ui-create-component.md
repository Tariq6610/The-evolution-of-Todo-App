# UI: Create Component

Creates a clean, reusable, and accessible UI component using Tailwind CSS, shadcn/ui patterns, and TypeScript.

## Usage

```
/sp.ui.create-component <component-name> [--variant <type>] [--description "<desc>"]
```

## Examples

```bash
# Create a card component
/sp.ui.create-component TaskCard --description "Display individual task with status, priority, and actions"

# Create a badge component with variants
/sp.ui.create-component Badge --variant "status|priority" --description "Colored badges for task status and priority"

# Create a container component
/sp.ui.create-component Container --description "Responsive container with max-width"
```

## Component Creation Rules

1. **File Location**: `apps/002-fullstack-web/frontend/components/{type}/{ComponentName}.tsx`
   - `{type}` = `ui`, `features`, or `layout`
   - Use shadcn/ui base components for `ui/` type
   - Create feature-specific components for `features/` type

2. **TypeScript Types**:
   ```tsx
   export interface ComponentNameProps {
     // Props with proper TypeScript types
   }
   ```

3. **Component Structure**:
   ```tsx
   "use client"

   import * as React from "react"
   import { cn } from "@/lib/utils"
   import { Button } from "@/components/ui/button"

   export interface ComponentNameProps {
     className?: string
     // ... other props
   }

   export function ComponentName({ className, ...props }: ComponentNameProps) {
     return (
       <div className={cn("base-classes", className)} {...props}>
         {/* Component content */}
       </div>
     )
   }
   ```

4. **Use CVA for Variants**:
   ```tsx
   import { cva, type VariantProps } from "class-variance-authority"

   const componentVariants = cva("base-classes", {
     variants: {
       variant: {
         default: "default-classes",
         primary: "primary-classes",
       },
       size: {
         sm: "sm-classes",
         md: "md-classes",
         lg: "lg-classes",
       },
     },
     defaultVariants: {
       variant: "default",
       size: "md",
     },
   })
   ```

5. **Accessibility**:
   - Use semantic HTML elements
   - Add ARIA labels where needed
   - Ensure keyboard navigation works
   - Include focus states

6. **Responsive Design**:
   - Mobile-first approach
   - Use Tailwind breakpoints: `sm:`, `md:`, `lg:`, `xl:`

7. **forwardRef** (for DOM elements):
   ```tsx
   export const ComponentName = React.forwardRef<
     HTMLDivElement,
     ComponentNameProps
   >(({ className, ...props }, ref) => {
       return <div ref={ref} className={cn(...)} {...props} />
   })
   ComponentName.displayName = "ComponentName"
   ```

## Output

The skill creates:
1. Component file with TypeScript types
2. Proper imports and structure
3. CVA variants if needed
4. Accessibility attributes
5. Responsive design patterns
6. Export statement with displayName

## Component Type Guide

| Type | When to Use | Location |
|------|-------------|----------|
| `ui` | Base, reusable components | `components/ui/` |
| `features` | Domain-specific features | `components/features/` |
| `layout` | Page layout components | `components/layout/` |

## Example: TaskCard Component

```tsx
"use client"

import * as React from "react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Checkbox } from "@/components/ui/checkbox"

export interface Task {
  id: string
  title: string
  description?: string
  status: "pending" | "completed"
  priority: "low" | "medium" | "high"
  tags: string[]
}

export interface TaskCardProps {
  task: Task
  onToggle?: (id: string) => void
  onDelete?: (id: string) => void
  className?: string
}

export function TaskCard({ task, onToggle, onDelete, className }: TaskCardProps) {
  const priorityColors = {
    low: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300",
    medium: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300",
    high: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300",
  }

  return (
    <div className={cn(
      "flex items-center gap-4 rounded-lg border bg-card p-4 text-card-foreground shadow-sm transition-all hover:shadow-md",
      className
    )}>
      <Checkbox
        checked={task.status === "completed"}
        onCheckedChange={() => onToggle?.(task.id)}
        aria-label={`Toggle ${task.title}`}
      />

      <div className="flex-1 space-y-1">
        <h3 className={cn(
          "font-semibold",
          task.status === "completed" && "line-through text-muted-foreground"
        )}>
          {task.title}
        </h3>

        {task.description && (
          <p className="text-sm text-muted-foreground">{task.description}</p>
        )}

        <div className="flex flex-wrap gap-2">
          <Badge className={priorityColors[task.priority]} variant="outline">
            {task.priority}
          </Badge>

          {task.tags.map((tag) => (
            <Badge key={tag} variant="secondary" className="text-xs">
              {tag}
            </Badge>
          ))}
        </div>
      </div>

      <Button
        variant="ghost"
        size="icon"
        onClick={() => onDelete?.(task.id)}
        aria-label="Delete task"
      >
        <TrashIcon className="h-4 w-4" />
      </Button>
    </div>
  )
}

function TrashIcon(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M3 6h18" />
      <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6" />
      <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2" />
    </svg>
  )
}
```

## Checklist

After creating component, verify:
- [ ] TypeScript types for all props
- [ ] Proper semantic HTML
- [ ] Accessibility (ARIA, keyboard nav, focus states)
- [ ] Responsive design (mobile-first)
- [ ] Uses shadcn/ui base components where appropriate
- [ ] Clean Tailwind class names using cn()
- [ ] Component is reusable and composable
- [ ] Has displayName if using forwardRef
- [ ] Follows naming conventions (PascalCase)
