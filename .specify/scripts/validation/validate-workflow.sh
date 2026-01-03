#!/bin/bash
# Infrastructure Validation Script
# Validates compliance with project constitution
# Runs as pre-commit hook and standalone validator

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track overall status
VALIDATION_PASSED=true

# Print section header
print_header() {
    echo ""
    echo "========================================"
    echo "$1"
    echo "========================================"
}

# Print success message
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Print error message
print_error() {
    echo -e "${RED}✗ $1${NC}"
    VALIDATION_PASSED=false
}

# Print warning message
print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Validation 1: Branch Naming Convention
validate_branch_name() {
    print_header "Validating Branch Naming"

    current_branch=$(git rev-parse --abbrev-ref HEAD)

    # Skip check if in detached HEAD or master/main
    if [[ "$current_branch" == "HEAD" ]] || [[ "$current_branch" == "master" ]] || [[ "$current_branch" == "main" ]]; then
        print_warning "Not on a feature branch, skipping branch naming check"
        return 0
    fi

    # Check if branch follows phase-N-description pattern
    if [[ ! "$current_branch" =~ ^phase-[0-9]+-.+$ ]]; then
        print_error "Branch name '$current_branch' does not follow phase-N-description pattern"
        echo "  Expected format: phase-<number>-<short-description>"
        echo "  Examples: phase-1-console-app, phase-2-fullstack-web"
        return 1
    fi

    print_success "Branch naming: $current_branch"
    return 0
}

# Validation 2: Feature Specification Exists
validate_spec_exists() {
    print_header "Validating Feature Specification"

    current_branch=$(git rev-parse --abbrev-ref HEAD)

    # Skip check if in detached HEAD or master/main
    if [[ "$current_branch" == "HEAD" ]] || [[ "$current_branch" == "master" ]] || [[ "$current_branch" == "main" ]]; then
        print_warning "Not on a feature branch, skipping spec check"
        return 0
    fi

    # Extract feature name from branch
    # phase-2-fullstack-web -> 002-fullstack-web
    if [[ "$current_branch" =~ ^phase-([0-9]+)-(.+)$ ]]; then
        phase_num="${BASH_REMATCH[1]}"
        feature_name="${BASH_REMATCH[2]}"

        # Pad phase number with zeros (1 -> 001, 2 -> 002)
        phase_padded=$(printf "%03d" "$phase_num")

        # Check for spec.md in specs/ with padded phase number format first
        spec_path="specs/${phase_padded}-${feature_name}/spec.md"

        if [[ ! -f "$spec_path" ]]; then
            # If not found, also check the non-padded format
            spec_path="specs/${feature_name}/spec.md"
            if [[ ! -f "$spec_path" ]]; then
                print_error "Spec file not found: $spec_path or specs/${phase_padded}-${feature_name}/spec.md"
                echo "  Branch: $current_branch"
                echo "  Expected format: specs/${phase_padded}-${feature_name}/spec.md or specs/${feature_name}/spec.md"
                echo "  Feature spec must exist before committing changes"
                return 1
            fi
        fi

        print_success "Feature specification exists: $spec_path"
        return 0
    fi

    print_warning "Cannot determine feature name from branch, skipping spec check"
    return 0
}

# Validation 3: PHR Created
validate_phr_exists() {
    print_header "Validating PHR Creation"

    current_branch=$(git rev-parse --abbrev-ref HEAD)

    # Skip check if in detached HEAD or master/main
    if [[ "$current_branch" == "HEAD" ]] || [[ "$current_branch" == "master" ]] || [[ "$current_branch" == "main" ]]; then
        print_warning "Not on a feature branch, skipping PHR check"
        return 0
    fi

    # Extract feature name from branch
    if [[ "$current_branch" =~ ^phase-([0-9]+)-(.+)$ ]]; then
        phase_num="${BASH_REMATCH[1]}"
        feature_name="${BASH_REMATCH[2]}"

        # Pad phase number with zeros (1 -> 001, 2 -> 002)
        phase_padded=$(printf "%03d" "$phase_num")

        # Check for PHR directory with padded phase number format first
        phr_dir="history/prompts/${phase_padded}-${feature_name}"

        if [[ ! -d "$phr_dir" ]]; then
            # If not found, also check the non-padded format
            phr_dir="history/prompts/${feature_name}"
            if [[ ! -d "$phr_dir" ]]; then
                print_error "PHR directory not found: $phr_dir or history/prompts/${phase_padded}-${feature_name}"
                echo "  Prompt History Record must be created for every feature"
                echo "  Run: .specify/scripts/bash/create-phr.sh --title '<title>' --stage spec --feature $feature_name"
                return 1
            fi
        fi

        # Check if there's at least one PHR file
        phr_count=$(find "$phr_dir" -name "*.prompt.md" 2>/dev/null | wc -l)

        if [[ "$phr_count" -eq 0 ]]; then
            print_warning "No PHR files found in $phr_dir"
            echo "  Consider creating a PHR for this feature"
        else
            print_success "PHR directory exists with $phr_count record(s)"
        fi

        return 0
    fi

    print_warning "Cannot determine feature name from branch, skipping PHR check"
    return 0
}

