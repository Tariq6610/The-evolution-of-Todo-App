# UI: Create Form

Creates a beautiful, accessible form with validation using Tailwind CSS, shadcn/ui components, and React Hook Form + Zod.

## Usage

```
/sp.ui.create-form <form-name> --fields "<field1> <field2> ..." [--description "<desc>"]
```

## Examples

```bash
# Create task form
/sp.ui.create-form TaskForm --fields "title description priority status tags" --description "Create or edit tasks"

# Create login form
/sp.ui.create-form LoginForm --fields "email password remember" --description "User login form"

# Create signup form
/sp.ui.create-form SignUpForm --fields "name email password confirmPassword" --description "User registration form"
```

## Form Creation Rules

1. **File Location**: `apps/002-fullstack-web/frontend/components/forms/<FormName>.tsx`

2. **Dependencies**:
   - React Hook Form for form management
   - Zod for schema validation
   - shadcn/ui components (Input, Button, Label, etc.)

3. **Form Structure**:
   ```tsx
   "use client"

   import * as React from "react"
   import { useForm } from "react-hook-form"
   import { zodResolver } from "@hookform/resolvers/zod"
   import * as z from "zod"
   import { Button } from "@/components/ui/button"
   import { Input } from "@/components/ui/input"
   import { Label } from "@/components/ui/label"
   import {
     Form,
     FormControl,
     FormField,
     FormItem,
     FormLabel,
     FormMessage,
   } from "@/components/ui/form"

   const formSchema = z.object({
     fieldName: z.string().min(1, "Required"),
   })

   export function FormName({ onSubmit, defaultValues }: FormNameProps) {
     const form = useForm<z.infer<typeof formSchema>>({
       resolver: zodResolver(formSchema),
       defaultValues,
     })

     return (
       <Form {...form}>
         <form onSubmit={form.handleSubmit(onSubmit)}>
           {/* Form fields */}
         </form>
       </Form>
     )
   }
   ```

4. **Field Types**:
   - `text` - String input
   - `email` - Email validation
   - `password` - Password input
   - `number` - Number input
   - `textarea` - Multi-line text
   - `select` - Dropdown selection
   - `checkbox` - Boolean toggle
   - `date` - Date picker
   - `tags` - Tag input (array of strings)

5. **Validation Rules**:
   - Required fields: `z.string().min(1)`
   - Email: `z.string().email()`
   - Minimum length: `z.string().min(5)`
   - Maximum length: `z.string().max(100)`
   - Number range: `z.number().min(0).max(100)`
   - Pattern matching: `z.string().regex(/pattern/)`

6. **Accessibility**:
   - Label for every input
   - ARIA attributes for errors
   - Keyboard navigation
   - Focus management

7. **Responsive Design**:
   - Stack inputs on mobile
   - Grid layout on desktop

## Field Mappings

| Field Name | Type | Component | Validation |
|------------|------|-----------|------------|
| `title` | text | Input | required, min: 1 |
| `description` | textarea | Textarea | optional |
| `email` | email | Input | email, required |
| `password` | password | Input | required, min: 8 |
| `priority` | select | Select | required, enum |
| `status` | select | Select | required, enum |
| `tags` | tags | Input + tags | optional, array |
| `remember` | checkbox | Checkbox | boolean |
| `date` | date | DatePicker | required |

## Example: TaskForm Component

```tsx
"use client"

import * as React from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

const taskSchema = z.object({
  title: z.string().min(1, "Title is required").max(100, "Title too long"),
  description: z.string().max(500, "Description too long").optional(),
  priority: z.enum(["low", "medium", "high"]),
  tags: z.array(z.string()).optional(),
})

export interface TaskFormValues {
  title: string
  description?: string
  priority: "low" | "medium" | "high"
  tags?: string[]
}

export interface TaskFormProps {
  onSubmit: (values: TaskFormValues) => void
  defaultValues?: Partial<TaskFormValues>
  submitLabel?: string
  isSubmitting?: boolean
}

export function TaskForm({
  onSubmit,
  defaultValues = { title: "", priority: "medium" },
  submitLabel = "Create Task",
  isSubmitting = false,
}: TaskFormProps) {
  const form = useForm<TaskFormValues>({
    resolver: zodResolver(taskSchema),
    defaultValues,
  })

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        {/* Title Field */}
        <FormField
          control={form.control}
          name="title"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Title</FormLabel>
              <FormControl>
                <Input
                  placeholder="What needs to be done?"
                  {...field}
                  aria-describedby="title-description"
                />
              </FormControl>
              <p id="title-description" className="text-sm text-muted-foreground">
                Keep it short and clear
              </p>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Description Field */}
        <FormField
          control={form.control}
          name="description"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Description</FormLabel>
              <FormControl>
                <Textarea
                  placeholder="Add more details..."
                  rows={3}
                  {...field}
                  aria-describedby="description-description"
                />
              </FormControl>
              <p id="description-description" className="text-sm text-muted-foreground">
                Optional: Max 500 characters
              </p>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Priority Field */}
        <FormField
          control={form.control}
          name="priority"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Priority</FormLabel>
              <Select onValueChange={field.onChange} defaultValue={field.value}>
                <FormControl>
                  <SelectTrigger aria-describedby="priority-description">
                    <SelectValue placeholder="Select priority" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  <SelectItem value="low">Low</SelectItem>
                  <SelectItem value="medium">Medium</SelectItem>
                  <SelectItem value="high">High</SelectItem>
                </SelectContent>
              </Select>
              <p id="priority-description" className="text-sm text-muted-foreground">
                Higher priority tasks appear first
              </p>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Tags Field */}
        <FormField
          control={form.control}
          name="tags"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Tags</FormLabel>
              <FormControl>
                <Input
                  placeholder="work, personal, urgent (comma separated)"
                  {...field}
                  aria-describedby="tags-description"
                />
              </FormControl>
              <p id="tags-description" className="text-sm text-muted-foreground">
                Optional: Separate tags with commas
              </p>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Submit Button */}
        <Button type="submit" disabled={isSubmitting} className="w-full">
          {isSubmitting ? "Creating..." : submitLabel}
        </Button>
      </form>
    </Form>
  )
}
```

## Form Props Interface

```tsx
export interface FormNameProps {
  onSubmit: (values: FormValues) => void | Promise<void>
  defaultValues?: Partial<FormValues>
  submitLabel?: string
  isSubmitting?: boolean
  onCancel?: () => void
}
```

## Checklist

After creating form, verify:
- [ ] Zod schema with proper validation
- [ ] React Hook Form integration
- [ ] Label for every input
- [ ] ARIA attributes for accessibility
- [ ] Error messages display properly
- [ ] Submit button with loading state
- [ ] Cancel button (if needed)
- [ ] Responsive design
- [ ] Keyboard navigation works
- [ ] Focus states visible
