# DevOps and Quality Tooling

## Overview

SparseTag uses modern Python DevOps practices to ensure code quality, maintainability, and reliability.

## Quality Tools

### Ruff - Linting and Formatting

**What it does:**
- Lints code for style issues, bugs, and anti-patterns
- Formats code automatically (replaces black)
- Sorts imports (replaces isort)
- Suggests modern Python syntax upgrades

**Configuration**: `pyproject.toml` `[tool.ruff]` section

**Usage:**
```bash
# Check code
ruff check src/ tests/

# Auto-fix issues
ruff check --fix src/ tests/

# Format code
ruff format src/ tests/

# Check formatting without changing
ruff format --check src/ tests/
```

**Rules enabled:**
- E/W: PEP 8 style (pycodestyle)
- F: Pyflakes (undefined names, unused imports)
- I: Import sorting (isort)
- N: PEP 8 naming conventions
- UP: Pyupgrade (modern Python syntax)
- B: Bugbear (common bugs and anti-patterns)
- C4: Comprehensions improvements
- PIE/RET/SIM: Code simplification
- RUF: Ruff-specific rules

### Mypy - Type Checking

**What it does:**
- Static type checking
- Catches type errors before runtime
- Enforces type hint coverage

**Configuration**: `mypy.ini` and `pyproject.toml` `[tool.mypy]`

**Usage:**
```bash
# Check specific files
mypy src/sparsetag.py src/cache_manager.py src/exceptions.py

# Check all source
mypy src/
```

**Strict mode enabled:**
- All functions must have type hints
- No untyped definitions
- No implicit Optional
- Strict equality checks

### Pytest - Testing

**What it does:**
- Runs 173+ unit tests
- Measures code coverage
- Generates coverage reports

**Configuration**: `pyproject.toml` `[tool.pytest.ini_options]`

**Usage:**
```bash
# Run all tests
python -m pytest tests/

# With coverage
python -m pytest tests/ --cov=src

# With detailed coverage
python -m pytest tests/ --cov=src --cov-report=term-missing

# Fail if coverage < 85%
python -m pytest tests/ --cov=src --cov-fail-under=85

# Generate HTML report
python -m pytest tests/ --cov=src --cov-report=html
```

## Pre-commit Hooks

**What they do:**
- Run quality checks automatically before each commit
- Prevent bad commits from entering history
- Provide immediate feedback

**Setup:**
```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install
```

**What runs:**
1. File cleanup (trailing whitespace, end-of-file fixes)
2. File validation (YAML, TOML, JSON syntax)
3. Ruff format (auto-format code)
4. Ruff check (lint with auto-fix)
5. Mypy (type checking)
6. Pytest (all tests + coverage ≥85%)

**Manual execution:**
```bash
# Run all hooks
pre-commit run --all-files

# Run specific hook
pre-commit run ruff --all-files
pre-commit run pytest --all-files

# Skip hooks (not recommended)
git commit --no-verify
```

## Continuous Integration (GitHub Actions)

**What it does:**
- Runs tests on every push and pull request
- Tests on Python 3.9, 3.10, 3.11, 3.12, 3.13
- Tests on Ubuntu and Windows
- Reports coverage to Codecov
- Blocks PRs if tests fail

**Workflow**: `.github/workflows/ci.yml`

**Jobs:**
1. **quality**: Fast quality checks (ruff, mypy) on Python 3.11
2. **test**: Full test matrix (10 combinations: 5 Python × 2 OS)

**Coverage reporting:**
- Uploads to codecov.io from Ubuntu + Python 3.11
- Adds coverage report to PRs
- Fails if coverage drops below 85%

**Badges**: Status badges in README.md show CI status and coverage

## Coverage Reporting (Codecov)

**What it does:**
- Tracks code coverage over time
- Shows coverage changes in PRs
- Provides coverage badges
- Enforces coverage requirements

**Configuration**: `.codecov.yml`

**Requirements:**
- Project coverage: ≥85%
- Patch coverage: ≥85% (new code)
- Threshold: 1% (allows minor fluctuations)

**Dashboard**: https://codecov.io/gh/your-org/sparsetagging

## SonarCloud Quality Monitoring

