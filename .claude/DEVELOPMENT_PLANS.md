# Development Plans Archive

This file documents significant planning sessions from Claude Code, preserving the evolution of design decisions and implementation strategies across the SparseTagging project.

## Purpose

Development plans capture the thought process behind major features, bug fixes, and architectural decisions. Unlike session documentation (which focuses on what was accomplished), plans document:

- **Problem analysis** - Root cause identification and constraints
- **Design decisions** - Why certain approaches were chosen
- **Implementation strategy** - Step-by-step execution plans
- **Trade-offs considered** - Alternative approaches and their pros/cons

These plans serve as:
- **Learning material** for understanding project evolution
- **Reference documentation** for future similar problems
- **Training examples** for effective prompting and collaboration with AI
- **Historical record** of architectural decisions

Plans are stored globally at `~/.claude/plans/` and linked here for project-specific context.

---

## Plan 1: snug-crunching-sunset.md
**Date:** 2025-12-18
**Status:** Completed
**Related Sessions:** Unknown
**Summary:** Fix Claude CLI Subprocess Timeout Issue - Resolved hardcoded Git Bash path causing 300-second timeouts

# Fix Claude CLI Subprocess Timeout Issue

## Problem Statement

When running `python -m framework.main` standalone (outside of Claude Code session), the subprocess that calls Claude CLI times out after exactly 300 seconds. However, when the same code runs inside a Claude Code session, it completes successfully in ~36 seconds.

## Symptoms

```
2025-12-18 10:07:13,928 - INFO - Running Claude CLI (timeout=300s, budget=$5.0)
2025-12-18 10:12:14,077 - ERROR - Claude CLI timed out after 300 seconds
```

The subprocess hangs for exactly 300 seconds before timing out.

## What Has Been Tried (All Failed)

1. **Increased timeout to 900 seconds** - Still timed out
2. **Verified prompt size** - Only 1.6KB, not an issue
3. **Tested Claude CLI manually** - Works fine with simple commands
4. **Verified configuration centralization** - Working correctly (config values being used)

## Root Cause Identified

**Hardcoded Git Bash Path for Wrong User**

In `framework/claude_runner.py:77`:
```python
git_bash_path = r'C:\Users\cgbraun\AppData\Local\Programs\Git\bin\bash.exe'
```

- Path is hardcoded to user **"cgbraun"**
- Current user is **"major"**
- Verified: This path does NOT exist on the current system
- Claude CLI likely hangs waiting for a bash executable that doesn't exist

