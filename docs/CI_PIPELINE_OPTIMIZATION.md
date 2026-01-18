# CI/CD Pipeline Optimization for Documentation Changes

## Overview

The SparseTagging CI/CD pipeline has been optimized to intelligently skip expensive compute jobs when only documentation files change. This reduces CI execution time by ~97% (from 25 minutes to 45 seconds) for documentation-only commits.

**Implementation Date:** 2026-01-18
**Status:** Active
**GitHub Actions Workflow:** `.github/workflows/ci.yml`

---

## Execution Strategies

The pipeline uses path-based filtering to determine which jobs to run based on what files changed.

### Strategy 1: Documentation-Only Changes

**Triggers when ONLY these files change:**
- `docs/**` - Documentation files
- `*.md` - Markdown files in root
- `.claude/**` - Claude Code project files
- `tools/diagram-converter/**` - Documentation tooling
- `ScanResults/**` - Auto-generated scan results

**Jobs that run:**
- `detect-changes` (~5s) - Determines what changed
- `service-health-check` (~5s) - Checks external services
- `doc-validation` (~30-45s) - Lints markdown and checks links

**Jobs that are skipped:**
- `quality` - Code quality checks (ruff, mypy)
- `sonarcloud` - SonarCloud analysis
- `test` - 8 parallel test matrix jobs (Python 3.10-3.13 × Ubuntu/Windows)
- `docker-build-scan` - Docker build and security scanning

**Total execution time:** ~45 seconds (vs. 25 minutes for full pipeline)
**Compute savings:** 97%

### Strategy 2: Code Changes

**Triggers when ANY of these files change:**
- `src/**` - Source code
- `tests/**` - Test files
- `requirements*.txt` - Python dependencies
- `pyproject.toml` - Project metadata
- `Dockerfile` - Docker image definition
- `mypy.ini` - Type checking configuration
- `.ruff.toml` - Linting configuration
- `.pre-commit-config.yaml` - Pre-commit hooks
- `sonar-project.properties` - SonarCloud configuration
- `.github/workflows/**` - CI/CD workflows

**Jobs that run:**
- All jobs (full pipeline)

**Total execution time:** ~25 minutes
**Behavior:** Same as before optimization

### Strategy 3: Mixed Changes (Code + Docs)

**Triggers when:**
- Both code and documentation files change in the same commit/PR

**Jobs that run:**
- All jobs (full pipeline including doc-validation)

**Total execution time:** ~25.5 minutes
**Overhead:** Negligible (~30 seconds for doc validation)

---

## Path Filter Categories

The `detect-changes` job uses `dorny/paths-filter@v3.0.2` to categorize file changes:

### Filter: `code`
```yaml
code:
  - 'src/**'
  - 'tests/**'
  - 'requirements*.txt'
  - 'pyproject.toml'
  - 'Dockerfile'
```

**Rationale:** Changes to source code, tests, or dependencies require full testing and validation.

### Filter: `docs`
```yaml
docs:
  - 'docs/**'
  - '*.md'
  - '.claude/**'
  - 'tools/diagram-converter/**'
```

**Rationale:** Documentation changes don't affect runtime behavior and can be validated separately.

### Filter: `config`
```yaml
config:
  - 'mypy.ini'
  - '.ruff.toml'
  - '.pre-commit-config.yaml'
  - 'sonar-project.properties'
```

**Rationale:** Configuration changes affect quality gates and need full validation.

### Filter: `workflows`
```yaml
workflows:
  - '.github/workflows/**'
```

**Rationale:** Workflow changes should be tested with the full pipeline to ensure CI/CD works correctly.

### Filter: `scan_results`
```yaml
scan_results:
  - 'ScanResults/**'
```

**Rationale:** Auto-generated scan results are informational and don't require any validation.

---

## Job Execution Logic

### Conditional Execution

All heavy jobs use this condition:
```yaml
if: needs.detect-changes.outputs.code == 'true' || needs.detect-changes.outputs.config == 'true' || needs.detect-changes.outputs.workflows == 'true'
```

This means:
- Run if code changed
- Run if config changed
- Run if workflows changed
- Skip if only docs or scan results changed

### Documentation Validation

The `doc-validation` job uses:
```yaml
if: needs.detect-changes.outputs.docs == 'true'
```

This means:
- Run if any documentation files changed
- Skip if only code or config changed

### Always-On Jobs

The `service-health-check` job runs unconditionally:
- No `needs` or `if` conditions
- Provides informational health status
- Fast execution (~5 seconds)

---

## Documentation Validation Tools

### Markdownlint (`markdownlint-cli2`)