**What it does:**
- Comprehensive code quality and security analysis
- Detects vulnerabilities (OWASP Top 10, CWE coverage)
- Tracks code complexity and duplication
- Monitors technical debt over time
- Blocks PRs that don't meet quality standards

**Configuration**: `sonar-project.properties`

**Dashboard**: https://sonarcloud.io/project/overview?id=vonbraun_SparseTagging

### Weekly Quality Review (15 min)

**Schedule**: Every Monday at 9 AM

**Steps:**
1. **Dashboard Overview**
   - Go to https://sonarcloud.io/project/overview?id=vonbraun_SparseTagging
   - Check Quality Gate status (pass/fail)
   - Review trend graphs (last 30 days)

2. **Security Tab**
   - Filter: Severity = BLOCKER or CRITICAL
   - Review new vulnerabilities (if any)
   - Create GitHub issues for non-trivial fixes
   - Assign to team member

3. **Measures Tab**
   - Coverage: Trending up/down? (target: maintain 88%+)
   - Complexity: New spikes? (investigate functions >15)
   - Duplication: Increasing? (refactor opportunities)
   - Technical Debt: Growing? (schedule cleanup sprint)

4. **Issues Tab**
   - Filter: Assigned to you
   - Prioritize: BLOCKER > CRITICAL > MAJOR > MINOR
   - Resolve or defer

### Metrics Glossary

| Metric | Definition | Target |
|--------|------------|--------|
| **Security Rating** | A-E scale based on vulnerability count/severity | A (zero vulnerabilities) |
| **Reliability Rating** | A-E scale based on bug count/severity | A (zero bugs) |
| **Maintainability Rating** | A-E scale based on technical debt ratio | A (≤5% debt) |
| **Coverage** | % of code executed by tests | ≥85% overall, ≥90% new |
| **Cognitive Complexity** | How hard code is to understand (per function) | ≤15 |
| **Cyclomatic Complexity** | Number of code paths (per function) | ≤10 |
| **Code Smells** | Maintainability issues (style, complexity, etc.) | <50 overall, <5 new |
| **Technical Debt** | Estimated time to fix all code smells | <1 day overall |
| **Duplicated Lines** | % of code duplicated elsewhere | ≤3% |

### Interpreting Ratings

**Security/Reliability/Maintainability Ratings:**
- **A**: 0 issues (excellent)
- **B**: ≥1 minor issue
- **C**: ≥1 major issue
- **D**: ≥1 critical issue
- **E**: ≥1 blocker issue

**Coverage:**
- **Green**: ≥85%
- **Yellow**: 70-84%
- **Red**: <70%

### Common Fixes

**Cognitive Complexity >15:**
```python
# Before (complexity: 25)
def execute_query(query):
    if 'operator' in query:
        if query['operator'] == 'AND':
            # 15 lines of logic
        elif query['operator'] == 'OR':
            # 15 lines of logic
        elif query['operator'] == 'NOT':
            # 10 lines of logic
    else:
        # 10 lines of single-column logic

# After (complexity: 5 each)
def execute_query(query):
    if 'operator' in query:
        return _execute_multi_column_query(query)
    return _execute_single_column_query(query)

def _execute_multi_column_query(query):
    handlers = {'AND': _handle_and, 'OR': _handle_or, 'NOT': _handle_not}
    return handlers[query['operator']](query)
```

**Code Duplication:**
```python
# Before (duplicated in 3 places)
def test_query_high():
    st = SparseTag.create_random(1000, ['Tag1'], 1.0, seed=42)
    result = st.query({'column': 'Tag1', 'op': '==', 'value': TagConfidence.HIGH})
    # assertions...

# After (DRY)
@pytest.fixture
def sample_sparse_tag():
    return SparseTag.create_random(1000, ['Tag1'], 1.0, seed=42)

def test_query_high(sample_sparse_tag):
    result = sample_sparse_tag.query({'column': 'Tag1', 'op': '==', 'value': TagConfidence.HIGH})
    # assertions...
```

### CVE Scanning (GitHub Dependabot)

**What it does:**
- Monitors numpy, scipy, psutil for security vulnerabilities
- Creates automated PRs for dependency updates
- Groups security patches for easier review

**Configuration**: `.github/dependabot.yml`