System git installation is at: `C:\Program Files\Git\`

## Implementation Plan

### Solution: Fix Git Bash Path Detection

**File to modify:** `framework/claude_runner.py`

**Changes needed:**

1. **Remove hardcoded path** (line 77) for user "cgbraun"

2. **Add dynamic git-bash detection** that tries multiple locations:
   - Current user's local installation: `C:\Users\{username}\AppData\Local\Programs\Git\bin\bash.exe`
   - System-wide installation: `C:\Program Files\Git\bin\bash.exe`
   - Alternative location: `C:\Program Files (x86)\Git\bin\bash.exe`
   - Check if already set in environment

3. **Implement detection logic:**
   ```python
   import os
   from pathlib import Path

   # Only set if not already in environment
   if 'CLAUDE_CODE_GIT_BASH_PATH' not in env:
       # Get current username
       username = os.environ.get('USERNAME', 'major')

       # Try multiple possible git-bash locations
       possible_paths = [
           Path(f"C:/Users/{username}/AppData/Local/Programs/Git/bin/bash.exe"),
           Path("C:/Program Files/Git/bin/bash.exe"),
           Path("C:/Program Files (x86)/Git/bin/bash.exe"),
       ]

       for git_bash_path in possible_paths:
           if git_bash_path.exists():
               env['CLAUDE_CODE_GIT_BASH_PATH'] = str(git_bash_path)
               logger.info(f"Set CLAUDE_CODE_GIT_BASH_PATH to {git_bash_path}")
               break
       else:
           logger.warning("Could not find git-bash, Claude CLI may have issues")
   ```

4. **Test the fix:**
   ```bash
   python -m framework.main --reset --max-tests 1
   ```

   Should complete in ~30-40 seconds without timing out.

## Critical Files

- `framework/claude_runner.py` - Lines 73-80 (git-bash path detection)
- `framework/config.py` - Configuration (timeout is correctly set to 300s, no changes needed)

## Validation Criteria

✓ Test runs without timeout
✓ Completes in ~30-60 seconds
✓ Generates code successfully
✓ Logs show correct git-bash path detected
✓ Works for any Windows user (not hardcoded to "cgbraun")

## Notes

- Do NOT change `CLAUDE_TIMEOUT_SECONDS` - keep at 300 seconds
- The timeout value is working correctly; the issue is the subprocess hanging due to missing bash.exe
- Configuration centralization work was completed successfully in previous session

---

## Plan 2: wise-soaring-rose.md
**Date:** 2025-12-18
**Status:** Completed
**Related Sessions:** Unknown
**Summary:** Fix Framework Issues and Improve Test Methodology - Fixed 3 critical bugs (overall score persistence, token metrics, classification test syntax) and added rate limit handling

# Fix Framework Issues and Improve Test Methodology

## Problem Analysis

The framework has run successfully but results show critical bugs and methodology issues:

### Critical Bugs Identified

1. **Overall Score Always 0** - Calculated but never saved to metrics.json
2. **Token/Cost Always 0** - `claude --print` doesn't output metadata, parsing fails
3. **Classification Tests Never Run** - Syntax error in test file (line 161)
4. **Methodology Issues** - Tasks too complex, low signal-to-noise ratio

### Data from Example Run (27/54 tests completed)

**Pytest Pass Rates:**
- Classification: 0% (0/0 tests - syntax error prevents collection)
- Data Cleaning: 11% (1/9 tests passing)
- Feature Engineering: 9% (1/11 tests passing)

**Observed Issues:**
- Overall scores show 0 in CSV but execution.log shows 44-61 range
- Token counts: all 0 (should be thousands)
- Cost: all $0 (should be ~$0.01-0.10 per run)
- No differentiation between prompt styles (all perform similarly poorly)

---

## Root Cause Analysis

### Bug #1: Overall Score Not Persisted

**Location:** framework/metrics_analyzer.py:59-61, framework/main.py:142-143

**Issue:**
1. `analyze_code()` saves metrics.json (line 60)
2. `main.py` calculates overall_score AFTER (line 142-143)
3. overall_score added to in-memory dict but never re-saved
4. Report generator reads metrics.json, finds overall_score=0 (default)

**Fix:** Save metrics.json again after adding overall_score

---

### Bug #2: Token/Cost Parsing Fails

**Location:** framework/claude_runner.py:106-115

**Issue:**
- `claude --print` outputs only the response text (no metadata)
- `parse_cost_from_output()` searches for `"$0.05"` patterns that don't exist
- Always returns None, causing estimated_tokens=0, cost_usd=0

**Options:**
- A: Remove token/cost scoring (10% of score) - **Quick fix**
- B: Parse from Claude stderr/status output - **May not exist**
- C: Estimate tokens from prompt+response length - **Approximation**

**Recommendation:** Option C - estimate tokens as (prompt_chars + response_chars) / 4

---

### Bug #3: Classification Test Syntax Error

**Location:** test_modules/tests/test_classification.py:161

**Issue:**
```python
class TestEvaluation Metrics:  # Space in class name!
```

**Fix:** Change to:
```python
class TestEvaluationMetrics:
```

---

### Methodology Issue: Tasks Too Difficult

**Current State:**
- Tasks expect 120-180 LOC production-ready code
- Complex requirements (9-11 pytest tests each)
- Failure rates: 89-100% across all prompts
- No clear winner between prompt styles

**Problems:**
1. **Low success rates** make it hard to differentiate prompt effectiveness
2. **Complex tasks** obscure signal - too many ways to fail
3. **Strict test criteria** (metadata, specific implementations) too rigid
4. **All prompts fail similarly** - no useful comparison

**Example:** Data cleaning task requires:
- Missing value handling (multiple strategies)
- Outlier detection (IQR or z-score)
- Column standardization (snake_case)
- Data type consistency
- Return cleaned DataFrame + metadata report

Claude often generates code that works but fails specific test assertions (e.g., "must return metadata dict with specific keys").

---

## Implementation Plan - Bug Fixes Only

**Scope:** Fix 3 critical bugs, re-run report generation on existing data
**User Decision:** Option A - Bug fixes only, defer methodology improvements until after rerun

### Changes to Implement

**1. Fix Overall Score Persistence Bug**

**File:** `framework/main.py` (around line 143)

**Problem:**
- `analyze_code()` saves metrics.json (line 132)
- `calculate_overall_score()` runs AFTER and adds to in-memory dict (line 142-143)
- overall_score never saved back to metrics.json
- Report generator reads stale file, sees overall_score=0

**Solution:**
```python
# After line 143, add:
from framework.utils import save_json

metrics['overall_score'] = overall_score
# Re-save metrics with overall_score included
metrics_file = Path(run_dir) / "metrics.json"
save_json(metrics, str(metrics_file))
logger.info(f"Saved updated metrics with overall score")
```

---

**2. Remove Token/Cost Metrics Entirely**

**Files to modify:**
- `framework/claude_runner.py` - Remove token parsing code
- `framework/metrics_analyzer.py` - Remove token component from scoring (recalculate weights)
- `framework/config.py` - Remove TOKEN_WEIGHT constant
- `framework/report_generator.py` - Remove token columns from reports

**Rationale:**
- `claude --print` doesn't provide metadata
- No reliable way to get actual token counts
- Remove instead of estimating (cleaner)
- Redistribute 10% weight to other metrics

**Changes:**

**a) framework/claude_runner.py:106-115**
- Delete entire token/cost parsing block
- Remove from result dict
```python
# DELETE these lines:
cost = parse_cost_from_output(process.stdout)
if cost:
    estimated_tokens = estimate_tokens_from_cost(cost)
    result['cost_usd'] = cost
    result['estimated_tokens'] = estimated_tokens
    logger.info(f"Estimated cost: ${cost:.4f}, tokens: {estimated_tokens}")
else:
    result['cost_usd'] = 0
    result['estimated_tokens'] = 0
```

**b) framework/config.py**
- Remove `TOKEN_WEIGHT = 10`
- Redistribute weight: Add 5% to Speed, 5% to Quality
```python
# Old weights (100 total):
PYTEST_WEIGHT = 30
QUALITY_WEIGHT = 20
COMPLEXITY_WEIGHT = 15
DOCUMENTATION_WEIGHT = 15
SPEED_WEIGHT = 10
TOKEN_WEIGHT = 10  # DELETE THIS

