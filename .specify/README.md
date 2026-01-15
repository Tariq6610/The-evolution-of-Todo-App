# Infrastructure Implementation - Quick Start

## What Was Implemented

✅ Pre-commit hook automatically enforces constitution compliance
✅ Validation script checks all project rules
✅ Infrastructure agent maintains the validation system
✅ No manual coordination needed between agents

## Files Created

```
.git/hooks/pre-commit                           # Git hook (auto-runs before commit)
.specify/scripts/validation/validate-workflow.sh  # Validation logic
.claude/agents/infrastructure.md              # Agent configuration
.specify/INFRASTRUCTURE.md                    # Full documentation
.specify/README.md                            # This file
```

## How It Works

```
Implementation Agent (or you)
    │ Runs: git commit
    │
    ▼ (automatic)
.git/hooks/pre-commit runs
    │
    ▼
Validate-workflow.sh checks:
    ├─→ Branch naming (phase-N-description)
    ├─→ spec.md exists
    ├─→ PHR created
    ├─→ mypy, ruff (Python)
    ├─→ eslint, prettier (TypeScript)
    ├─→ Directory structure
    └─→ Tests pass
    │
    ├─→ Fail → Block commit, show errors
    └─→ Pass → Allow commit
```

## Test It Now

```bash
# Test validation script (no commit)
.specify/scripts/validation/validate-workflow.sh

# Create a test commit (will trigger hook)
echo "test" > test.txt
git add test.txt
git commit -m "Test commit"
# See hook run and check results
```

## Key Benefits

1. **Zero Manual Coordination** - Hook runs automatically
2. **Cannot Be Bypassed** - Works at git level
3. **Universal** - Works with any agent, CLI, or GUI
4. **Self-Correcting** - Agents see errors and fix automatically
5. **Constitution Enforced** - All rules validated automatically

## What Each Check Does

| Check | Enforces | Fails If |
|-------|-----------|-----------|
| Branch Naming | phase-N-description pattern | Wrong format |
| Spec Exists | spec-driven development | No spec.md |
| PHR Created | Traceability | No PHR records |
| mypy strict | Type hints on all functions | Missing types |
| ruff lint/format | Code quality | Linting issues |
| eslint/prettier | TS code quality | Formatting issues |
| Directory Structure | Phase-based structure | Invalid layout |
| Tests Pass | Quality assurance | Failing tests |

## Common Issues & Fixes

### Branch naming error
```bash
# Error: "Branch name 'feature-auth' does not follow pattern"
# Fix:
git branch -m feature-auth phase-2-authentication
```

### Spec missing error
```bash
# Error: "Spec file not found"
# Fix:
.specify/scripts/bash/create-phr.sh --title "Authentication" --stage spec --feature fullstack-web
```

### Type checking error
```bash
# Error: "Function is missing a type annotation"
# Fix: Add type hint to function
def add_task(task: Task) -> None:  # Add type hints
    pass
```

### Code formatting error
```bash
# Error: "ruff format check failed"
# Fix: Auto-format code
ruff format src/
```

## Manual Validation

Check compliance without committing:
```bash
.specify/scripts/validation/validate-workflow.sh
```

## When to Use Infrastructure Agent

Invoke the infrastructure agent (via Task tool) for:
- Adding new validation rules
- Updating existing checks
- Debugging validation failures
- Improving error messages
- Updating constitution

## Next Steps

1. ✅ Test validation on current branch
2. ✅ Create a feature branch (phase-N-description)
3. ✅ Try committing to see hook in action
4. ✅ Let implementation agent work - it will auto-fix issues

## Full Documentation

See `.specify/INFRASTRUCTURE.md` for complete documentation including:
- Detailed validation rules
- Error message examples
- Adding new checks
- Troubleshooting guide

## Agent Configuration

See `.claude/agents/infrastructure.md` for:
- Agent responsibilities
- What agent does/doesn't do
- When to invoke the agent
- Success criteria

---

**Status**: ✅ Implemented and tested
**Version**: 1.0.0
**Date**: 2026-01-01