**Handling CVE Alerts:**
1. Dependabot creates PR with title `chore(deps): bump [package] from X to Y`
2. Review PR description for CVE details and severity
3. Check changelog for breaking changes
4. Run tests locally: `pytest tests/`
5. If tests pass, merge immediately
6. If tests fail, investigate compatibility and create fix

**Manual CVE Check:**
```bash
# Install pip-audit
pip install pip-audit

# Scan for CVEs
pip-audit -r requirements.txt

# Output shows:
# - CVE ID (e.g., CVE-2024-12345)
# - Severity (CRITICAL, HIGH, MEDIUM, LOW)
# - Affected version range
# - Fixed version
```

## Development Workflow

### Initial Setup

```bash
# Clone and setup
git clone https://github.com/your-org/sparsetagging.git
cd sparsetagging
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements-dev.txt
pre-commit install
```

### Making Changes

```bash
# Create branch
git checkout -b feature/my-feature

# Make changes
# ... edit code ...

# Pre-commit runs automatically on commit
git add .
git commit -m "Add feature X"

# Pre-commit will:
# 1. Format code with ruff
# 2. Lint with ruff
# 3. Type check with mypy
# 4. Run all tests with coverage

# Push (triggers CI)
git push origin feature/my-feature
```

### Quality Checklist

Before pushing:
- [ ] Pre-commit hooks pass
- [ ] All tests pass (173+)
- [ ] Coverage ≥85%
- [ ] No mypy errors
- [ ] No ruff violations
- [ ] Updated CHANGELOG.md

### Troubleshooting

**Pre-commit is slow:**
- Pytest runs 173 tests on every commit
- Consider `git commit --no-verify` for WIP commits
- Run `pre-commit run pytest` manually before final commit

**Ruff format changed my code:**
- Ruff enforces consistent style
- Review changes: `git diff`
- If you disagree, add to `pyproject.toml` ruff.lint.ignore

**Mypy errors after updating dependencies:**
- Update type stubs: `pip install --upgrade mypy`
- Check `mypy.ini` for ignore settings

**Coverage dropped below 85%:**
- Add tests for new code
- Check uncovered lines: `pytest --cov=src --cov-report=term-missing`
- Remove dead code if applicable

## Tool Comparison

| Tool | Purpose | Replaces | Speed | Auto-fix |
|------|---------|----------|-------|----------|
| **ruff** | Lint + Format | flake8, black, isort, pyupgrade | ⚡ 10-100x faster | ✅ Yes |
| **mypy** | Type checking | pylint (partial) | Medium | ❌ No |
| **pytest** | Testing | unittest | Fast | ❌ No |
| **pre-commit** | Automation | Manual checks | N/A | ✅ Runs auto-fix tools |
| **codecov** | Coverage reporting | Local coverage only | N/A | ❌ No |

## Best Practices

1. **Run pre-commit before pushing** - Catches issues early
2. **Don't skip pre-commit** - Keeps codebase clean
3. **Monitor coverage trends** - Keep coverage high
4. **Fix mypy errors immediately** - Type safety prevents bugs
5. **Use ruff auto-fix** - `ruff check --fix` saves time
6. **Review ruff suggestions** - Learn better Python patterns

## Configuration Details

### Ruff Configuration (pyproject.toml)

