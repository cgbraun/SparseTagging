# Claude Code Project Templates - Implementation Plan

## Project Overview

Create a reusable, defense-grade project initialization system for Python projects (libraries, CLIs, web services) that embeds organizational quality standards, development workflows, and security practices into every new project from day one.

**Target User**: Christopher (MRSL Director of Engineering) working in PyCharm with Claude Code
**Use Case**: Rapidly initialize new defense contractor projects with consistent quality gates
**Quality Level**: Defense-grade (SonarCloud, CVE scanning, type safety, comprehensive testing)

---

## Success Criteria

1. ✅ **Speed**: New project setup in <5 minutes (interactive script + template application)
2. ✅ **Consistency**: All projects share quality gates, tooling, documentation patterns
3. ✅ **Security**: Defense-grade quality from initialization (ITAR/DFARS compliant practices)
4. ✅ **Maintainability**: Templates version-controlled, evolve with lessons learned
5. ✅ **Flexibility**: Adapts to libraries, CLIs, web services without manual editing

---

## Architecture

```
claude-code-templates/
├── README.md                              # Usage guide
├── QUALITY_STANDARDS.md                   # Organizational standards (universal)
├── init_project.py                        # Interactive setup script
│
├── templates/
│   ├── python-library/                    # For PyPI packages
│   │   ├── CLAUDE.md.template
│   │   ├── settings.local.json.template
│   │   ├── .claude/
│   │   │   ├── hooks.json.template
│   │   │   ├── SUMMARY_SESSION.md
│   │   │   ├── KEY_PROMPTS_AND_PLANS.md
│   │   │   └── OTHER_SESSION_NOTES.md
│   │   ├── pyproject.toml.template
│   │   ├── mypy.ini.template
│   │   ├── .ruff.toml.template
│   │   ├── .pre-commit-config.yaml.template
│   │   ├── .github/
│   │   │   └── workflows/
│   │   │       └── ci.yml.template
│   │   ├── requirements.txt.template
│   │   ├── requirements-dev.txt.template
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   └── test_example.py.template
│   │   └── PROJECT_SETUP.md
│   │
│   ├── python-cli/                        # For command-line tools
│   │   └── [similar structure, CLI-specific variations]
│   │
│   └── python-service/                    # For FastAPI/Flask services
│       └── [similar structure, service-specific variations]
│
├── examples/
│   └── reference-sparsetag/               # Real-world example
│       ├── CLAUDE.md
│       └── settings.local.json
│
└── scripts/
    ├── validate_template.py               # Template validation
    └── upgrade_project.py                 # Update existing project to new standards
```

---

## Phase 1: Foundation & Core Templates

### 1.1 Project Structure Setup

**Action**: Create directory structure and core documentation

**Files to Create**:

1. **README.md** (root)
   - Purpose: Quick start guide for using templates
   - Sections: Installation, Usage, Template Types, Customization, Examples
   - Target: 5-minute onboarding time

2. **QUALITY_STANDARDS.md** (root)
   - Purpose: Organizational quality standards (defense-grade)
   - Content from SparseTag CLAUDE.md:
     - SonarCloud standards (Security Rating A, 85%+ coverage, complexity ≤15)
     - CVE scanning requirements (Dependabot, pip-audit)
     - Type safety requirements (mypy strict mode)
     - Testing standards (pytest, coverage thresholds)
     - CI/CD pipeline requirements
     - Documentation standards (markdownlint)
   - Rationale: Why each standard matters for defense contractors
   - Enforcement: How standards are checked (tools, CI gates)

