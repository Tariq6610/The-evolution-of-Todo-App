# Infrastructure Automation System

**Purpose**: Automatically enforces project constitution compliance without manual intervention or agent coordination.

---

## Overview

This system uses **Git pre-commit hooks** to validate all commits against the project constitution. When any agent (or human) runs `git commit`, the validation script automatically executes and blocks non-compliant changes.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│           Any Agent or Developer                            │
│  - Implementation Agent                                    │
│  - Manual git operations                                  │
│  - GUI tools (VS Code, GitHub Desktop)                    │
└─────────────────────────────────────────────────────────────┘
                        │
                        │ git commit
                        ▼
┌─────────────────────────────────────────────────────────────┐
│           .git/hooks/pre-commit                            │
│  (Executes automatically before every commit)              │
└─────────────────────────────────────────────────────────────┘
                        │
                        │ Calls
                        ▼
┌─────────────────────────────────────────────────────────────┐
│  .specify/scripts/validation/validate-workflow.sh         │
│                                                           │
│  Checks:                                                 │
│  1. Branch naming (phase-N-description)                   │
│  2. Feature specification exists (spec.md)                   │
│  3. PHR created (history/prompts/<feature>/)             │
│  4. Python code quality (mypy, ruff)                     │
│  5. TypeScript code quality (eslint, prettier)             │
│  6. Directory structure (apps/00X-phase/)                  │
│  7. Tests pass (pytest)                                   │
└─────────────────────────────────────────────────────────────┘
                        │
                        ├─→ Fail
                        │       ↓
                        │    ❌ Block commit
                        │       ↓
                        │  Agent fixes issues
                        │       ↓
                        │  Agent retries git commit
                        │
                        └─→ Pass
                                ↓
                           ✅ Allow commit
```

## Files

| File | Purpose | Maintained By |
|------|---------|---------------|
| `.git/hooks/pre-commit` | Git hook that triggers validation | Infrastructure Agent |
| `.specify/scripts/validation/validate-workflow.sh` | Main validation script | Infrastructure Agent |
| `.claude/agents/infrastructure.md` | Agent configuration | Infrastructure Agent |
| `.specify/memory/constitution.md` | Project governance rules | Infrastructure Agent (updates) |

## How It Works

### For Agents

**Implementation Agent workflow:**

1. Agent completes feature (code changes, tests)
2. Agent runs: `git commit -m "feat: add task management"`
3. Pre-commit hook triggers automatically
4. Validation script runs
5. **If validation passes**: Commit succeeds ✅
6. **If validation fails**: Git returns error
7. Agent reads error message, fixes issues, retries git commit
8. Repeat until validation passes

**No manual intervention required!**

### For Developers

**Manual git workflow:**

1. Make changes
2. Run: `git commit -m "message"`
3. See validation output:
   - ✅ All checks passed: Commit succeeds
   - ❌ Validation failed: See errors, fix them, retry
4. Repeat step 2

## Validation Checks

### 1. Branch Naming

**Rule**: Branch must follow `phase-<number>-<description>` pattern

**Examples**:
- ✅ `phase-1-console-app`
- ✅ `phase-2-fullstack-web`
- ✅ `phase-3-ai-chatbot`
- ❌ `feature/todo-app`
- ❌ `fix-auth-bug`
- ❌ `main-branch`

**How to fix**:
```bash
# Rename branch
git branch -m old-branch-name phase-2-new-feature
```

---

### 2. Feature Specification

**Rule**: `spec.md` must exist in `specs/<feature-name>/` before committing

**Example**:
- On branch `phase-2-fullstack-web`
- Must have: `specs/fullstack-web/spec.md`

**How to fix**:
```bash
# Create spec
mkdir -p specs/fullstack-web
touch specs/fullstack-web/spec.md

# Fill spec.md (or run /sp.specify)
```

---

### 3. PHR Creation

**Rule**: PHR directory must exist in `history/prompts/<feature-name>/`

**Example**:
- On branch `phase-2-fullstack-web`
- Must have: `history/prompts/fullstack-web/` with at least one PHR

**How to fix**:
```bash
# Create PHR
.specify/scripts/bash/create-phr.sh --title "Feature spec" --stage spec --feature fullstack-web
```

---

### 4. Python Code Quality

**Rules**:
- All functions must have type hints
- Code must pass `mypy --strict`
- Code must pass `ruff check`
- Code must be formatted with `ruff format`

**How to fix**:
```bash
# Type check
mypy --strict src/

# Lint and auto-fix
ruff check --fix src/

# Format code
ruff format src/
```

---

### 5. TypeScript/JavaScript Code Quality

**Rules**:
- TypeScript strict mode enabled
- Code must pass ESLint
- Code must be formatted with Prettier

**How to fix**:
```bash
# Lint
eslint src/

# Format
prettier --write src/
```

---

### 6. Directory Structure

**Rule**: Apps must follow `apps/<phase-id>-<name>/{src,tests,frontend,backend}/`

**Examples**:
- ✅ `apps/001-console-todo/src/`
- ✅ `apps/002-fullstack-web/frontend/`
- ✅ `apps/002-fullstack-web/backend/`
- ❌ `apps/todo-app/code/` (invalid phase ID)

**How to fix**:
- Reorganize files to follow correct structure
- Or commit changes in valid structure

---

### 7. Tests Pass

**Rule**: All tests must pass before committing

**How to fix**:
```bash
# Run tests
pytest tests/