**Version:** 0.12.1 (pinned)
**Purpose:** Lints markdown files for style consistency
**Configuration:** `.markdownlint.yaml`

**Rules enforced:**
- Heading hierarchy (MD001, MD003)
- List formatting (MD004, MD005, MD006, MD007, MD029, MD030, MD032)
- Emphasis style (MD036, MD037)
- Code block style (MD046, MD048)
- Whitespace (MD009, MD010, MD012, MD018, MD019, MD022, MD023, MD027, MD028, MD031)

**Rules disabled:**
- MD013 (line length) - Technical docs often have long lines
- MD033 (inline HTML) - Allowed for complex formatting
- MD034 (bare URLs) - Common in technical docs
- MD041 (first line heading) - Some files start with badges/metadata

**Output:** `markdownlint-report.txt` (uploaded as artifact)

### Markdown Link Check (`markdown-link-check`)

**Version:** 3.12.1 (pinned)
**Purpose:** Validates all hyperlinks in markdown files
**Configuration:** `.markdown-link-check.json`

**Features:**
- 10 second timeout per link
- 3 retries on failure
- Retry on HTTP 429 (rate limiting)
- Accepts status codes: 200, 206, 301, 302, 307, 308, 400, 405, 999

**Ignored patterns:**
- `http://localhost*` - Local development URLs
- `https://github.com/.*/actions/runs/*` - Ephemeral workflow URLs
- `https://sonarcloud.io/project/*` - Dynamic SonarCloud URLs

**Output:** `markdown-link-check-report.txt` (uploaded as artifact)

---

## Testing the Optimization

### Test Scenarios

Run these tests to verify path filtering works correctly:

#### Test 1: Documentation-Only Change
```bash
# Make a doc-only change
echo "test" >> docs/TEST.md
git add docs/TEST.md
git commit -m "docs: test doc-only change"
git push
```

**Expected behavior:**
- `detect-changes` outputs: `docs=true`, `code=false`, `config=false`, `workflows=false`
- Jobs run: `detect-changes`, `service-health-check`, `doc-validation`
- Jobs skipped: `quality`, `sonarcloud`, `test`, `docker-build-scan`
- Execution time: ~45 seconds

#### Test 2: Code-Only Change
```bash
# Make a code change
echo "# test comment" >> src/sparsetag.py
git add src/sparsetag.py
git commit -m "test: verify code change triggers full pipeline"
git push
```

**Expected behavior:**
- `detect-changes` outputs: `code=true`
- Jobs run: All jobs (full pipeline)
- Jobs skipped: None
- Execution time: ~25 minutes

#### Test 3: Mixed Change (Code + Docs)
```bash
# Make both code and doc changes
echo "# test" >> src/sparsetag.py
echo "test" >> docs/TEST.md
git add src/sparsetag.py docs/TEST.md
git commit -m "test: mixed code and doc change"
git push
```

**Expected behavior:**
- `detect-changes` outputs: `code=true`, `docs=true`
- Jobs run: All jobs including `doc-validation`
- Jobs skipped: None
- Execution time: ~25.5 minutes

#### Test 4: Config-Only Change
```bash
# Make a config change
echo "# test comment" >> mypy.ini
git add mypy.ini
git commit -m "test: config change triggers full pipeline"
git push
```

**Expected behavior:**
- `detect-changes` outputs: `config=true`
- Jobs run: All jobs (full pipeline)
- Jobs skipped: None
- Execution time: ~25 minutes

#### Test 5: Scan Results Cleanup
```bash
# Delete old scan results
git rm -r ScanResults/2026-01-06_*
git commit -m "chore: cleanup old scan results"
git push
```

**Expected behavior:**
- `detect-changes` outputs: `scan_results=true`, all others `false`
- Jobs run: `detect-changes`, `service-health-check`
- Jobs skipped: All validation jobs (code and docs)
- Execution time: ~10 seconds

#### Test 6: Workflow Change
```bash
# Make a workflow change
echo "# test comment" >> .github/workflows/ci.yml
git add .github/workflows/ci.yml
git commit -m "test: workflow change triggers full pipeline"
git push
```

**Expected behavior:**
- `detect-changes` outputs: `workflows=true`
- Jobs run: All jobs (full pipeline)
- Jobs skipped: None
- Execution time: ~25 minutes

### Verification Steps

For each test:

1. **Check GitHub Actions UI**
   - Go to: https://github.com/cgbraun/SparseTagging/actions
   - Click on the latest workflow run
   - Verify correct jobs executed/skipped

2. **Check detect-changes outputs**
   - Expand the `detect-changes` job
   - Look for output like:
     ```
     code: false
     docs: true
     config: false
     workflows: false
     scan_results: false
     ```