3. **examples/reference-sparsetag/** (directory)
   - Copy actual SparseTag CLAUDE.md and settings.local.json
   - Purpose: Real-world reference implementation
   - Add REFERENCE_NOTES.md explaining key patterns

### 1.2 Interactive Setup Script

**File**: `init_project.py`

**Requirements**:
- Python 3.8+ (type hints, pathlib)
- No external dependencies (stdlib only for portability)
- Interactive prompts with validation
- Dry-run mode for preview
- Colorized output for clarity

**User Inputs** (collected interactively):

```python
# Required inputs
project_name: str           # e.g., "sparsetag"
project_type: str           # "library" | "cli" | "service"
project_description: str    # One-line summary

# Optional inputs (with smart defaults)
package_name: str           # Default: project_name.lower().replace("-", "_")
author_name: str            # Default: from git config
author_email: str           # Default: from git config
python_version: str         # Default: "3.8"
license: str                # Default: "MIT" (options: MIT, Apache-2.0, Proprietary)

# Feature flags (y/n, default based on type)
enable_sonarcloud: bool     # Default: True
enable_docker: bool         # Default: False for library, True for service
enable_github_actions: bool # Default: True
enable_pre_commit: bool     # Default: True

# Quality settings (for defense-grade, these are fixed but shown for transparency)
min_coverage: int           # Fixed: 85
max_complexity: int         # Fixed: 15
enable_mypy_strict: bool    # Fixed: True
enable_security_scan: bool  # Fixed: True (bandit)
```

**Script Flow**:

```
1. Display banner and purpose
2. Detect if running in existing directory or creating new
3. Collect user inputs with validation:
   - Project name: validate format (lowercase, hyphens ok)
   - Type: validate against available templates
   - Description: validate non-empty
   - Optional fields: provide defaults, allow override
4. Show configuration summary, ask for confirmation
5. Execute template application:
   - Copy template files
   - Replace placeholders in all .template files
   - Rename .template files (remove extension)
   - Initialize git repository
   - Create virtual environment
   - Install dependencies
   - Run initial quality checks (optional)
6. Display next steps guide
```

**Placeholder Syntax** (in template files):

```
{{PROJECT_NAME}}           → project_name from input
{{PROJECT_NAME_UPPER}}     → project_name.upper()
{{PACKAGE_NAME}}           → package_name from input
{{PROJECT_DESCRIPTION}}    → project_description from input
{{AUTHOR_NAME}}            → author_name from input
{{AUTHOR_EMAIL}}           → author_email from input
{{PYTHON_VERSION}}         → python_version from input
{{CURRENT_YEAR}}           → datetime.now().year
{{CURRENT_DATE}}           → datetime.now().strftime("%Y-%m-%d")
{{MIN_COVERAGE}}           → min_coverage (85 for defense)
{{MAX_COMPLEXITY}}         → max_complexity (15 for defense)
```

**Validation Rules**:
- Project name: `^[a-z][a-z0-9-]*$` (lowercase, starts with letter, hyphens ok)
- Package name: `^[a-z][a-z0-9_]*$` (valid Python identifier)
- Python version: `^3\.[8-9]|3\.1[0-9]$` (3.8+)
- Email: basic regex validation
- Description: non-empty, <120 chars

**Error Handling**:
- Detect existing project (warn before overwrite)
- Validate template existence
- Check write permissions
- Graceful failure with rollback on error
- Clear error messages with resolution steps

---

## Phase 2: Python Library Template

### 2.1 CLAUDE.md Template

**File**: `templates/python-library/CLAUDE.md.template`

**Structure** (based on SparseTag, generalized):

```markdown
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

{{PROJECT_DESCRIPTION}}

**Current Version:** v0.1.0 (initialized {{CURRENT_DATE}})

**Project Type**: Python Library
**Target**: PyPI package for {{PROJECT_DESCRIPTION}}

## Development Environment

### Virtual Environment Setup

```bash
# Create virtual environment (first time)
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Unix/macOS)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

### Required Dependencies

**Core** (requirements.txt):
- Add your runtime dependencies here

**Development** (requirements-dev.txt):
- pytest>=7.0.0
- pytest-cov>=4.0.0
- mypy>=1.0.0
- ruff>=0.1.0
- pre-commit>=3.0.0
- pip-audit>=2.0.0

## Code Quality & Security (Defense-Grade Standards)

This project follows defense-grade quality standards suitable for ITAR/DFARS compliance.
See [QUALITY_STANDARDS.md](../../QUALITY_STANDARDS.md) for full rationale.

### Quality Gates

**SonarCloud Integration** (when enabled):
- Zero security vulnerabilities (Security Rating: A)
- {{MIN_COVERAGE}}% coverage for new code ({{MIN_COVERAGE}}% overall)
- Cognitive complexity ≤{{MAX_COMPLEXITY}} per function
- Max 3% code duplication

**Pre-commit Checks**:
- **Ruff**: Linting and formatting (replaces flake8, black, isort)
- **Mypy**: Type checking (strict mode enabled)
- **Pytest**: Run test suite with coverage
- **Markdownlint**: Documentation quality

**Security Scanning**:
- **Dependabot**: Automated CVE monitoring for dependencies
- **Bandit**: Python security linting
- **pip-audit**: CVE scanning for installed packages

### Running Quality Checks Locally

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Type check
mypy src/{{PACKAGE_NAME}}

# Run tests with coverage
pytest tests/ --cov=src/{{PACKAGE_NAME}} --cov-report=html

# Security scan
bandit -r src/{{PACKAGE_NAME}}
pip-audit

# All checks (via pre-commit)
pre-commit run --all-files
```

### CI/CD Pipeline

**Workflow**: `.github/workflows/ci.yml`

The CI pipeline enforces quality gates and provides deployment automation:

**Pipeline Stages**:
1. **Code Quality**: Ruff, mypy, pylint
2. **Security**: Bandit, pip-audit
3. **Testing**: pytest with coverage reporting
4. **Documentation**: Markdownlint, link checking
5. **SonarCloud**: Code quality analysis (when enabled)
6. **Package Build**: Verify package builds successfully

**Quality Gates** (must pass for merge):
- ✅ All tests pass
- ✅ Coverage ≥{{MIN_COVERAGE}}%
- ✅ No type errors (mypy)
- ✅ No security issues (Bandit)
- ✅ No high/critical CVEs
- ✅ SonarCloud Quality Gate passed (when enabled)

## Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src/{{PACKAGE_NAME}}

# Generate HTML coverage report
pytest tests/ --cov=src/{{PACKAGE_NAME}} --cov-report=html
# Open htmlcov/index.html in browser

# Run specific test file
pytest tests/test_example.py

# Run with verbose output
pytest tests/ -v

# Run with print statements visible
pytest tests/ -s
```

**Test Organization**:
```
tests/
├── __init__.py
├── test_core.py              # Core functionality tests
├── test_edge_cases.py        # Boundary conditions
├── test_error_handling.py    # Exception scenarios
└── test_integration.py       # End-to-end workflows
```

**Coverage Requirements**:
- Overall: ≥{{MIN_COVERAGE}}%
- New code: ≥90%
- Critical modules: 100% (exceptions, validation)

## Type Checking

This project uses mypy in strict mode for maximum type safety:

```bash
# Check all source files
mypy src/{{PACKAGE_NAME}}

# Check specific module
mypy src/{{PACKAGE_NAME}}/core.py

# Check with more detailed output
mypy src/{{PACKAGE_NAME}} --show-error-codes
```

**Configuration**: `mypy.ini`
- Strict mode enabled (`strict = True`)
- All functions must have type hints
- No implicit Optional allowed
- Strict equality checks enforced

**Type Patterns**:
```python
# Use TYPE_CHECKING for circular import avoidance
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .other_module import OtherClass

# Explicit Optional for nullable values
from typing import Optional
def function(param: Optional[str] = None) -> int:
    pass

# Type aliases for complex types
from typing import Dict, List, Union
ConfigDict = Dict[str, Union[str, int, bool]]
```

## Code Architecture

### Project Structure

```
{{PROJECT_NAME}}/
├── src/
│   └── {{PACKAGE_NAME}}/
│       ├── __init__.py          # Package initialization
│       ├── core.py              # Core functionality
│       ├── exceptions.py        # Custom exceptions
│       └── utils.py             # Utility functions
├── tests/
│   ├── __init__.py
│   └── test_*.py                # Test modules
├── docs/                        # Documentation (if needed)
├── .github/
│   └── workflows/
│       └── ci.yml               # CI/CD pipeline
├── CLAUDE.md                    # This file
├── README.md                    # Project documentation
├── pyproject.toml               # Project metadata
├── mypy.ini                     # Type checking config
├── .ruff.toml                   # Linting config
├── .pre-commit-config.yaml      # Pre-commit hooks
├── requirements.txt             # Runtime dependencies
└── requirements-dev.txt         # Development dependencies
```

### Custom Exceptions

Use domain-specific exceptions from `exceptions.py`:

```python
# Exception hierarchy
{{PACKAGE_NAME}}Error (Exception)           # Base exception
├── ValidationError (ValueError)            # Input validation failures
├── ConfigurationError (ValueError)         # Configuration issues
└── ProcessingError (RuntimeError)          # Runtime processing errors
```

**Usage**:
```python
from {{PACKAGE_NAME}}.exceptions import ValidationError

def validate_input(value):
    if not isinstance(value, int):
        raise ValidationError(f"Expected int, got {type(value)}")
```

## Code Patterns

### Module Imports

```python
# Standard library imports (group 1)
import os
import sys
from pathlib import Path

# Third-party imports (group 2)
import numpy as np
import requests

# Local application imports (group 3)
from {{PACKAGE_NAME}}.core import MainClass
from {{PACKAGE_NAME}}.exceptions import ValidationError
```

### Error Handling

```python
# Specific exceptions, clear messages
try:
    result = process_data(input_data)
except ValidationError as e:
    logger.error(f"Input validation failed: {e}")
    raise
except ProcessingError as e:
    logger.error(f"Processing failed: {e}")
    # Handle or re-raise with context
    raise RuntimeError(f"Failed to process data: {e}") from e
```

### Logging

```python
import logging

logger = logging.getLogger(__name__)

# Use appropriate levels
logger.debug("Detailed diagnostic info")
logger.info("Normal operation info")
logger.warning("Something unexpected but handled")
logger.error("Error occurred, operation failed")
logger.critical("Critical failure, cannot continue")
```

## Important Constraints

1. **Type Safety**: All functions must have type hints (mypy strict mode)
2. **Test Coverage**: Maintain ≥{{MIN_COVERAGE}}% coverage, ≥90% for new code
3. **Complexity**: Functions must have complexity ≤{{MAX_COMPLEXITY}}
4. **Security**: Zero high/critical vulnerabilities allowed
5. **Documentation**: All public APIs must have docstrings
6. **Dependencies**: Keep minimal, audit for CVEs regularly
7. **Backward Compatibility**: Follow semantic versioning (semver)

## Future Development

See CHANGELOG.md for version roadmap and planned features.

## Getting Help

- **Documentation**: See README.md for user guide
- **Issues**: Report bugs/features on GitHub Issues
- **Standards**: See QUALITY_STANDARDS.md for detailed requirements
- **Contributing**: See CONTRIBUTING.md (when created)

---

**Last Updated**: {{CURRENT_DATE}}
**Template Version**: 1.0.0
**Quality Level**: Defense-Grade
```

### 2.2 Settings Template

**File**: `templates/python-library/settings.local.json.template`

**Philosophy**:
- ✅ **Permissive for reads**: Full read access, exploration, inspection
- ❌ **Restrictive for writes**: No git push, no permanent modifications without explicit approval
- ✅ **Quality tools enabled**: pytest, mypy, ruff, pre-commit
- ✅ **Safe operations**: git status/diff/log, but not commit/push by default
- ✅ **Session logging**: Can append to .claude/ for documentation

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep",
      "WebFetch",
      "WebSearch",

      "Bash(ls)",
      "Bash(ls:*)",
      "Bash(cat)",
      "Bash(cat:*)",
      "Bash(grep)",
      "Bash(grep:*)",
      "Bash(find)",
      "Bash(find:*)",
      "Bash(head)",
      "Bash(head:*)",
      "Bash(tail)",
      "Bash(tail:*)",
      "Bash(wc)",
      "Bash(wc:*)",
      "Bash(diff)",
      "Bash(diff:*)",
      "Bash(basename)",
      "Bash(basename:*)",
      "Bash(dirname)",
      "Bash(dirname:*)",
      "Bash(pwd)",
      "Bash(echo)",
      "Bash(echo:*)",

      "Bash(which)",
      "Bash(which:*)",
      "Bash(where)",
      "Bash(where:*)",

      "Bash(git status)",
      "Bash(git status:*)",
      "Bash(git diff)",
      "Bash(git diff:*)",
      "Bash(git log)",
      "Bash(git log:*)",
      "Bash(git show)",
      "Bash(git show:*)",
      "Bash(git branch)",
      "Bash(git branch:*)",
      "Bash(git rev-parse)",
      "Bash(git rev-parse:*)",

      "Bash(python)",
      "Bash(python:*)",
      "Bash(python3)",
      "Bash(python3:*)",
      "Bash(python -m pytest)",
      "Bash(python -m pytest:*)",
      "Bash(pytest)",
      "Bash(pytest:*)",
      "Bash(python -m pip list)",
      "Bash(python -m pip show)",
      "Bash(python -m pip show:*)",
      "Bash(pip list)",
      "Bash(pip show)",
      "Bash(pip show:*)",

      "Bash(mypy)",
      "Bash(mypy:*)",
      "Bash(ruff check)",
      "Bash(ruff check:*)",
      "Bash(ruff format)",
      "Bash(ruff format:*)",
      "Bash(ruff)",
      "Bash(ruff:*)",
      "Bash(bandit)",
      "Bash(bandit:*)",
      "Bash(pip-audit)",
      "Bash(pip-audit:*)",

      "Bash(pre-commit run)",
      "Bash(pre-commit run:*)",
      "Bash(pre-commit install)",

      "Bash(cat >> .claude/SUMMARY_SESSION.md << 'EOF')",
      "Bash(cat >> .claude/KEY_PROMPTS_AND_PLANS.md << 'EOF')",
      "Bash(cat >> .claude/OTHER_SESSION_NOTES.md << 'EOF')",

      "Bash(if [ -f \".venv/Scripts/activate\" ])",
      "Bash(then echo \"Windows venv\")",
      "Bash(elif [ -f \".venv/bin/activate\" ])",
      "Bash(then echo \"Unix venv\")",
      "Bash(fi)",

      "Bash(npx markdownlint-cli2)",
      "Bash(npx markdownlint-cli2:*)",
      "Bash(npx markdown-link-check)",
      "Bash(npx markdown-link-check:*)",

      "WebFetch(domain:github.com)",
      "WebFetch(domain:pypi.org)",
      "WebFetch(domain:docs.python.org)",
      "WebFetch(domain:sonarcloud.io)",
      "WebFetch(domain:docs.sonarsource.com)"
    ],

    "deny": [
      "Bash(git push)",
      "Bash(git push:*)",
      "Bash(git commit)",
      "Bash(git commit:*)",
      "Bash(git add)",
      "Bash(git add:*)",
      "Bash(rm)",
      "Bash(rm:*)",
      "Bash(pip install)",
      "Bash(pip install:*)",
      "Bash(pip uninstall)",
      "Bash(pip uninstall:*)"
    ]
  }
}
```

**Rationale**:
- Git operations: Can inspect (diff, log, status) but cannot modify (add, commit, push)
- Package management: Can list/show but cannot install (prevent dependency changes)
- File system: Can read but explicit rm denial for safety
- Quality tools: Full access for checking/formatting
- Web access: Limited to trusted domains (GitHub, PyPI, Python docs, SonarCloud)

### 2.3 Hooks Configuration

**File**: `templates/python-library/.claude/hooks.json.template`

**Purpose**: Automated quality gates after file edits

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python -m pytest tests/ --quiet --tb=short || true",
            "description": "Run tests after code edits (graceful failure)"
          }
        ]
      }
    ]
  }
}
```

**Notes**:
- `|| true` allows workflow to continue even if tests fail
- User can review failures and decide next action
- Can be extended with:
  - Type checking: `mypy src/{{PACKAGE_NAME}} || true`
  - Linting: `ruff check . || true`
  - Format checking: `ruff format --check . || true`

### 2.4 Configuration Files

**File**: `templates/python-library/mypy.ini.template`

```ini
[mypy]
python_version = {{PYTHON_VERSION}}
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
check_untyped_defs = True
no_implicit_optional = True
warn_redundant_casts = True
warn_unused_ignores = True
strict_equality = True
strict = True

# Allow untyped calls for certain libraries
[mypy-pytest.*]
ignore_missing_imports = True

[mypy-setuptools.*]
ignore_missing_imports = True
```

**File**: `templates/python-library/.ruff.toml.template`

```toml
# Ruff configuration for {{PROJECT_NAME}}

line-length = 100
target-version = "py{{PYTHON_VERSION|replace('.', '')}}"

[lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "N",    # pep8-naming
    "UP",   # pyupgrade
    "B",    # flake8-bugbear
    "C4",   # flake8-comprehensions
    "SIM",  # flake8-simplify
    "RUF",  # Ruff-specific rules
]

ignore = [
    "E501",  # Line too long (handled by formatter)
]

[lint.per-file-ignores]
"tests/*" = ["S101"]  # Allow assert in tests

[format]
quote-style = "double"
indent-style = "space"
```

**File**: `templates/python-library/.pre-commit-config.yaml.template`

```yaml
# Pre-commit hooks for {{PROJECT_NAME}}

repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
        args: [--strict]

  - repo: https://github.com/igorshubovych/markdownlint-cli
    rev: v0.39.0
    hooks:
      - id: markdownlint
        args: [--fix]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: [--maxkb=500]
```

**File**: `templates/python-library/pyproject.toml.template`

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{{PROJECT_NAME}}"
version = "0.1.0"
description = "{{PROJECT_DESCRIPTION}}"
authors = [
    {name = "{{AUTHOR_NAME}}", email = "{{AUTHOR_EMAIL}}"}
]
license = {text = "{{LICENSE}}"}
readme = "README.md"
requires-python = ">=3.{{PYTHON_VERSION|split('.')[1]}}"
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.{{PYTHON_VERSION|split('.')[1]}}",
]

[project.urls]
Homepage = "https://github.com/{{AUTHOR_NAME}}/{{PROJECT_NAME}}"
Issues = "https://github.com/{{AUTHOR_NAME}}/{{PROJECT_NAME}}/issues"

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]
```

### 2.5 CI/CD Template

**File**: `templates/python-library/.github/workflows/ci.yml.template`

**Note**: This is a comprehensive template based on SparseTag's CI, adapted for generic use

```yaml
name: CI Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  quality:
    name: Code Quality
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '{{PYTHON_VERSION}}'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Lint with Ruff
        run: |
          ruff check . --output-format=github
          echo "RUFF_EXIT_CODE=$?" >> $GITHUB_ENV

      - name: Type check with mypy
        run: |
          mypy src/{{PACKAGE_NAME}}
          echo "MYPY_EXIT_CODE=$?" >> $GITHUB_ENV

      - name: Security scan with Bandit
        run: |
          bandit -r src/{{PACKAGE_NAME}} -f json -o bandit-report.json || true
          bandit -r src/{{PACKAGE_NAME}}
          echo "BANDIT_EXIT_CODE=$?" >> $GITHUB_ENV

      - name: CVE scan with pip-audit
        run: |
          pip-audit --desc --format json --output pip-audit-report.json || true
          pip-audit --desc
          echo "PIP_AUDIT_EXIT_CODE=$?" >> $GITHUB_ENV

  test:
    name: Test Suite
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '{{PYTHON_VERSION}}'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run tests with coverage
        run: |
          pytest tests/ \
            --cov=src/{{PACKAGE_NAME}} \
            --cov-report=xml \
            --cov-report=term \
            --junit-xml=pytest-report.xml

      - name: Check coverage threshold
        run: |
          coverage report --fail-under={{MIN_COVERAGE}}

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        if: always()
        with:
          file: ./coverage.xml
          fail_ci_if_error: false

  sonarcloud:
    name: SonarCloud Analysis
    runs-on: ubuntu-latest
    needs: [quality, test]
    if: github.event_name == 'pull_request' || github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: SonarCloud Scan
        uses: SonarSource/sonarcloud-github-action@master
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
        with:
          args: >
            -Dsonar.projectKey={{AUTHOR_NAME}}_{{PROJECT_NAME}}
            -Dsonar.organization={{AUTHOR_NAME}}
            -Dsonar.python.coverage.reportPaths=coverage.xml
            -Dsonar.python.version={{PYTHON_VERSION}}

  doc-validation:
    name: Documentation Validation
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Markdownlint
        run: |
          npx markdownlint-cli2 "**/*.md" "#node_modules" "#.venv"

      - name: Markdown link check
        run: |
          npx markdown-link-check README.md --config .markdown-link-check.json || true
