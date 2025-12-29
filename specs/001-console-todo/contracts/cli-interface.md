# CLI Interface Contracts: Phase I - In-Memory Console Todo App

**Feature**: 001-console-todo | **Date**: 2025-12-29

## Menu System Contract

**Requirement Reference**: FR-012 - System MUST present an interactive menu with numbered options

### Main Menu

```
=== Todo Menu ===
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Complete/Incomplete
0. Exit

Enter choice (0-5): _
```

**Invariants**:
- Menu always displays 6 options (0-5)
- Options 1-5 are operations, 0 exits
- Prompt appears at bottom after menu
- Newline clears previous output
- Menu redisplays after each operation completes

### Menu Option Behaviors

| Option | Action | Returns | Next State |
|--------|--------|---------|-------------|
| 0 | Exit application | None | Terminates program |
| 1 | Launch Add Task flow | Task created/None | Redisplay menu |
| 2 | View All Tasks | None | Redisplay menu |
| 3 | Launch Update Task flow | Task updated/None | Redisplay menu |
| 4 | Launch Delete Task flow | Task deleted/None | Redisplay menu |
| 5 | Launch Toggle Status flow | Status toggled/None | Redisplay menu |

## Input Contracts

### Task Title Input

**Requirement Reference**: FR-001, FR-007

```
Enter task title: [user input]
```

**Validation Rules**:
- Cannot be empty
- Cannot be whitespace-only (strip then check length)
- Minimum 1 character after stripping
- No maximum length (but reasonable limit ~500 chars)

**Error Cases**:
- Empty/whitespace title: "Error: Task title cannot be empty. Please try again."
- Returns to prompt (re-ask) until valid

### Task Description Input

**Requirement Reference**: FR-001

```
Enter task description (optional, press Enter to skip): [user input]
```

**Validation Rules**:
- Optional - empty string valid
- Any string (including whitespace) valid
- No validation on content

**Behavior**:
- Press Enter without typing = None (no description)
- Any text = description string

### Priority Selection

**Requirement Reference**: FR-010

```
Select priority:
1. Low
2. Medium (default)
3. High

Enter choice (1-3) or press Enter for default: _
```

**Validation Rules**:
- Must be 1, 2, or 3
- Enter without input = 2 (Medium, default)

**Error Cases**:
- Invalid choice: "Error: Invalid priority. Enter 1, 2, 3, or press Enter for default."
- Returns to prompt until valid

**Mapping**:
- 1 → Priority.LOW
- 2 → Priority.MEDIUM
- 3 → Priority.HIGH

### Tags Input

**Requirement Reference**: FR-011

```
Enter tags (comma-separated, optional, press Enter to skip): [user input]
```

**Validation Rules**:
- Optional - empty string valid
- Comma-separated list of tag strings
- Tags are stripped of leading/trailing whitespace

**Behavior**:
- Press Enter without typing = [] (no tags)
- "work,home" → ["work", "home"]
- "work, home, urgent " → ["work", "home", "urgent"]

### Task ID Input

**Requirement Reference**: FR-008 (error handling)

```
Enter task ID: [user input]
```

**Validation Rules**:
- Must match existing task ID in storage
- Error if not found: "Error: Task not found. Please check the ID and try again."

**Behavior**:
- Returns to operation start (menu or input collection) on error
- Does not crash on invalid ID

## Display Contracts

### Task List Display

**Requirement Reference**: FR-003, FR-014

```
=== All Tasks (3) ===

[1] Buy groceries
    Status: [ ] Pending
    Priority: Medium
    Description: Weekly shopping
    Tags: home
    Created: 2025-12-29 10:30:00
    Updated: 2025-12-29 10:30:00

[2] Finish report
    Status: [X] Completed
    Priority: High
    Description: Q4 financial report
    Tags: work, urgent
    Created: 2025-12-28 14:00:00
    Updated: 2025-12-29 09:15:00

[3] Call mom
    Status: [ ] Pending
    Priority: Low
    Description: (none)
    Tags: family
    Created: 2025-12-29 11:00:00
    Updated: 2025-12-29 11:00:00

---
Total: 3 tasks (1 completed, 2 pending)
```

**Format Rules**:
- Header: `=== All Tasks (<count>) ===`
- Each task starts with `[<display-id>] <title>`
- Status: `[ ]` for pending, `[X]` for completed
- Priority: Always shown (Low/Medium/High)
- Description: `(none)` if None/empty
- Tags: Comma-separated if present, blank line if empty
- Timestamps: Format `YYYY-MM-DD HH:MM:SS`
- Footer: Task count summary with completion breakdown

**Empty List**:
```
=== All Tasks (0) ===

No tasks yet. Add your first task to get started!
```

### Single Task Display

Used for update confirmation and after operations.

```
=== Task Details ===

ID: abc123def
Title: Buy groceries
Status: Completed [X]
Priority: High
Description: Weekly shopping for the week
Tags: home, groceries
Created: 2025-12-29 10:30:00
Updated: 2025-12-29 11:45:00
```