3. **Verify execution time**
   - Check total workflow duration
   - Compare against expected time

4. **Check artifacts**
   - For doc-only changes: Look for `doc-validation-reports` artifact
   - For code changes: Look for `quality-reports`, `test-results-*`, etc.

5. **Verify no failures**
   - All jobs should succeed or be skipped
   - `continue-on-error: true` jobs can fail without blocking

---

## Troubleshooting

### Issue: Jobs unexpectedly skipped

**Symptoms:**
- Code changes don't trigger full pipeline
- Doc validation doesn't run on markdown changes

**Diagnosis:**
1. Check `detect-changes` job output
2. Verify file paths match filter patterns
3. Check if `.github/workflows/ci.yml` is up to date

**Solution:**
```bash
# Verify filters are correct
git show HEAD:.github/workflows/ci.yml | grep -A 20 "dorny/paths-filter"

# Check which files changed
git diff --name-only HEAD~1

# Force re-run workflow
# Go to Actions tab → Select workflow → Re-run all jobs
```

### Issue: Doc validation fails on markdownlint

**Symptoms:**
- `doc-validation` job shows errors
- Markdownlint reports rule violations

**Diagnosis:**
1. Download `markdownlint-report.txt` artifact
2. Identify which rules are failing
3. Check if rules should be disabled for this project

**Solution:**
```bash
# Run locally to see errors
npm install -g markdownlint-cli2
markdownlint-cli2 "**/*.md"

# Fix issues or update .markdownlint.yaml to disable rule
# Example: Disable MD013 (line length)
echo "MD013: false" >> .markdownlint.yaml
```

### Issue: Link check fails on valid links

**Symptoms:**
- `markdown-link-check` reports broken links
- Links work in browser but fail in CI

**Diagnosis:**
1. Download `markdown-link-check-report.txt` artifact
2. Identify which links are failing
3. Check if links need to be ignored

**Solution:**
```bash
# Run locally to reproduce
npm install -g markdown-link-check
find . -name "*.md" | xargs -n1 markdown-link-check

# Add to .markdown-link-check.json ignore patterns
# Example: Ignore specific domain
{
  "ignorePatterns": [
    {"pattern": "^https://example.com/"}
  ]
}
```

### Issue: Node.js cache not working

**Symptoms:**
- `doc-validation` job takes longer than expected
- NPM packages reinstalled every time