```

### 2.6 Test Template

**File**: `templates/python-library/tests/test_example.py.template`

```python
"""
Example test module for {{PROJECT_NAME}}.

This demonstrates the testing patterns and structure for this project.
"""

import pytest
from {{PACKAGE_NAME}}.core import example_function
from {{PACKAGE_NAME}}.exceptions import ValidationError


class TestExampleFunction:
    """Test suite for example_function."""

    def test_basic_functionality(self):
        """Test basic functionality works as expected."""
        result = example_function("test input")
        assert result is not None
        assert isinstance(result, str)

    def test_with_valid_input(self):
        """Test with various valid inputs."""
        test_cases = [
            ("input1", "expected1"),
            ("input2", "expected2"),
        ]
        for input_val, expected in test_cases:
            result = example_function(input_val)
            assert result == expected

    def test_with_invalid_input(self):
        """Test that invalid input raises appropriate exception."""
        with pytest.raises(ValidationError, match="Invalid input"):
            example_function(None)

    def test_edge_case_empty_string(self):
        """Test edge case with empty string."""
        result = example_function("")
        assert result == ""

    def test_edge_case_long_string(self):
        """Test with very long input."""
        long_input = "x" * 10000
        result = example_function(long_input)
        assert len(result) == len(long_input)


class TestIntegration:
    """Integration tests for complete workflows."""

    def test_end_to_end_workflow(self):
        """Test a complete end-to-end workflow."""
        # Setup
        input_data = "test"

        # Execute
        result = example_function(input_data)

        # Verify
        assert result is not None
        # Add more assertions as needed