# New weights (100 total):
PYTEST_WEIGHT = 30
QUALITY_WEIGHT = 25  # 20 + 5
COMPLEXITY_WEIGHT = 15
DOCUMENTATION_WEIGHT = 15
SPEED_WEIGHT = 15   # 10 + 5
```

**c) framework/metrics_analyzer.py:300-308**
- Delete token scoring section

**d) framework/main.py:137-139**
- Remove token/cost from execution metadata
```python
# Change:
metrics['execution'] = {
    'duration_seconds': test_timer.get_duration(),
    'cost_usd': claude_result.get('cost_usd', 0),          # DELETE
    'estimated_tokens': claude_result.get('estimated_tokens', 0)  # DELETE
}

# To:
metrics['execution'] = {
    'duration_seconds': test_timer.get_duration()
}
```

**e) framework/report_generator.py**
- Remove token/cost columns from CSV/JSON/Excel exports
- Remove from aggregation logic
- Remove from charts/reports

---

**3. Fix Classification Test Syntax Error**

**File:** `test_modules/tests/test_classification.py:161`

**Problem:** Class name has space: `class TestEvaluation Metrics:`

**Solution:**
```python
# Line 161, change:
class TestEvaluation Metrics:

# To:
class TestEvaluationMetrics:
```

---

**4. Re-run Report Generation on Fixed Data**

After fixing bugs, update existing test metrics:

**Script to update existing metrics.json files:**
```python
# Update all existing metrics files with overall_score
import json
from pathlib import Path
from framework.metrics_analyzer import calculate_overall_score

results_dir = Path("results/ExampleRuns/runs")
for run_dir in results_dir.glob("run_*"):
    metrics_file = run_dir / "metrics.json"
    if metrics_file.exists():
        with open(metrics_file) as f:
            metrics = json.load(f)

        # Calculate and add overall_score
        overall_score = calculate_overall_score(metrics)
        metrics['overall_score'] = overall_score

        # Save back
        with open(metrics_file, 'w') as f:
            json.dump(metrics, f, indent=2)

        print(f"Updated {run_dir.name}: overall_score={overall_score}")
```

**Then regenerate reports:**
```bash
python -m framework.main --generate-report
```

---

## Implementation Steps

1. ✅ Fix overall_score persistence in `framework/main.py`
2. ✅ Remove token metrics from `framework/claude_runner.py`
3. ✅ Update scoring weights in `framework/config.py`
4. ✅ Remove token scoring from `framework/metrics_analyzer.py`
5. ✅ Remove token columns from `framework/report_generator.py`
6. ✅ Fix class name in `test_modules/tests/test_classification.py`
7. ✅ Create script to update existing metrics files
8. ✅ Run update script on existing results
9. ✅ Regenerate reports with corrected data

---

## Critical Files

- `framework/main.py` - Overall score persistence
- `framework/claude_runner.py` - Remove token parsing
- `framework/config.py` - Update weights
- `framework/metrics_analyzer.py` - Remove token scoring
- `framework/report_generator.py` - Remove token columns
- `test_modules/tests/test_classification.py` - Syntax fix

---

## Expected Outcomes

After fixes:
- ✅ Overall scores visible in reports (44-61 range)
- ✅ Classification tests run successfully
- ✅ No token/cost metrics (removed completely)
- ✅ Clean reports showing real differentiation between prompts
- ✅ Can identify which prompt variation works best

Then decide on methodology improvements for future runs.

---

## CRITICAL FINDING: Rate Limit Failures

### Discovery

All 27 "FAILED" tests were NOT actual test failures - they hit Claude API rate limit!

**Evidence:**
- Failed runs complete in 6-8 seconds (not 30-40s like successful runs)
- `claude_output.txt` contains: "Limit reached · resets 11pm (America/New_York)"
- Exit code 1, empty stderr
- No code generated, no metrics collected

**Affected prompt variations:**
- `role_*` (9 tests)
- `specification_*` (9 tests)
- `combined_*` (9 tests)

**Successful variations:**
- `baseline_*` (9 tests) ✓
- `cot_*` (9 tests) ✓
- `emotional_*` (9 tests) ✓

**Root cause:** Tests ran sequentially, hit hourly rate limit after 27 successful runs.

---

## Additional Requirements: Rate Limit Handling

### Problem

Framework treats rate limit errors as test failures, corrupting results:
- Can't distinguish "test failed" from "API limit reached"
- Failed tests counted in statistics (50% failure rate is misleading)
- No way to retry incomplete tests without full reset
- Reports show failed variations that never actually ran

### Options for Handling Rate Limits

**Option 1: Detect and Mark as INCOMPLETE (Recommended)**

Modify `framework/claude_runner.py` and `framework/state_manager.py`:

```python
# In claude_runner.py, detect rate limit:
if "Limit reached" in process.stdout or "limit reached" in process.stdout.lower():
    result['error'] = "RATE_LIMIT_EXCEEDED"
    result['rate_limit'] = True
    logger.warning("Hit Claude API rate limit")
    return result

# In state_manager.py, add new status:
# Status can be: PENDING, IN_PROGRESS, SUCCESS, FAILED, INCOMPLETE
if 'rate_limit' in result and result['rate_limit']:
    status = 'INCOMPLETE'
else:
    status = 'FAILED'
```

**Benefits:**
- Clear distinction between real failures and rate limits
- Can filter INCOMPLETE from reports
- Easy to retry: `--retry-incomplete` flag

**Option 2: Add Exponential Backoff/Retry**

Automatically retry with delays when rate limit hit:

```python
# In claude_runner.py:
MAX_RETRIES = 3
BACKOFF_DELAYS = [60, 300, 900]  # 1min, 5min, 15min

for retry in range(MAX_RETRIES):
    result = run_claude_cli(...)
    if not result.get('rate_limit'):
        break
    if retry < MAX_RETRIES - 1:
        delay = BACKOFF_DELAYS[retry]
        logger.info(f"Rate limit hit, waiting {delay}s before retry...")
        time.sleep(delay)