**Format Rules**:
- Fields shown in ID → Title → Status → Priority → Description → Tags → Created → Updated order
- Status includes checkbox `[ ]` or `[X]` for visual clarity
- Description or Tags empty: field omitted or shown as `(none)`

### Success Messages

**Add Task**:
```
✓ Task created successfully!
```

**Update Task**:
```
✓ Task updated successfully!
```

**Delete Task**:
```
✓ Task deleted successfully!
```

**Toggle Status**:
```
✓ Task marked as completed!
```
or
```
✓ Task marked as pending!
```

### Error Messages

**FR-007**: Empty title
```
Error: Task title cannot be empty. Please try again.
```

**FR-008**: Task not found
```
Error: Task not found. Please check the ID and try again.
```

**FR-013**: Invalid menu choice
```
Error: Invalid choice. Please enter a number between 0 and 5.
```

**FR-013**: Invalid priority choice
```
Error: Invalid priority. Enter 1, 2, 3, or press Enter for default.
```

**General input error**:
```
Error: Invalid input. Please try again.
```

## Flow Contracts

### Add Task Flow

```
[Menu displayed]
User selects 1
    │
    ▼
[Title input prompt]
    ├──► Empty/whitespace → Error → Redisplay prompt
    └───► Valid title
            │
            ▼
[Description input prompt] (optional)
    │
    ▼
[Priority selection prompt] (optional, default Medium)
    ├──► Invalid → Error → Redisplay prompt
    └───► Valid choice
            │
            ▼
[Tags input prompt] (optional)
    │
    ▼
[Task created]
    │
    ▼
[Success message]
    │
    ▼
[Redisplay menu]
```

### View Tasks Flow

```
[Menu displayed]
User selects 2
    │
    ▼
[Task list displayed]
    │
    ▼
[Press Enter to continue...]
    │
    ▼
[Redisplay menu]
```

### Update Task Flow

```
[Menu displayed]
User selects 3
    │
    ▼
[Task ID input]
    ├──► Not found → Error → Return to menu
    └───► Valid ID
            │
            ▼
[Current task displayed]
    │
    ▼
[New title prompt] (optional, press Enter to skip)
    │
    ▼
[New description prompt] (optional, press Enter to skip)
    │
    ▼
[New priority selection] (optional, press Enter to skip)
    │
    ▼
[New tags prompt] (optional, press Enter to skip)
    │
    ▼
[Task updated]
    │
    ▼
[Updated task displayed]
    │
    ▼
[Success message]
    │
    ▼
[Redisplay menu]
```

### Delete Task Flow

```
[Menu displayed]
User selects 4
    │
    ▼
[Task ID input]
    ├──► Not found → Error → Return to menu
    └───► Valid ID
            │
            ▼
[Task to delete displayed]
    │
    ▼
[Confirmation prompt]
Delete this task? (y/N): _
    ├──► No → Return to menu
    └───► Yes
            │
            ▼
[Task deleted]
    │
            ▼
[Success message]
    │
            ▼
[Redisplay menu]
```

### Toggle Status Flow

```
[Menu displayed]
User selects 5
    │
    ▼
[Task ID input]
    ├──► Not found → Error → Return to menu
    └───► Valid ID
            │
            ▼
[Task displayed]
    │
    ▼
[Status toggled]
    │
    ▼
[Success message (pending ↔ completed)]
    │
    ▼
[Updated task displayed]
    │
    ▼
[Redisplay menu]
```

### Exit Flow

```
[Menu displayed]
User selects 0
    │
    ▼
[Exit confirmation]
Exit application? All unsaved data will be lost. (y/N): _
    ├──► No → Redisplay menu
    └───► Yes
            │
            ▼
[Goodbye message]
Thank you for using Todo App!
    │
            ▼
[Program terminates]
```

## Requirements Coverage

| Requirement | Contract Section | Coverage |
|-------------|------------------|----------|
| FR-001 | Add Task Flow | ✅ Title + optional description |
| FR-002 | Task entity | ✅ Unique ID generation |
| FR-003 | Task List Display | ✅ All attributes shown |
| FR-004 | Toggle Status Flow | ✅ Pending ↔ completed |
| FR-005 | Update Task Flow | ✅ Title, description, priority, tags |
| FR-006 | Delete Task Flow | ✅ Delete by ID |
| FR-007 | Task Title Input | ✅ Empty/whitespace validation |
| FR-008 | Task ID Input | ✅ Not found error |
| FR-009 | Task entity | ✅ Timestamps maintained |
| FR-010 | Priority Selection | ✅ Low/Medium/High |
| FR-011 | Tags Input | ✅ Comma-separated, optional |
| FR-012 | Menu System Contract | ✅ Numbered options |
| FR-013 | Error Messages | ✅ All error cases defined |
| FR-014 | Task List Display | ✅ Count shown in header/footer |
| FR-015 | Exit Flow | ✅ Exit from menu |