# Fixtures
@pytest.fixture
def sample_data():
    """Provide sample data for tests."""
    return {
        "key1": "value1",
        "key2": "value2",
    }


@pytest.fixture
def temp_config(tmp_path):
    """Provide temporary configuration file."""
    config_file = tmp_path / "config.json"
    config_file.write_text('{"setting": "value"}')
    return config_file
```

---

## Phase 3: Project Type Variants

### 3.1 Python CLI Template

**Differences from Library**:
- Add `src/{{PACKAGE_NAME}}/cli.py` with argparse/click setup
- Add `pyproject.toml` entry points for CLI commands
- Add `tests/test_cli.py` for CLI testing
- Add example CLI usage to README
- CI/CD includes CLI smoke tests

**Additional Files**:
- `src/{{PACKAGE_NAME}}/cli.py.template` - Main CLI entry point
- CLI testing guide in CLAUDE.md

### 3.2 Python Service Template

**Differences from Library**:
- Add FastAPI/Flask skeleton
- Add `docker-compose.yml` for local development
- Add health check endpoints
- Add service-specific CI/CD (container build, push)
- Add API documentation generation
- Add load testing configuration

**Additional Files**:
- `src/{{PACKAGE_NAME}}/main.py.template` - FastAPI app
- `src/{{PACKAGE_NAME}}/routers/` - API route modules
- `Dockerfile.template` - Container definition
- `docker-compose.yml.template` - Local dev environment

---

## Phase 4: Validation & Documentation

### 4.1 Template Validation Script

**File**: `scripts/validate_template.py`

**Purpose**: Ensure templates are well-formed before use

**Checks**:
1. All placeholders are valid (match defined list)
2. Template files are valid for their type (JSON, TOML, YAML, Python)
3. Required files exist for each template type
4. No hardcoded values that should be placeholders
5. References between files are consistent

**Usage**:
```bash
python scripts/validate_template.py templates/python-library
```

### 4.2 README Documentation

**File**: `README.md` (root)

**Sections**:
1. **Quick Start**: 5-minute guide to first project
2. **Installation**: How to install/use templates
3. **Template Types**: Library vs CLI vs Service
4. **Customization**: How to modify templates
5. **Quality Standards**: Link to QUALITY_STANDARDS.md
6. **Examples**: Link to examples/ directory
7. **Contributing**: How to improve templates
8. **Troubleshooting**: Common issues and solutions

### 4.3 Project Setup Guide

**File**: `templates/python-library/PROJECT_SETUP.md`

**Purpose**: Next steps after template initialization

**Content**:
```markdown
# Project Setup Guide - {{PROJECT_NAME}}