# Fix failing tests
# Then retry git commit
```

---

## Testing Validation Manually

To run validation without committing:

```bash
# Test all validations
.specify/scripts/validation/validate-workflow.sh
```

This is useful for:
- Debugging validation failures
- Checking code quality before committing
- Understanding what validation will check

## Bypassing Validation (Emergencies Only)

**WARNING**: Only bypass in emergencies. Document bypass with a PHR.

```bash
# Bypass pre-commit hook
git commit --no-verify -m "Emergency fix"

# After fixing issues, amend commit
git commit --amend --no-verify
```

## Error Messages

### Example: Branch Naming Fail

```
✗ Branch name 'feature-auth' does not follow phase-N-description pattern
  Expected format: phase-<number>-<short-description>
  Examples: phase-1-console-app, phase-2-fullstack-web
```

**Fix**: Rename branch using `git branch -m`

### Example: Spec Missing

```
✗ Spec file not found: specs/fullstack-web/spec.md
  Branch: phase-2-fullstack-web
  Feature spec must exist before committing changes
```

**Fix**: Create `specs/fullstack-web/spec.md`

### Example: Type Check Fail

```
✗ mypy failed. Run: mypy --strict <files>
src/domain/task.py:15: error: Function is missing a type annotation
```

**Fix**: Add type annotation to function

### Example: Ruff Fail

```
✗ ruff format check failed. Run: ruff format <files>
  To auto-format: ruff format <files>
```

**Fix**: Run `ruff format` on the file(s)

## Adding New Validation Rules

When you need to add a new validation check:

1. Edit `.specify/scripts/validation/validate-workflow.sh`
2. Add a new `validate_<name>()` function
3. Call the function in `main()`
4. Test the script manually
5. Commit the changes (validation will apply to this commit too!)

**Example: Add check for minimum test coverage**

```bash
validate_test_coverage() {
    print_header "Validating Test Coverage"

    if command -v pytest &> /dev/null; then
        coverage=$(pytest --cov=. --cov-report=term-missing 2>/dev/null | grep "TOTAL" | awk '{print $4}' | sed 's/%//')

        if (( $(echo "$coverage < 80" | bc -l) )); then
            print_error "Test coverage is ${coverage}%, minimum 80% required"
            return 1
        fi

        print_success "Test coverage: ${coverage}%"
    fi

    return 0
}
```

Then add to `main()`:
```bash
validate_test_coverage
```

## Updating Constitution

When constitution (`.specify/memory/constitution.md`) changes:

1. Update validation scripts to reflect new rules
2. Add new validation checks if needed
3. Remove obsolete checks
4. Test validation manually
5. Create ADR for significant changes
6. Update this documentation

## Infrastructure Agent Responsibilities

**Do:**
- ✅ Create and maintain validation scripts
- ✅ Configure pre-commit hooks
- ✅ Update checks when constitution changes
- ✅ Monitor compliance patterns
- ✅ Improve validation error messages

**Don't:**
- ❌ Run git commands
- ❌ Coordinate with other agents
- ❌ Intercept commits manually
- ❌ Generate code or features

## Troubleshooting

### Validation Script Not Running

**Symptoms**: Commits succeed even when violating rules

**Solution**: Check if pre-commit hook is executable
```bash
chmod +x .git/hooks/pre-commit
```

### Validation Script Not Found

**Symptoms**: Error "No such file or directory"

**Solution**: Ensure path is correct relative to git root
```bash
ls -la .specify/scripts/validation/
```

### Tools Not Installed

**Symptoms**: "mypy not installed, skipping type checking"

**Solution**: Install required tools
```bash
# Python tools
pip install mypy ruff pytest

# TypeScript tools (if needed)
npm install -D eslint prettier
```

### Validation Too Slow

**Symptoms**: Validation takes > 30 seconds

**Solution**: Optimize validation script or add skip flag for specific checks

## Best Practices

1. **Run validation manually before committing** - Save time by fixing issues early
2. **Read error messages carefully** - They often include fix suggestions
3. **Keep validation fast** - Only check changed files, not entire codebase
4. **Test validation scripts** - After making changes, test manually
5. **Document new rules** - Update this README when adding checks
6. **Use auto-format tools** - ruff format, prettier save time
7. **Fix errors before retrying** - Don't use --no-verify unless emergency

## Success Indicators

Infrastructure automation is working when:
- ✅ No manual coordination needed between agents
- ✅ Invalid commits are blocked automatically
- ✅ Agents can commit without human intervention
- ✅ All code follows constitution
- ✅ Validation failures are clear and actionable
- ✅ Developers understand how to fix violations

## Support

For infrastructure issues:
1. Check validation script output for specific errors
2. Read this documentation for fixes
3. Run validation manually to debug
4. Consult `.claude/agents/infrastructure.md` for agent-specific help
5. Review `.specify/memory/constitution.md` for project rules

---

**Last Updated**: 2026-01-01
**Maintained By**: Infrastructure Agent
**Version**: 1.0.0