```toml
[tool.ruff]
target-version = "py39"
line-length = 100

[tool.ruff.lint]
select = ["E", "W", "F", "I", "N", "UP", "B", "C4", "PIE", "RET", "SIM", "PTH", "RUF"]
ignore = ["E501", "PTH123"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

**Key settings:**
- `target-version`: Python 3.9+ (matches minimum version)
- `line-length`: 100 characters (consistent with existing code)
- `select`: Comprehensive rule set covering style, bugs, and modernization
- `ignore E501`: Line length handled by formatter
- `ignore PTH123`: Allow `open()` instead of `Path.open()`

### Pre-commit Configuration (.pre-commit-config.yaml)

Hooks run in this order:
1. File cleanup (trailing whitespace, EOF)
2. File validation (YAML, TOML, JSON)
3. Ruff format (auto-format)
4. Ruff lint (with auto-fix)
5. Mypy (type check specific files)
6. Pytest (full test suite + coverage)

**Why this order:**
- Format before lint avoids format-then-lint loops
- Type check after formatting for cleaner code
- Tests last because they're slowest

### GitHub Actions CI (.github/workflows/ci.yml)

**Two-job strategy:**
1. **quality** job: Fast linting and type checking (Ubuntu, Python 3.11)
2. **test** job: Full matrix testing (5 Python versions × 2 OS)

**Benefits:**
- Fast feedback on code quality issues
- Comprehensive testing across environments
- Coverage reporting from single canonical environment

### Codecov Configuration (.codecov.yml)

**Coverage thresholds:**
- Project: 85% (matches pytest requirement)
- Patch: 85% (new code must maintain coverage)
- Threshold: 1% (allows minor fluctuations)

**Ignored files:**
- `tests/*` (don't count test coverage)
- `src/benchmark.py` (benchmark script)

## Common Tasks

### Adding a new dependency

1. Add to `requirements.txt` (runtime) or `requirements-dev.txt` (dev only)
2. Install: `pip install -r requirements-dev.txt`
3. Update docs if needed
4. Commit both files

### Updating tool versions

```bash
# Update ruff
pip install --upgrade ruff
pre-commit autoupdate

# Update other tools
pip install --upgrade mypy pytest pytest-cov

# Verify everything works
pre-commit run --all-files
```

### Running specific tests

```bash
# Single test file
python -m pytest tests/test_cache_manager.py

# Single test class
python -m pytest tests/test_cache_manager.py::TestCacheManager

# Single test method
python -m pytest tests/test_cache_manager.py::TestCacheManager::test_initialization

# Tests matching pattern
python -m pytest tests/ -k "cache"
```

### Debugging test failures

```bash
# Show full traceback
python -m pytest tests/ -v --tb=long

# Stop on first failure
python -m pytest tests/ -x

# Show print statements
python -m pytest tests/ -s

# Run last failed tests
python -m pytest tests/ --lf
```

## CI/CD Integration

### Setting up GitHub Actions

1. Push `.github/workflows/ci.yml` to repository
2. GitHub automatically detects and runs workflow
3. View results in "Actions" tab

### Setting up Codecov

1. Sign up at https://codecov.io
2. Connect GitHub repository
3. Add `CODECOV_TOKEN` to GitHub repository secrets:
   - Go to repository Settings → Secrets → Actions
   - Add new secret named `CODECOV_TOKEN`
   - Paste token from Codecov dashboard
4. Push to trigger workflow
5. View coverage at `https://codecov.io/gh/your-org/sparsetagging`

### Adding status badges to README

Update URLs in README.md after setting up CI and Codecov:

```markdown
![CI Status](https://github.com/YOUR-ORG/sparsetagging/workflows/CI/badge.svg)
![Coverage](https://codecov.io/gh/YOUR-ORG/sparsetagging/branch/main/graph/badge.svg)
```

## Maintenance

### Quarterly review checklist

- [ ] Update tool versions (`pre-commit autoupdate`)
- [ ] Review and update ruff rules
- [ ] Check for new mypy strict settings
- [ ] Update Python version matrix in CI
- [ ] Review and update coverage thresholds
- [ ] Clean up ignored warnings/errors

### When things break

**CI failing:**
1. Check Actions tab for error details
2. Reproduce locally: `pre-commit run --all-files`
3. Fix issues
4. Push fix

**Pre-commit hook failing:**
1. Run manually to see error: `pre-commit run --all-files`
2. Run specific hook: `pre-commit run ruff --all-files`
3. Fix issue or update configuration
4. Test: `pre-commit run --all-files`

**Coverage dropping:**
1. Check which files lack coverage: `pytest --cov=src --cov-report=term-missing`
2. Add tests for uncovered lines
3. Remove dead code if applicable

## References

- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Mypy Documentation](https://mypy.readthedocs.io/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Pre-commit Documentation](https://pre-commit.com/)
- [Codecov Documentation](https://docs.codecov.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## Getting Help

If you encounter issues:

1. Check this document first
2. Review tool documentation
3. Check `.github/workflows/ci.yml` for CI configuration
4. Check `.pre-commit-config.yaml` for hook configuration
5. Check `pyproject.toml` for tool settings
6. Open an issue with:
   - Error message
   - Steps to reproduce
   - Environment (Python version, OS, tool versions)