This guide walks through completing your project setup after template initialization.

## Initial Setup (First Time)

### 1. Verify Environment

```bash
# Check Python version
python --version  # Should be {{PYTHON_VERSION}}+

# Verify virtual environment
which python      # Should point to .venv/

# Check dependencies installed
pip list          # Should show pytest, mypy, ruff, etc.
```

### 2. Configure Git

```bash
# Set up pre-commit hooks
pre-commit install

# Create initial commit
git add .
git commit -m "chore: Initialize project from template"

# (Optional) Connect to GitHub
git remote add origin https://github.com/{{AUTHOR_NAME}}/{{PROJECT_NAME}}.git
git push -u origin main
```

### 3. Configure SonarCloud (Optional)

1. Go to https://sonarcloud.io
2. Import your GitHub repository
3. Copy the project key
4. Add `SONAR_TOKEN` to GitHub Secrets
5. Update organization in ci.yml

### 4. Write Your First Code

```bash
# Create core module
touch src/{{PACKAGE_NAME}}/core.py

# Create corresponding test
touch tests/test_core.py

# Run tests
pytest tests/
```

## Development Workflow

### Daily Workflow

1. **Pull latest changes**
   ```bash
   git pull origin main
   ```

2. **Create feature branch**
   ```bash
   git checkout -b feature/my-feature
   ```