```

**Benefits:**
- Automatic handling
- Tests complete eventually

**Drawbacks:**
- Long wait times (up to 15min per retry)
- May still fail if persistent rate limit

**Option 3: Detect and Stop Immediately**

Stop entire test suite when rate limit detected:

```python
if "Limit reached" in output:
    logger.error("Claude API rate limit reached!")
    logger.error("Please wait until limit resets, then resume with:")
    logger.error("  python -m framework.main --retry-incomplete")
    sys.exit(2)  # Special exit code for rate limit
```

**Benefits:**
- Prevents wasting time on tests that will fail
- Clear guidance to user

**Drawbacks:**
- Requires manual intervention
- Must wait for limit reset

**Option 4: Mark and Continue**

Like Option 1, but continue running other tests:

- Mark rate-limited tests as INCOMPLETE
- Continue to next test
- At end, report how many incomplete

**Benefits:**
- Maximizes tests completed
- Can retry incomplete later

**Drawbacks:**
- May hit limit repeatedly
- Doesn't save time if limit persists

---

### Recommended Approach

**Combination of Options 1 + 3:**

1. **Detect rate limit** in `claude_runner.py`
2. **Mark as INCOMPLETE** in state manager
3. **Stop test suite** when first rate limit detected
4. **Provide clear message**:
   ```
   ⚠️  Claude API rate limit reached (27/54 tests completed)

   The limit resets at 11pm (America/New_York).

   To resume and complete remaining tests:
     python -m framework.main

   The framework will automatically skip completed tests.
   ```

5. **Add `--retry-incomplete` flag** to rerun only INCOMPLETE tests

---

### Implementation Details

**1. Add rate limit detection:**

File: `framework/claude_runner.py`

```python
# After getting stdout, check for rate limit
if "Limit reached" in result['stdout'] or "limit reached" in result['stdout'].lower():
    result['error'] = "Claude API rate limit reached"
    result['rate_limit'] = True
    logger.warning(f"Rate limit detected. Output: {result['stdout'][:100]}")
    return result
```

**2. Add INCOMPLETE status:**

File: `framework/state_manager.py`

Add to test status enum/handling:
```python
# Status values: PENDING, IN_PROGRESS, SUCCESS, FAILED, INCOMPLETE

def mark_test_incomplete(test_id, error, run_dir):
    """Mark test as incomplete (rate limit, timeout, etc.)"""
    # Similar to mark_test_failed but different status
```

**3. Stop on rate limit:**

File: `framework/main.py`

```python
# After run_claude_cli returns:
if claude_result.get('rate_limit'):
    logger.error("\n" + "="*70)
    logger.error("RATE LIMIT REACHED")
    logger.error("="*70)
    logger.error(f"Completed: {state.completed_tests}/{state.total_tests}")
    logger.error(f"Remaining: {state.total_tests - state.completed_tests}")
    logger.error("\nThe Claude API rate limit has been reached.")
    logger.error("Wait until the limit resets, then resume:")
    logger.error(f"  python -m framework.main")
    logger.error("="*70)

    state.mark_test_incomplete(test_id, "Rate limit reached", run_dir)
    sys.exit(2)  # Exit code 2 = rate limit
```

**4. Add --retry-incomplete flag:**

File: `framework/main.py`

```python
parser.add_argument(
    "--retry-incomplete",
    action="store_true",
    help="Retry only tests marked as INCOMPLETE (rate limits, etc.)"
)

# In get_pending_tests:
if args.retry_incomplete:
    tests = [t for t in all_tests if state.tests[t]['status'] == 'INCOMPLETE']
else:
    tests = [t for t in all_tests if state.tests[t]['status'] == 'PENDING']
