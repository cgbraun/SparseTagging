# Security Scan Results

**Scan Date:** 2026-01-06 21:57:03 UTC
**Commit SHA:** \e1d5a04d65d98f45d1834e2c69b3c67831c3e1f7
**Branch:** \main
**Workflow Run:** https://github.com/\cgbraun/SparseTagging/actions/runs/\20763292738

---

## Vulnerability Summary (Trivy)

| Severity | Count |
|----------|-------|
| CRITICAL | 0
0 |
| HIGH     | 0
0 |
| MEDIUM   | 16 |
| LOW      | 126 |

> **Note:** Counts are approximate based on keyword matching. See  for full details.

---

## Available Files

### 1. 
- **Format:** SARIF (Static Analysis Results Interchange Format)
- **Purpose:** Machine-readable security findings
- **Usage:**
  - Import into VS Code, PyCharm, or other IDEs with SARIF support
  - Upload to GitHub Security tab (Code Scanning)
  - Process with automated security tools
- **Contains:** Vulnerabilities, secrets, misconfigurations
- **Severity Filter:** CRITICAL, HIGH only

### 2. 
- **Format:** Human-readable table
- **Purpose:** Quick visual review of all vulnerabilities
- **Usage:** Open in text editor to review findings
- **Contains:** Vulnerabilities, secrets, misconfigurations
- **Severity Filter:** CRITICAL, HIGH, MEDIUM

### 3. 
- **Format:** SPDX 2.3 JSON
- **Purpose:** Software Bill of Materials for compliance and supply chain security
- **Usage:**
  
- **Contains:** All packages, versions, licenses, dependencies

### 4. 
- **Format:** Markdown with links
- **Purpose:** Quick access to SonarCloud analysis results
- **Contains:** Links to dashboards, coverage, security hotspots

### 5. 
- **Format:** Cobertura XML
- **Purpose:** Code coverage metrics from pytest
- **Usage:** Import into IDEs, coverage visualization tools
- **Contains:** Line-by-line coverage data for all source files

### 6. 
- **Format:** Markdown summary report
- **Purpose:** Consolidated test results from all Python versions and platforms
- **Contains:** Pass/fail status for Python 3.10-3.13 on Ubuntu and Windows

### 7. 
- **Format:** Plain text
- **Purpose:** Linting results from ruff
- **Contains:** Code style violations, unused imports, complexity issues

### 8. 
- **Format:** Plain text
- **Purpose:** Code formatting check results
- **Contains:** Files that need formatting, formatting violations

### 9. 
- **Format:** Plain text
- **Purpose:** Static type checking results
- **Contains:** Type errors, missing annotations, type mismatches

---

## How to Use These Results

### Quick Security & Quality Review

1. **Security:** Check  for CRITICAL/HIGH vulnerabilities
2. **Tests:** Review  for test pass/fail status
3. **Code Quality:** Check  and  for issues
4. **Coverage:** Review  metrics (should be ≥85%)
5. **SBOM:** Review  for dependencies
6. **SonarCloud:** Click links in  for detailed analysis

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