**Diagnosis:**
1. Check if `package-lock.json` exists (it shouldn't for global installs)
2. Verify cache configuration in workflow

**Solution:**
```yaml
# Update doc-validation job to remove cache dependency path
- name: Set up Node.js
  uses: actions/setup-node@v4
  with:
    node-version: '20'
    # Remove this line if no package-lock.json:
    # cache-dependency-path: '**/package-lock.json'
```

### Issue: Pre-commit hook fails locally

**Symptoms:**
- `pre-commit run --all-files` fails on markdownlint
- Works in CI but not locally

**Diagnosis:**
1. Check if markdownlint-cli2 is installed globally
2. Verify Node.js is available

**Solution:**
```bash
# Install Node.js (required for markdownlint)
# Windows: Download from https://nodejs.org/
# Linux/Mac: Use nvm or package manager

# Install markdownlint-cli2
npm install -g markdownlint-cli2@0.12.1

# Update pre-commit hooks
pre-commit autoupdate
pre-commit run --all-files
```

### Issue: False negatives (code changes skipped)

**Symptoms:**
- Changed `src/sparsetag.py` but pipeline was skipped
- Code quality issues not caught

**This should NEVER happen.** If it does:

1. **Immediately investigate** - This is a critical bug
2. Check `detect-changes` filter patterns
3. Verify `dorny/paths-filter` is working correctly
4. Check workflow YAML syntax

**Emergency rollback:**
```bash
# Remove path filtering (all jobs run always)
git revert <commit-hash>
git push
```

---

## Performance Metrics

### Baseline (Before Optimization)

| Commit Type | Jobs Run | Execution Time | Parallel Runners |
|-------------|----------|----------------|------------------|
| Documentation | All (10 jobs) | ~25 minutes | 10 |
| Code | All (10 jobs) | ~25 minutes | 10 |
| Mixed | All (10 jobs) | ~25 minutes | 10 |

**Total CI minutes per day (estimated):** 250 minutes (10 commits/day × 25 min/commit)

### After Optimization

| Commit Type | Jobs Run | Execution Time | Parallel Runners | Speedup |
|-------------|----------|----------------|------------------|---------|
| Documentation | 3 jobs | ~45 seconds | 3 | **97% faster** |
| Code | All (10 jobs) | ~25 minutes | 10 | No change |
| Mixed | All (11 jobs) | ~25.5 minutes | 11 | Negligible overhead |

**Estimated commit distribution:**
- 30% documentation-only (3 commits/day)
- 50% code changes (5 commits/day)
- 20% mixed (2 commits/day)

**Total CI minutes per day (optimized):** ~177 minutes
**Daily savings:** ~73 minutes (29% reduction)
**Weekly savings:** ~511 minutes (~8.5 hours)
**Monthly savings:** ~2,190 minutes (~36.5 hours)

### Cost Savings

**GitHub Actions pricing (as of 2026):**
- Public repositories: Free unlimited minutes
- Private repositories: Included minutes vary by plan

**For private repositories on Team plan (3,000 minutes/month included):**
- Before: ~5,000 minutes/month (over limit, $0.008/min overage)
- After: ~3,540 minutes/month (within limit)
- **Monthly savings:** ~$11.68 (1,460 minutes × $0.008/min)
- **Annual savings:** ~$140

**For self-hosted runners:**
- Compute time reduction directly translates to:
  - Lower infrastructure costs
  - Reduced CI queue times
  - Faster developer feedback

---

## Future Enhancements

### Planned Improvements

1. **Caching Optimization**
   - Cache npm packages for doc-validation
   - Cache Python packages across jobs
   - **Estimated savings:** 10-15% additional speedup

2. **Parallel Link Checking**
   - Use `markdown-link-check` in parallel mode
   - Check multiple files simultaneously
   - **Estimated savings:** 30% faster doc validation

3. **Smart Retries**
   - Retry only failed jobs, not entire workflow
   - **Estimated savings:** Faster recovery from transient failures

4. **Dependabot Path Filtering**
   - Skip full pipeline for documentation-only dependency updates
   - Requires custom Dependabot configuration
   - **Estimated savings:** 5-10% additional reduction

### Not Planned (Intentionally Deferred)

1. **Retry Logic for Network Failures**
   - **Reason:** No demonstrated need, adds complexity
   - **Reconsider if:** 3+ failures/month due to network issues

2. **Granular Test Matrix Filtering**
   - Example: Skip Windows tests for Linux-only changes
   - **Reason:** Risk of false negatives, minimal benefit
   - **Reconsider if:** Test matrix grows beyond 8 jobs

---

## Maintenance

### Updating Path Filters

When adding new directories or file types:

1. **Identify category:** Is it code, docs, config, or workflows?
2. **Update filter:** Edit `.github/workflows/ci.yml` → `detect-changes` job
3. **Test:** Create test commit and verify jobs run correctly
4. **Document:** Update this file with the new pattern

**Example: Adding new config file**
```yaml
# Add to config filter in ci.yml
config:
  - 'mypy.ini'
  - '.ruff.toml'
  - '.pre-commit-config.yaml'
  - 'sonar-project.properties'
  - 'pytest.ini'  # New config file
```

### Updating Documentation Tools

To update markdownlint or markdown-link-check:

1. **Check for updates:**
   ```bash
   npm outdated -g markdownlint-cli2 markdown-link-check
   ```

2. **Update version in workflow:**
   ```yaml
   # .github/workflows/ci.yml
   - name: Install markdown tools
     run: |
       npm install -g markdownlint-cli2@0.13.0  # Update version
       npm install -g markdown-link-check@3.13.0  # Update version
   ```

3. **Update pre-commit hook:**
   ```yaml
   # .pre-commit-config.yaml
   - repo: https://github.com/DavidAnson/markdownlint-cli2
     rev: v0.13.0  # Update version
   ```

4. **Test locally:**
   ```bash
   pre-commit run --all-files
   ```

5. **Add to Dependabot monitoring:**
   ```yaml
   # .github/dependabot.yml
   - package-ecosystem: "npm"
     directory: "/"
     schedule:
       interval: "weekly"
   ```

---

## References

- **GitHub Actions Path Filter:** https://github.com/dorny/paths-filter
- **Markdownlint Rules:** https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md
- **Markdown Link Check:** https://github.com/tcort/markdown-link-check
- **SparseTagging CI Workflow:** `.github/workflows/ci.yml`
- **SparseTagging CI Philosophy:** `CLAUDE.md` → "CI/CD Pipeline" section

---

## Change Log

| Date | Change | Impact |
|------|--------|--------|
| 2026-01-18 | Initial implementation | 97% speedup for doc-only changes |

---

## Contact

For questions or issues with CI/CD optimization:

1. **Check this document** for troubleshooting steps
2. **Review workflow logs** in GitHub Actions UI
3. **File an issue** at: https://github.com/cgbraun/SparseTagging/issues
4. **Tag issue** with `ci/cd` label