```

**5. Exclude INCOMPLETE from reports:**

File: `framework/report_generator.py`

```python
# Filter out incomplete tests
successful_tests = [
    t for t_id, t in state['tests'].items()
    if t['status'] == 'SUCCESS'
]
```

---

### Updated Implementation Steps

1. ✅ Fix overall_score persistence in `framework/main.py`
2. ✅ Remove token metrics from `framework/claude_runner.py`
3. ✅ Update scoring weights in `framework/config.py`
4. ✅ Remove token scoring from `framework/metrics_analyzer.py`
5. ✅ Remove token columns from `framework/report_generator.py`
6. ✅ Fix class name in `test_modules/tests/test_classification.py`
7. ✅ **Add rate limit detection** in `framework/claude_runner.py`
8. ✅ **Add INCOMPLETE status** in `framework/state_manager.py`
9. ✅ **Stop suite on rate limit** in `framework/main.py`
10. ✅ **Add --retry-incomplete flag** in `framework/main.py`
11. ✅ **Filter INCOMPLETE from reports** in `framework/report_generator.py`
12. ✅ Create script to update existing metrics files
13. ✅ Run update script on existing results
14. ✅ Regenerate reports with corrected data (excluding incomplete tests)

---

## User Decision

**Rate Limit Handling:** Option A - Detect + Stop

When rate limit detected:
1. Mark test as INCOMPLETE
2. Save state immediately
3. Stop test suite execution
4. Display clear message with:
   - Number of completed tests
   - When limit resets
   - How to resume: `python -m framework.main`
5. Exit with code 2 (distinct from normal errors)

Benefits:
- Clean, predictable behavior
- No wasted time on tests that will fail
- Easy to resume after limit resets
- Framework automatically skips completed tests

---

## Final Implementation Summary

**Bug Fixes:**
1. Overall score persistence
2. Remove token/cost metrics completely
3. Fix classification test syntax error

**New Features:**
4. Rate limit detection and handling
5. INCOMPLETE test status
6. Stop-on-limit behavior with clear messaging
7. --retry-incomplete flag for targeted reruns

**After Implementation:**
- Fix existing 27 successful test results (add overall_score)
- Regenerate reports (exclude INCOMPLETE tests)
- When rate limit resets, rerun incomplete tests: `python -m framework.main`
- All 54 tests will complete successfully
- Can properly compare all 6 prompt variations

---

## Plan 3: humming-skipping-pond.md
**Date:** 2025-12-24
**Status:** Completed
**Related Sessions:** Unknown
**Summary:** DevOps Quality Tooling Plan for SparseTag - Added ruff linting/formatting, pre-commit hooks, GitHub Actions CI/CD, and Codecov integration

# DevOps Quality Tooling Plan for SparseTag

## Current State Analysis

### Existing Quality Tools ✅
- **pytest** (7.0+): 173 tests, ≥85% coverage target
- **pytest-cov** (4.0+): Coverage reporting (HTML reports)
- **mypy** (1.0+): Type checking with strict mode, 100% type hint coverage
- **Configuration**: All configured in `pyproject.toml` with good settings

### What's Missing ❌
- No automated linting/formatting
- No pre-commit hooks
- No CI/CD pipeline (GitHub Actions, etc.)
- No automated quality gates
- Manual quality checks in CONTRIBUTING.md

### Code Quality Observations
- Code follows PEP 8 conventions
- 100-character line limit
- Google-style docstrings
- Comprehensive type hints
- Good existing test coverage

## User Requirements
- Add DevOps tools like **ruff** to increase code quality
- **NO fluff** - only tools that are actually used and beneficial
- DevOps-ready: coverage, quality checks, automation

## Evaluation of DevOps Tools

### High Value (Recommended)

#### 1. **Ruff** - Modern Python Linter & Formatter
**Why valuable:**
- Replaces 6+ tools: flake8, isort, pyupgrade, autoflake, pydocstyle, etc.
- 10-100x faster than existing linters (written in Rust)
- Auto-fix capabilities
- Configurable in `pyproject.toml` (centralized config)
- Actively maintained, modern Python best practices

**What it does:**
- Linting: 800+ rules covering all major Python style issues
- Import sorting: Replaces isort
- Code formatting: Replaces black
- Auto-upgrades: Modern Python syntax (f-strings, type hints, etc.)

**Not fluff because:**
- Catches real bugs (unused variables, undefined names)
- Enforces consistency automatically
- Fast enough to run on every save in IDE
- Single tool replaces multiple dependencies

#### 2. **Pre-commit Hooks** - Automated Local Quality Gates
**Why valuable:**
- Runs quality checks BEFORE commit (prevents bad commits)
- Same checks locally as CI/CD (fail fast)
- Configurable per-tool
- Standard in professional Python projects

**What it runs:**
- ruff check + ruff format
- mypy type checking
- pytest (optional - can be slow)
- YAML/JSON/TOML validation
- Trailing whitespace, end-of-file fixes

**Not fluff because:**
- Catches issues before they reach CI/CD
- Saves time (no failed CI builds)
- Enforces quality standards automatically
- Can auto-fix most issues

#### 3. **GitHub Actions CI/CD** - Automated Testing & Quality
**Why valuable:**
- Runs tests on multiple Python versions (3.9-3.13)
- Automated quality gate for PRs
- Coverage reporting with badges
- Prevents regression
- Professional DevOps standard

**What it does:**
- Run pytest on matrix of Python versions
- Type checking with mypy
- Linting with ruff
- Coverage reporting (codecov/coveralls optional)
- Automated status checks on PRs

**Not fluff because:**
- Catches platform-specific bugs
- Ensures compatibility across Python versions
- Provides confidence before merge
- Standard for open-source projects

### Low Value (Not Recommended)

- **black**: Replaced by `ruff format` (same formatting, one less tool)
- **flake8**: Replaced by `ruff check` (faster, more comprehensive)
- **isort**: Replaced by `ruff check --select I` (same functionality)
- **pylint**: Slower than ruff, overlapping rules
- **bandit**: Security linter - valuable but adds complexity (defer)
- **Safety/pip-audit**: Dependency vulnerability scanning (defer for now)

## Pending Questions for User

[Questions will be added after clarification]

## Implementation Plan

### Phase 1: Add Ruff Configuration

**File: `pyproject.toml`**

Add the following sections to configure ruff:

```toml
[tool.ruff]
target-version = "py39"  # Match minimum Python version
line-length = 100  # Match existing style guide

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes (undefined names, unused imports)
    "I",    # isort (import sorting)
    "N",    # pep8-naming conventions
    "UP",   # pyupgrade (modernize Python syntax)
    "B",    # flake8-bugbear (common bugs)
    "C4",   # flake8-comprehensions (better comprehensions)
    "PIE",  # flake8-pie (unnecessary code)
    "RET",  # flake8-return (simplify returns)
    "SIM",  # flake8-simplify (simplify code)
    "PTH",  # flake8-use-pathlib (use pathlib)
    "RUF",  # Ruff-specific rules
]

ignore = [
    "E501",  # Line too long (handled by formatter)
    "PTH123", # open() instead of Path.open() - not critical for this project
]

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["PLR2004"]  # Magic values in tests are fine

