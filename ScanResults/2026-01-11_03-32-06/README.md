# Security Scan Results

**Scan Date:** 2026-01-11 03:32:06 UTC
**Commit SHA:** 41b79e7c269c61ba425f7b52f066d1dd9bf11cd4
**Branch:** main
**Workflow Run:** https://github.com/cgbraun/SparseTagging/actions/runs/20888785314
**SonarCloud:** https://sonarcloud.io/project/overview?id=cgbraun_SparseTagging

---

## CI Pipeline Execution Summary

### Quality Gate Results

| Check | Exit Code | Status |
|-------|-----------|--------|
| Ruff Lint | 0 | ✅ Passed |
| Ruff Format | 0 | ✅ Passed |
| Mypy Type Check | 0 | ✅ Passed |

> **Note:** Exit code 0 = passed. Non-zero = issues found. See individual report files for details.

### Test Matrix Results

- **Total Test Runs:** 8 (Python 3.10-3.13 × Ubuntu/Windows)
- **Passed:** 8
- **Failed:** 0
- **Details:** See `test-summary.md` for per-environment results

### Service Health Checks

The following external services were checked for availability:
- PyPI (package downloads)
- Docker Hub (base images)
- SonarCloud (code quality analysis)
- GitHub Container Registry (image publishing)

> **View Results:** Check [workflow run logs](https://github.com/cgbraun/SparseTagging/actions/runs/20888785314) → "Service Health Check" job


> **Note:** Docker smoke tests only run on main branch (not executed for this build).

---

## Vulnerability Summary (Trivy)

| Severity | Count |
|----------|-------|
| CRITICAL | 0 |
| HIGH     | 0 |
| MEDIUM   | 2 |
| LOW      | 25 |

> **Note:** Counts are approximate based on keyword matching. See trivy-report.txt for full details.

---

## Available Files

### 1. `trivy-results.sarif`
- **Format:** SARIF (Static Analysis Results Interchange Format)
- **Purpose:** Machine-readable security findings
- **Usage:**
  - Import into VS Code, PyCharm, or other IDEs with SARIF support
  - Upload to GitHub Security tab (Code Scanning)
  - Process with automated security tools
- **Contains:** Vulnerabilities, secrets, misconfigurations
- **Severity Filter:** CRITICAL, HIGH only

### 2. `trivy-report.txt`
- **Format:** Human-readable table
- **Purpose:** Quick visual review of all vulnerabilities
- **Usage:** Open in text editor to review findings
- **Contains:** Vulnerabilities, secrets, misconfigurations
- **Severity Filter:** CRITICAL, HIGH, MEDIUM

### 3. `sbom.spdx.json`
- **Format:** SPDX 2.3 JSON
- **Purpose:** Software Bill of Materials for compliance and supply chain security
- **Usage:**
  ```bash
  # View with Trivy
  trivy sbom sbom.spdx.json

  # Validate SPDX format
  # (requires spdx-tools: https://github.com/spdx/tools)
  java -jar spdx-tools.jar Verify sbom.spdx.json
  ```
- **Contains:** All packages, versions, licenses, dependencies


### 4. `coverage.xml`
- **Format:** Cobertura XML
- **Purpose:** Code coverage metrics from pytest
- **Usage:** Import into IDEs, coverage visualization tools
- **Contains:** Line-by-line coverage data for all source files

### 5. `test-summary.md`
- **Format:** Markdown summary report
- **Purpose:** Consolidated test results from all Python versions and platforms
- **Contains:** Pass/fail status for Python 3.10-3.13 on Ubuntu and Windows

### 6. `ruff-lint.txt`
- **Format:** Plain text
- **Purpose:** Linting results from ruff
- **Contains:** Code style violations, unused imports, complexity issues

### 7. `ruff-format.txt`
- **Format:** Plain text
- **Purpose:** Code formatting check results
- **Contains:** Files that need formatting, formatting violations

### 8. `mypy-report.txt`
- **Format:** Plain text
- **Purpose:** Static type checking results
- **Contains:** Type errors, missing annotations, type mismatches

---

## SonarCloud Code Quality & Security

**Project:** SparseTagging | **Commit:** 41b79e7c269c61ba425f7b52f066d1dd9bf11cd4 | **Branch:** main

- 🔒 **[Security Vulnerabilities](https://sonarcloud.io/project/issues?id=cgbraun_SparseTagging&resolved=false&types=VULNERABILITY)** - Unresolved security issues
- ⚠️ **[Security Hotspots](https://sonarcloud.io/project/security_hotspots?id=cgbraun_SparseTagging)** - Security-sensitive code for review
- 🐛 **[Bugs & Code Smells](https://sonarcloud.io/project/issues?id=cgbraun_SparseTagging&resolved=false)** - All quality issues
- 📈 **[Code Coverage Details](https://sonarcloud.io/component_measures?id=cgbraun_SparseTagging&metric=coverage&view=list)** - Line and branch coverage

---

## How to Use These Results

### Quick Security & Quality Review

1. **Security Vulnerabilities:** Check SonarCloud security links above + 
2. **Tests:** Review  for test pass/fail status
3. **Code Quality:** Check SonarCloud bugs/code smells +  and 
4. **Coverage:** Review  metrics (should be ≥85%)
5. **SBOM:** Review  for dependencies

### Detailed Analysis

1. **Import SARIF to IDE:**
   - VS Code: Install "SARIF Viewer" extension
   - PyCharm: Settings → Tools → SARIF → Import 

2. **GitHub Security Tab:**
   - Go to repository Security tab → Code Scanning
   - Results from SARIF upload appear here

3. **Compare with Previous Scans:**
   - Check  directory for historical scans
   - Compare vulnerability counts over time

---

## Docker Image Details

- **Base Image:** python:3.11-slim (Debian)
- **Application:** SparseTagging v2.4.1
- **Python Version:** 3.11
- **User:** sparsetag (non-root, UID 1000)
- **Architecture:** linux/amd64

---

## Next Steps

If vulnerabilities are found:

1. **Assess Impact:** Check if the CVE affects SparseTagging's use case
2. **Check for Fixes:** See if updated base images or packages are available
3. **Risk Assessment:** Document in SECURITY.md if no fix is available
4. **Patch:** Update Dockerfile or requirements.txt as needed
5. **Retest:** Push changes to trigger new security scan

For questions about these results, see  in the repository root.