3. **Write code + tests**
   - Edit files in `src/{{PACKAGE_NAME}}/`
   - Add tests in `tests/`

4. **Run quality checks**
   ```bash
   pre-commit run --all-files
   pytest tests/ --cov
   ```

5. **Commit changes**
   ```bash
   git add .
   git commit -m "feat: Add new feature"
   ```

6. **Push and create PR**
   ```bash
   git push origin feature/my-feature
   # Create PR on GitHub
   ```

### Adding Dependencies

```bash
# Add runtime dependency
echo "requests>=2.28.0" >> requirements.txt
pip install -r requirements.txt

# Add dev dependency
echo "black>=23.0.0" >> requirements-dev.txt
pip install -r requirements-dev.txt

# Update lock file (if using)
pip freeze > requirements-lock.txt
```

## Next Steps

- [ ] Write core functionality in `src/{{PACKAGE_NAME}}/`
- [ ] Add comprehensive tests in `tests/`
- [ ] Update README.md with usage examples
- [ ] Configure SonarCloud (if using)
- [ ] Set up Dependabot for security updates
- [ ] Add CHANGELOG.md for version tracking
- [ ] Configure PyPI publishing (for libraries)

### Getting Help

- **Template Issues**: See main templates repository
- **Project Issues**: Open issue on GitHub
- **Quality Standards**: See QUALITY_STANDARDS.md
- **CLAUDE.md**: Project-specific Claude Code guidance
```

---

## Phase 5: Testing & Refinement

### 5.1 Manual Testing Checklist

**Test Case 1: New Python Library Project**
```bash
# Execute
python init_project.py

# Inputs
Project name: test-library
Type: library
Description: Test library for validation
[Accept all defaults]

# Verify
- [ ] Directory created: test-library/
- [ ] All files present and valid
- [ ] Placeholders replaced correctly
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Tests run successfully
- [ ] Quality checks pass (ruff, mypy)
- [ ] Git repository initialized
```

**Test Case 2: Existing Project Enhancement**
```bash
# Setup existing project
mkdir existing-project
cd existing-project
git init
touch README.md

# Execute
python ../init_project.py --enhance

# Verify
- [ ] Existing files not overwritten
- [ ] New quality files added
- [ ] Settings configured correctly
- [ ] No conflicts with existing structure
```

**Test Case 3: Invalid Inputs**
```bash
# Test validation
Project name: InvalidName123  # Should reject (uppercase)
Project name: -invalid        # Should reject (starts with -)
Project name: valid-name      # Should accept