[tool.ruff.lint.isort]
known-first-party = ["src"]
section-order = ["future", "standard-library", "third-party", "first-party", "local-folder"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
```

**Rationale:**
- **E, W, F**: Core PEP 8 and pyflakes rules - catch real issues
- **I**: Import sorting replaces isort
- **UP**: Modernize syntax (e.g., suggest f-strings)
- **B**: Bugbear catches common bugs (mutable defaults, etc.)
- **C4, PIE, RET, SIM**: Code quality improvements
- **PTH**: Encourage pathlib (but allow open() for simplicity)
- **RUF**: Ruff's own rules

### Phase 2: Update requirements-dev.txt

**File: `requirements-dev.txt`**

Add after mypy:

```txt
# Code quality and formatting
ruff>=0.1.14

# Pre-commit hooks
pre-commit>=3.6.0
```

**Why these versions:**
- ruff 0.1.14: Stable release with format + lint
- pre-commit 3.6.0: Modern version with good performance

### Phase 3: Create Pre-commit Configuration

**File: `.pre-commit-config.yaml`** (NEW)

```yaml
# Pre-commit hooks for code quality
# Install: pip install pre-commit
# Setup: pre-commit install
# Run manually: pre-commit run --all-files

repos:
  # Standard pre-commit hooks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
        exclude: ^reports/
      - id: end-of-file-fixer
        exclude: ^reports/
      - id: check-yaml
      - id: check-toml
      - id: check-json
      - id: check-merge-conflict
      - id: check-added-large-files
        args: ['--maxkb=1000']

  # Ruff linter and formatter
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.14
    hooks:
      # Run the formatter first
      - id: ruff-format
        types_or: [python, pyi]
      # Then run the linter
      - id: ruff
        types_or: [python, pyi]
        args: [--fix, --exit-non-zero-on-fix]

  # Type checking with mypy
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        name: mypy
        entry: mypy
        language: system  # Use locally installed mypy
        types: [python]
        require_serial: true
        pass_filenames: false
        args: [src/sparsetag.py, src/cache_manager.py, src/exceptions.py]
        additional_dependencies: []

  # Run pytest with coverage
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        types: [python]
        pass_filenames: false
        always_run: true
        args: [tests/, --cov=src, --cov-report=term-missing, --cov-fail-under=85, -v]
```

**Hook Execution Order:**
1. File cleanup (whitespace, EOF)
2. File validation (YAML, TOML, JSON)
3. Ruff format (auto-format code)
4. Ruff check (lint with auto-fix)
5. Mypy (type checking)
6. Pytest (tests + coverage)

**Why this order:**
- Format before lint (avoid format-then-lint loops)
- Type check after format/lint (cleaner code)
- Tests last (slowest check)

### Phase 4: Create GitHub Actions Workflow

**File: `.github/workflows/ci.yml`** (NEW)

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  quality:
    name: Code Quality
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: 'pip'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements-dev.txt

      - name: Lint with ruff
        run: |
          ruff check src/ tests/

      - name: Check formatting with ruff
        run: |
          ruff format --check src/ tests/

      - name: Type check with mypy
        run: |
          mypy src/sparsetag.py src/cache_manager.py src/exceptions.py

  test:
    name: Test Python ${{ matrix.python-version }} on ${{ matrix.os }}
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest]
        python-version: ["3.9", "3.10", "3.11", "3.12", "3.13"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements-dev.txt

      - name: Test with pytest
        run: |
          pytest tests/ --cov=src --cov-report=xml --cov-report=term-missing --cov-fail-under=85 -v

      - name: Upload coverage to Codecov
        if: matrix.os == 'ubuntu-latest' && matrix.python-version == '3.11'
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          file: ./coverage.xml
          fail_ci_if_error: true
          verbose: true
```

**Why this workflow:**
- **Two jobs**: Quality checks (fast) run separately from tests (slow matrix)
- **Matrix**: Tests on Python 3.9-3.13, Ubuntu + Windows (matches real usage)
- **fail-fast: false**: Test all versions even if one fails
- **Coverage upload**: Only from one matrix combination (avoid duplicates)
- **Caching**: pip cache speeds up dependency installation

### Phase 5: Create Codecov Configuration

**File: `.codecov.yml`** (NEW)

```yaml
coverage:
  status:
    project:
      default:
        target: 85%  # Match pytest --cov-fail-under
        threshold: 1%  # Allow 1% decrease
        if_ci_failed: error

    patch:
      default:
        target: 85%  # New code should also be 85%+
        threshold: 5%

comment:
  layout: "reach,diff,flags,tree"
  behavior: default
  require_changes: true
  require_base: false
  require_head: true

ignore:
  - "tests/*"  # Don't track coverage of tests themselves
  - "src/benchmark.py"  # Benchmark script not critical

github_checks:
  annotations: true
```

**Why this config:**
- **Project target: 85%**: Matches existing coverage requirement
- **Threshold: 1%**: Allow minor fluctuations
- **Patch target: 85%**: New code must maintain coverage
- **Comments**: Show coverage changes on PRs
- **Ignore**: Don't count test files in coverage

### Phase 6: Update CONTRIBUTING.md

**File: `CONTRIBUTING.md`**

Add after "Install dev dependencies" section (around line 20):

```markdown
6. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

   This will automatically run quality checks before each commit:
   - Ruff formatting and linting
   - Mypy type checking
   - Pytest tests with coverage

   To run checks manually without committing:
   ```bash
   pre-commit run --all-files
   ```

   To skip pre-commit hooks (not recommended):
   ```bash
   git commit --no-verify
   ```
```

Update "Ensure quality checks pass" section (around line 140):

```markdown
3. Ensure quality checks pass:

   Pre-commit hooks will run automatically, but you can also run manually:

   ```bash
   # Run all pre-commit checks
   pre-commit run --all-files

   # Or run individual tools
   ruff check src/ tests/        # Linting
   ruff format src/ tests/        # Formatting
   mypy src/                      # Type checking
   pytest tests/ --cov=src        # Tests + coverage
   ```

   All checks must pass before merging.
```

### Phase 7: Update README.md

**File: `README.md`**

Add badges at the top (after the title, before description):

```markdown
# SparseTag v2.4.0

![CI Status](https://github.com/your-org/sparsetagging/workflows/CI/badge.svg)
![Coverage](https://codecov.io/gh/your-org/sparsetagging/branch/main/graph/badge.svg)
![Python Versions](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

High-performance sparse array library for tag confidence data with intelligent query caching.
```

Add a "Development" section before "License":

```markdown
## Development

This project uses modern DevOps practices:

- **Testing**: pytest with ≥85% coverage requirement
- **Type Safety**: mypy with strict mode, 100% type hint coverage
- **Code Quality**: ruff for linting and formatting
- **Pre-commit**: Automated quality checks before commit
- **CI/CD**: GitHub Actions testing on Python 3.9-3.13

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup.
```

### Phase 8: Create DevOps Documentation

**File: `docs/DEVOPS.md`** (NEW)

[Note: Content truncated for brevity - full DevOps documentation included in original plan]

## Migration Steps

### Step 1: Audit Current Code

Before enabling tools, check what needs fixing:

```bash
# Install ruff
pip install ruff

# Check for issues (don't fix yet)
ruff check src/ tests/ --preview

# Check formatting differences
ruff format --check src/ tests/
```

If there are many issues, consider:
- Fix critical issues first (undefined names, unused imports)
- Gradually enable more rules
- Use `# noqa: <code>` for intentional exceptions

### Step 2: Add Configuration Files

1. Add ruff config to `pyproject.toml`
2. Create `.pre-commit-config.yaml`
3. Create `.github/workflows/ci.yml`
4. Create `.codecov.yml`
5. Update `requirements-dev.txt`

### Step 3: Run Auto-fixes

```bash
# Auto-fix what can be fixed
ruff check --fix src/ tests/

# Format code
ruff format src/ tests/

# Verify tests still pass
pytest tests/
```

### Step 4: Install Pre-commit

```bash
pip install pre-commit
pre-commit install

# Test on all files
pre-commit run --all-files
```

Fix any issues that arise.

### Step 5: Setup GitHub Actions

1. Create `.github/workflows/` directory
2. Add `ci.yml` workflow
3. Push to GitHub
4. Verify workflow runs

### Step 6: Setup Codecov

1. Sign up at codecov.io
2. Connect GitHub repository
3. Add `CODECOV_TOKEN` to GitHub Secrets
4. Push to trigger coverage upload
5. Add badge to README.md

### Step 7: Update Documentation

1. Update CONTRIBUTING.md with pre-commit instructions
2. Update README.md with badges
3. Create docs/DEVOPS.md
4. Commit all changes

## Verification

After setup:

```bash
# 1. Pre-commit works
pre-commit run --all-files
# Should pass all checks

# 2. Local tests pass
pytest tests/ --cov=src --cov-fail-under=85
# Should show ≥85% coverage

# 3. Type checking passes
mypy src/
# Should show no errors

# 4. Linting passes
ruff check src/ tests/
# Should show no violations

# 5. Formatting is correct
ruff format --check src/ tests/
# Should show no changes needed

# 6. CI works
git push origin main
# Check GitHub Actions tab
```

## Critical Files

Files that will be created:
- `.pre-commit-config.yaml` - Pre-commit configuration
- `.github/workflows/ci.yml` - GitHub Actions CI/CD
- `.codecov.yml` - Codecov configuration
- `docs/DEVOPS.md` - This documentation

Files that will be modified:
- `pyproject.toml` - Add ruff configuration
- `requirements-dev.txt` - Add ruff, pre-commit
- `CONTRIBUTING.md` - Add pre-commit instructions
- `README.md` - Add badges and development section

## Risks and Considerations

### Risk 1: Ruff may suggest many changes
**Mitigation**:
- Start with auto-fix enabled rules only
- Review changes carefully
- Add exceptions to config if needed

### Risk 2: Pre-commit hooks slow down commits
**Mitigation**:
- Hooks run in ~5-10 seconds (173 tests)
- Can skip with `--no-verify` for WIP
- Benefits outweigh cost (catch issues early)

### Risk 3: CI matrix is large (10 combinations)
**Mitigation**:
- Uses GitHub Actions free tier (2000 min/month)
- Caching speeds up runs
- Can reduce matrix if needed

### Risk 4: Codecov requires token
**Mitigation**:
- Free for open source
- Token stored in GitHub Secrets
- Fallback: local coverage only

### Risk 5: Breaking existing workflows
**Mitigation**:
- All existing commands still work
- Pre-commit is additive (optional)
- CI doesn't affect local development
- Can disable tools individually if needed

---

## Plan 4: humming-splashing-locket.md
**Date:** 2026-01-11
**Status:** Completed
**Related Sessions:** SESSION-SparseTagging-2026-01-11
**Summary:** Simplify Session Documentation with Command-Based Trigger - Created /document-session slash command with automated file appending, thread-based aggregation, and date-only SESSION-IDs

# Plan: Simplify Session Documentation with Command-Based Trigger

## User Requirements (Clarified)

1. **Session = One Claude Code conversation** (even if spans multiple days)
2. **SESSION-ID date = chronological ordering only** (not precise timestamps)
3. **Purpose: Retrospectives & training**, not complete history
4. **Simple command to trigger capture** (not manual copy/paste)
5. **Works for both current and old/resumed sessions**

## Phase 1: Understanding Current State ✓

**Findings:**
- Slash commands = `.md` files in `.claude/commands/` directory
- File naming: `{command-name}.md` (e.g., `document-session.md`)
- When user types `/document-session`, Claude expands the file content as a prompt
- No `.claude/commands/` directory exists yet in SparseTagging project
- Current templates already exist in `.claude/` directory

## Phase 2: Simplified Design

### Key Simplifications

1. **SESSION-ID Format:** `SESSION-ProjectName-YYYY-MM-DD` (date only, no time)
   - Date = today's date (for chronological ordering)
   - Same ID if documented same day (acceptable)
   - No need for HH-MM precision

2. **Single Command:** `/document-session`
   - Works for current session: Uses today's date
   - Works for old/resumed session: Uses today's date (ordering purpose)
   - No distinction needed between current vs old

3. **Remove Complexity:**
   - No `start-session.sh` script needed
   - No `current_session_id.txt` file
   - No timestamp estimation logic
   - No multi-day session splitting

### Implementation Approach

**Create:** `.claude/commands/document-session.md`

**Content:** Extraction prompt that:
1. Auto-generates SESSION-ID from today's date
2. Identifies conversation threads
3. Outputs 3 sections for copy/paste

**User Workflow:**
1. At end of session: Type `/document-session`
2. Copy 3 outputs to respective .md files
3. Done (30 seconds)

## Phase 3: Review and Questions ✓

**User Confirmed:**
- ✅ Same SESSION-ID for same-day sessions is acceptable
- ✅ Remove EXTRACTION_PROMPT.md entirely (slash command replaces it)
- ✅ Delete start-session.sh and start-session.bat scripts

## Phase 4: Final Implementation Plan

### Files to Create

**1. `.claude/commands/document-session.md`**
- Contains the extraction prompt
- Auto-generates SESSION-ID: `SESSION-{ProjectName}-{Today's-Date}`
- Identifies conversation threads per existing criteria
- Outputs 3 sections for copy/paste to documentation files

### Files to Update

**2. `SUMMARY_SESSION.md`**
- Change SESSION-ID format from `SESSION-[PROJECTNAME]-[YYYY-MM-DD-HH-MM]` to `SESSION-[PROJECTNAME]-[YYYY-MM-DD]`
- Remove time component from Date/Time field
- Simplify to: `Date: [YYYY-MM-DD]`

**3. `KEY_PROMPTS_AND_PLANS.md`**
- Update Ref format to match new SESSION-ID (date only)
- No other changes (thread-based aggregation criteria remain)

**4. `OTHER_SESSION_NOTES.md`**
- Update Ref format to match new SESSION-ID (date only)
- No other changes

**5. `QUICK_REFERENCE.md`**
- Rewrite workflow section to use `/document-session` command
- Remove references to start-session scripts
- Remove references to EXTRACTION_PROMPT.md
- Simplify to single-command workflow

### Files to Delete

**6. `EXTRACTION_PROMPT.md`** - Replaced by slash command
**7. `start-session.sh`** - No longer needed
**8. `start-session.bat`** - No longer needed
**9. `.claude/current_session_id.txt`** - No longer generated

### Implementation Details

**Slash Command Content (`document-session.md`):**

```markdown
Analyze this Claude Code session and generate documentation entries.

**Auto-generate SESSION-ID from:**
- Project name: [Extract via: basename $(git rev-parse --show-toplevel) or basename $(pwd)]
- Today's date: [YYYY-MM-DD format]
- Format: SESSION-{ProjectName}-{YYYY-MM-DD}

**Identify conversation THREADS:**
- Aggregate related exchanges into ONE entry per thread
- Thread boundaries = topic changes (resolved → new item, planning → implementation)
- Restate threads as complete synthesized prompts (not fragments)

**Inclusion criteria:**
- Show iterative refinement through back-and-forth
- Result in significant decisions (architecture, strategy, design)
- Demonstrate problem-solving: problem → exploration → solution
- Contain substantial user input (2+ lines with meaningful content)

**Exclude:**
- 1-line simple commands
- Pasted debug output
- Simplistic multi-line tasks without design decisions

**Generate 3 outputs for copy/paste:**

1. SUMMARY_SESSION.md entry
2. KEY_PROMPTS_AND_PLANS.md entries (or "None")
3. OTHER_SESSION_NOTES.md entry (or "None")

[Full template sections with proper formatting...]
```

### Critical Files Summary

**Create:**
- `.claude/commands/document-session.md` (new slash command)

**Update:**
- `.claude/SUMMARY_SESSION.md` (SESSION-ID format)
- `.claude/KEY_PROMPTS_AND_PLANS.md` (Ref format)
- `.claude/OTHER_SESSION_NOTES.md` (Ref format)
- `.claude/QUICK_REFERENCE.md` (workflow instructions)

**Delete:**
- `.claude/EXTRACTION_PROMPT.md`
- `.claude/start-session.sh`
- `.claude/start-session.bat`

### Expected Outcome

**Before:**
1. Run start-session.sh at beginning
2. At end: Copy EXTRACTION_PROMPT.md content
3. Paste into Claude Code
4. Copy 3 outputs to files
5. Total time: 2-3 minutes

**After:**
1. At end: Type `/document-session`
2. Copy 3 outputs to files
3. Total time: 30 seconds

**Benefits:**
- Simpler SESSION-ID (just date for ordering)
- Single command interface
- Works same way for current and old sessions
- No pre-session setup required
- Cleaner file structure

---

**End of Development Plans Archive**