# Validation 4: Python Code Quality
validate_python_quality() {
    print_header "Validating Python Code Quality"

    python_files=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$' || true)

    if [[ -z "$python_files" ]]; then
        print_warning "No Python files in commit, skipping Python quality checks"
        return 0
    fi

    echo "Python files in commit: $python_files"

    # Check if mypy is available
    if command -v mypy &> /dev/null; then
        echo "Running mypy (strict mode)..."
        if mypy --strict $python_files 2>/dev/null; then
            print_success "mypy passed (strict mode)"
        else
            print_error "mypy failed. Run: mypy --strict <files>"
            return 1
        fi
    else
        print_warning "mypy not installed, skipping type checking"
    fi

    # Check if ruff is available
    if command -v ruff &> /dev/null; then
        echo "Running ruff format check..."
        if ruff format --check $python_files; then
            print_success "ruff format passed"
        else
            print_error "ruff format check failed. Run: ruff format <files>"
            echo "  To auto-format: ruff format <files>"
            return 1
        fi

        echo "Running ruff lint..."
        if ruff check $python_files; then
            print_success "ruff lint passed"
        else
            print_error "ruff lint failed. Run: ruff check <files>"
            echo "  To auto-fix: ruff check --fix <files>"
            return 1
        fi
    else
        print_warning "ruff not installed, skipping linting/formatting checks"
    fi

    return 0
}

# Validation 5: TypeScript/JavaScript Code Quality
validate_ts_quality() {
    print_header "Validating TypeScript/JavaScript Code Quality"

    ts_files=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(ts|tsx|js|jsx)$' || true)

    if [[ -z "$ts_files" ]]; then
        print_warning "No TypeScript/JavaScript files in commit, skipping TS quality checks"
        return 0
    fi

    echo "TypeScript/JavaScript files in commit: $ts_files"

    # Check if eslint is available
    if command -v eslint &> /dev/null || command -v npx &> /dev/null; then
        echo "Running eslint..."
        if npx eslint $ts_files || eslint $ts_files; then
            print_success "eslint passed"
        else
            print_error "eslint failed. Run: eslint <files>"
            return 1
        fi
    else
        print_warning "eslint not installed, skipping linting"
    fi

    # Check if prettier is available
    if command -v prettier &> /dev/null || command -v npx &> /dev/null; then
        echo "Running prettier check..."
        if npx prettier --check $ts_files || prettier --check $ts_files; then
            print_success "prettier format check passed"
        else
            print_error "prettier format check failed. Run: prettier --write <files>"
            return 1
        fi
    else
        print_warning "prettier not installed, skipping formatting check"
    fi

    return 0
}

# Validation 6: Tests Pass
validate_tests() {
    print_header "Validating Tests"

    # Detect if tests directory exists and run appropriate tests
    if [[ -d "tests" ]]; then
        if command -v pytest &> /dev/null; then
            echo "Running pytest..."
            if pytest tests/ -v --tb=short; then
                print_success "All tests passed"
            else
                print_error "Tests failed. Fix failing tests before committing"
                return 1
            fi
        elif command -v python &> /dev/null; then
            echo "Running tests with python -m pytest..."
            if python -m pytest tests/ -v --tb=short; then
                print_success "All tests passed"
            else
                print_error "Tests failed. Fix failing tests before committing"
                return 1
            fi
        else
            print_warning "pytest not found, skipping test execution"
        fi
    else
        print_warning "No tests directory found, skipping test validation"
    fi

    return 0
}

# Validation 7: Directory Structure
validate_directory_structure() {
    print_header "Validating Directory Structure"

    current_branch=$(git rev-parse --abbrev-ref HEAD)

    # Skip check if in detached HEAD or master/main
    if [[ "$current_branch" == "HEAD" ]] || [[ "$current_branch" == "master" ]] || [[ "$current_branch" == "main" ]]; then
        print_warning "Not on a feature branch, skipping structure check"
        return 0
    fi

    # Get changed files
    changed_files=$(git diff --cached --name-only --diff-filter=ACM)

    for file in $changed_files; do
        # Check if file is in apps/ directory and follows correct structure
        if [[ "$file" =~ ^apps/00[1-9]+- ]] || [[ "$file" =~ ^apps/phase-[1-9]+- ]]; then
            # File is in a phase directory, validate structure
            if [[ "$file" =~ ^apps/00[1-9]+- ]]; then
                # Check for padded format (001-, 002-, etc.)
                if [[ ! "$file" =~ ^apps/00[1-9]+-[^/]+/(src|tests|frontend|backend)/ ]]; then
                    print_error "Invalid directory structure: $file"
                    echo "  Files in apps/ must be organized as: apps/<phase-id>-<name>/{src,tests,frontend,backend}/"
                    return 1
                fi
            elif [[ "$file" =~ ^apps/phase-[1-9]+- ]]; then
                # Check for phase format (phase-1-, phase-2-, etc.)
                if [[ ! "$file" =~ ^apps/phase-[1-9]+-[^/]+/(src|tests|frontend|backend)/ ]]; then
                    print_error "Invalid directory structure: $file"
                    echo "  Files in apps/ must be organized as: apps/<phase-id>-<name>/{src,tests,frontend,backend}/"
                    return 1
                fi
            fi
        fi
    done

    print_success "Directory structure is valid"
    return 0
}

# Main execution
main() {
    echo -e "${GREEN}🏗️  Running Infrastructure Validation${NC}"
    echo ""

    # Run all validations
    validate_branch_name
    validate_spec_exists
    validate_phr_exists
    validate_python_quality
    validate_ts_quality
    validate_directory_structure

    # Only run tests if all other validations passed
    if [[ "$VALIDATION_PASSED" == true ]]; then
        validate_tests
    else
        print_header "Skipping Tests"
        print_warning "Tests not run due to failed validations above"
    fi

    # Print final result
    echo ""
    print_header "Validation Summary"

    if [[ "$VALIDATION_PASSED" == true ]]; then
        echo -e "${GREEN}✓ All validations passed!${NC}"
        echo ""
        exit 0
    else
        echo -e "${RED}✗ Validation failed. Please fix the issues above and try again.${NC}"
        echo ""
        echo "💡 Run this script manually to see detailed errors:"
        echo "   .specify/scripts/validation/validate-workflow.sh"
        echo ""
        exit 1
    fi
}

# Run main function
main