Email: invalid-email          # Should reject
Email: test@example.com       # Should accept
```

### 5.2 Automated Testing

**File**: `tests/test_init_project.py`

**Test Coverage**:
- Placeholder replacement logic
- Input validation (name, email, version formats)
- File copying and renaming
- Template selection based on project type
- Error handling and rollback
- Git initialization
- Virtual environment creation

---

## Phase 6: Documentation & Polish

### 6.1 QUALITY_STANDARDS.md

**File**: `QUALITY_STANDARDS.md` (root)

**Purpose**: Central reference for all organizational quality standards

**Sections**:
1. **Overview**: Why defense-grade standards matter
2. **Security**: CVE scanning, dependency auditing, vulnerability management
3. **Type Safety**: Why mypy strict mode, benefits for defense projects
4. **Testing**: Coverage requirements, test types, critical path testing
5. **Code Quality**: Complexity limits, duplication, maintainability
6. **Documentation**: Standards for code comments, API docs, user guides
7. **CI/CD**: Pipeline requirements, quality gates, deployment
8. **Compliance**: ITAR/DFARS considerations for defense contractors
9. **Tool Configurations**: Reference configs for each tool
10. **Enforcement**: How standards are checked and enforced

### 6.2 Example Reference Projects

**Directory**: `examples/reference-sparsetag/`

**Files**:
- Copy of actual SparseTag CLAUDE.md
- Copy of actual SparseTag settings.local.json
- `REFERENCE_NOTES.md` explaining key patterns:
  - Why certain sections are structured that way
  - How quality standards evolved
  - What worked well vs what didn't
  - Lessons learned

---

## Implementation Order

### Sprint 1: Foundation (Days 1-2)
1. Create directory structure
2. Write QUALITY_STANDARDS.md
3. Create basic README.md
4. Set up examples/reference-sparsetag/

### Sprint 2: Python Library Template (Days 3-5)
1. CLAUDE.md.template (comprehensive)
2. settings.local.json.template
3. hooks.json.template
4. Configuration files (mypy.ini, .ruff.toml, etc.)
5. CI/CD workflow template
6. Test template
7. PROJECT_SETUP.md

### Sprint 3: Interactive Script (Days 6-7)
1. Input collection and validation
2. Placeholder replacement logic
3. File operations (copy, rename)
4. Git and venv initialization
5. Error handling and rollback
6. User output and next steps

### Sprint 4: Testing & Refinement (Day 8)
1. Manual testing with real projects
2. Fix issues found
3. Improve error messages
4. Polish user experience

### Sprint 5: Documentation & Variants (Days 9-10)
1. Complete README.md
2. Template validation script
3. Python CLI template (variant)
4. Python service template (variant)

---

## Key Success Metrics

1. **Setup Time**: <5 minutes from init to first test run
2. **Quality Gates**: 100% of templates pass all quality checks
3. **Usability**: Zero ambiguous prompts in interactive script
4. **Maintainability**: Templates follow DRY principles, easy to update
5. **Adoption**: Christopher uses for next 3 projects without modification

---

## Technical Specifications

### Placeholder Replacement Engine

**Implementation**:
```python
def replace_placeholders(content: str, context: Dict[str, str]) -> str:
    """Replace all {{PLACEHOLDER}} with values from context."""
    import re

    # Support filters: {{PLACEHOLDER|filter}}
    pattern = r'\{\{([A-Z_]+)(?:\|([a-z_]+))?\}\}'

    def replacer(match):
        key = match.group(1)
        filter_name = match.group(2)

        if key not in context:
            raise ValueError(f"Unknown placeholder: {key}")

        value = context[key]

        # Apply filter if specified
        if filter_name:
            value = apply_filter(value, filter_name)

        return value

    return re.sub(pattern, replacer, content)

def apply_filter(value: str, filter_name: str) -> str:
    """Apply transformation filter to value."""
    filters = {
        'upper': str.upper,
        'lower': str.lower,
        'replace': lambda v: v.replace('.', ''),  # e.g., "3.8" -> "38"
        'split': lambda v: v.split('.'),
    }
    return filters[filter_name](value)
```

### File Operations

**Safe Copy with Rollback**:
```python
class TemplateInstaller:
    def __init__(self, target_dir: Path):
        self.target_dir = target_dir
        self.operations = []  # Track for rollback

    def copy_template(self, src: Path, dst: Path, context: Dict[str, str]):
        """Copy file and replace placeholders, track for rollback."""
        try:
            # Read template
            content = src.read_text()

            # Replace placeholders
            processed = replace_placeholders(content, context)

            # Write to destination
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(processed)

            # Track operation
            self.operations.append(('create', dst))

        except Exception as e:
            self.rollback()
            raise RuntimeError(f"Failed to copy {src}: {e}")

    def rollback(self):
        """Rollback all operations in reverse order."""
        for op_type, path in reversed(self.operations):
            if op_type == 'create' and path.exists():
                path.unlink()
```

### Input Validation

**Validation Functions**:
```python
import re
from typing import Optional

def validate_project_name(name: str) -> Optional[str]:
    """Validate project name format, return error message or None."""
    if not re.match(r'^[a-z][a-z0-9-]*$', name):
        return "Project name must start with lowercase letter and contain only lowercase letters, numbers, and hyphens"
    if len(name) < 3:
        return "Project name must be at least 3 characters"
    if len(name) > 50:
        return "Project name must be at most 50 characters"
    return None

def validate_email(email: str) -> Optional[str]:
    """Validate email format."""
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return "Invalid email format"
    return None

def validate_python_version(version: str) -> Optional[str]:
    """Validate Python version format."""
    if not re.match(r'^3\.[8-9]|3\.1[0-9]$', version):
        return "Python version must be 3.8 or higher (format: 3.8, 3.9, 3.10, etc.)"
    return None
```

---

## Prompts for Claude Code

When implementing this plan in Claude Code, use these prompts at each phase:

### Phase 1 Prompt:
```
I want to implement a Claude Code project templates system for defense-grade Python projects.

Start by creating the foundation:
1. Directory structure: templates/, examples/, scripts/
2. QUALITY_STANDARDS.md with defense-grade requirements from the SparseTag reference
3. Basic README.md with quick start guide
4. Copy SparseTag CLAUDE.md and settings.local.json to examples/reference-sparsetag/

Use the plan in CLAUDE_CODE_TEMPLATES_IMPLEMENTATION_PLAN.md as the detailed specification.
Focus on Phase 1 only. Ask for confirmation before proceeding to Phase 2.
```

### Phase 2 Prompt:
```
Now implement Phase 2: Python Library Template

Create all template files in templates/python-library/:
- CLAUDE.md.template (comprehensive, based on SparseTag but generalized)
- settings.local.json.template (defense-grade permissions)
- hooks.json.template (post-edit test running)
- Configuration files: mypy.ini, .ruff.toml, .pre-commit-config.yaml, pyproject.toml
- CI/CD: .github/workflows/ci.yml.template
- Test template: tests/test_example.py.template
- PROJECT_SETUP.md

Use placeholder syntax: {{PROJECT_NAME}}, {{PACKAGE_NAME}}, etc.
Follow specifications in the plan exactly.
```

### Phase 3 Prompt:
```
Implement Phase 3: Interactive Setup Script (init_project.py)

Requirements:
- Python 3.8+ stdlib only (no external deps)
- Interactive prompts with validation
- Dry-run mode for preview
- Placeholder replacement engine
- Safe file operations with rollback
- Clear user output and next steps

Test with: python init_project.py
Expected: Asks questions, creates project, runs successfully
```

---

## Appendix: Reference Material

### A. SparseTag CLAUDE.md Key Patterns

**Pattern 1: Project Overview**
- Current version visible
- Key features listed
- Links to external services (SonarCloud)

**Pattern 2: Quality Gates**
- Specific thresholds (85% coverage, complexity ≤15)
- Tool configurations listed
- How to run each check

**Pattern 3: Architecture Documentation**
- Data model explanation
- Key components with line references
- Critical implementation details
- Code patterns with examples

**Pattern 4: Decision Rationale**
- "Why we did it this way" sections
- Trade-offs explained
- When to reconsider decisions

### B. Permissions Philosophy

**Read Operations** (Permissive):
- All file reading (cat, grep, find, diff)
- Repository inspection (git status, log, diff)
- Web access to trusted domains
- Tool inspection (pip list, which)

**Write Operations** (Restrictive):
- No git push/commit/add (prevent accidental changes)
- No pip install (prevent dependency drift)
- No rm/delete (prevent data loss)
- Session logging allowed (.claude/ directory)

**Quality Tools** (Permissive):
- Full access to pytest, mypy, ruff, bandit
- Pre-commit hooks allowed
- Documentation tools (markdownlint)

### C. CI/CD Best Practices

**From SparseTag Experience**:
1. Exit code capture for quality gates (don't just run, check results)
2. Graceful degradation (optional services shouldn't block pipeline)
3. Path-based execution (skip unnecessary jobs for doc-only changes)
4. Service health checks (verify external dependencies before using)
5. Centralized version management (single source of truth)
6. SARIF scanning for accurate vulnerability counts
7. Comprehensive reporting (save scan results for review)

---

## Final Notes for Claude Code

**Key Points for Implementation**:

1. **Start Small**: Get Phase 1 working before Phase 2
2. **Test Frequently**: Run init_project.py after each change
3. **Use Real Data**: Test with actual project names, not "test123"
4. **Validate Output**: Check that placeholders are replaced correctly
5. **Error Handling**: Test with invalid inputs, ensure good error messages
6. **Documentation**: Update README as you implement features

**Expected Challenges**:

1. **Placeholder Filters**: The {{PLACEHOLDER|filter}} syntax needs careful parsing
2. **File Permissions**: Windows vs Unix path handling
3. **Git Operations**: Ensure git is installed and configured
4. **Virtual Environment**: Handle both venv and virtualenv
5. **Template Validation**: Ensure all templates are well-formed before use

**Success Indicators**:

- ✅ Can create new project in <5 minutes
- ✅ All placeholders replaced correctly
- ✅ Tests run successfully after init
- ✅ Quality checks pass (ruff, mypy)
- ✅ No manual file editing needed
- ✅ Clear error messages for failures
- ✅ Documentation is complete and accurate

**When Done**:

1. Test with 2-3 different project names
2. Verify all file types (TOML, YAML, JSON, Python)
3. Check that CI/CD would work (if pushed to GitHub)
4. Validate against QUALITY_STANDARDS.md
5. Create example project: "test-calculator"
6. Document any deviations from plan with rationale

---

**Plan Version**: 1.0
**Created**: 2026-01-23
**Author**: Claude (based on Christopher's SparseTag patterns)
**Status**: Ready for Implementation
**Estimated Implementation Time**: 8-10 hours (5 sprints)
