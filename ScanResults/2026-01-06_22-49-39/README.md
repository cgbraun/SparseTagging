# Security Scan Results

**Scan Date:** 2026-01-06 22:49:39 UTC
**Commit SHA:** 3e1a96b229398c80d5a04cd6b08aae4d95120f23
**Branch:** main
**Workflow Run:** https://github.com/cgbraun/SparseTagging/actions/runs/20764494960

## Quick Links

- 🔒 **[SonarCloud Security Vulnerabilities](https://sonarcloud.io/project/issues?id=cgbraun_SparseTagging&resolved=false&types=VULNERABILITY)**
- 📊 **[SonarCloud Dashboard](https://sonarcloud.io/project/overview?id=cgbraun_SparseTagging)**
- 📈 **[Code Coverage Report](https://sonarcloud.io/component_measures?id=cgbraun_SparseTagging&metric=coverage&view=list)**

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
- **Format:** Cobertura XML
- **Purpose:** Code coverage metrics from pytest
- **Usage:** Import into IDEs, coverage visualization tools
- **Contains:** Line-by-line coverage data for all source files

### 5. 
- **Format:** Markdown summary report
- **Purpose:** Consolidated test results from all Python versions and platforms
- **Contains:** Pass/fail status for Python 3.10-3.13 on Ubuntu and Windows

### 6. 
- **Format:** Plain text
- **Purpose:** Linting results from ruff
- **Contains:** Code style violations, unused imports, complexity issues

### 7. 
- **Format:** Plain text
- **Purpose:** Code formatting check results
- **Contains:** Files that need formatting, formatting violations

### 8. 
- **Format:** Plain text
- **Purpose:** Static type checking results
- **Contains:** Type errors, missing annotations, type mismatches

---

## SonarCloud Code Quality & Security Analysis

**Project:** SparseTagging
**Commit:** 3e1a96b229398c80d5a04cd6b08aae4d95120f23
**Branch:** main

### Security Analysis

- 🔒 **[Security Vulnerabilities](https://sonarcloud.io/project/issues?id=cgbraun_SparseTagging&resolved=false&types=VULNERABILITY)** - View all unresolved security vulnerabilities
- ⚠️ **[Security Hotspots](https://sonarcloud.io/project/security_hotspots?id=cgbraun_SparseTagging)** - Security-sensitive code requiring review
- 🛡️ **[Security Review Rating](https://sonarcloud.io/component_measures?id=cgbraun_SparseTagging&metric=security_review_rating)** - Overall security review status

### Code Quality Analysis

- 🐛 **[Bugs](https://sonarcloud.io/project/issues?id=cgbraun_SparseTagging&resolved=false&types=BUG)** - Identified bugs in the codebase
- 💡 **[Code Smells](https://sonarcloud.io/project/issues?id=cgbraun_SparseTagging&resolved=false&types=CODE_SMELL)** - Maintainability issues
- 📊 **[Project Dashboard](https://sonarcloud.io/project/overview?id=cgbraun_SparseTagging)** - Complete overview with quality gate status
- 📈 **[Code Coverage](https://sonarcloud.io/component_measures?id=cgbraun_SparseTagging&metric=coverage&view=list)** - Line and branch coverage details
- 🔍 **[This Commit](https://sonarcloud.io/project/overview?id=cgbraun_SparseTagging&branch=main)** - Analysis for this specific commit

### Key Metrics

View the SonarCloud dashboard for:
- **Security Rating** (A-E scale)
- **Reliability Rating** (bug density)
- **Maintainability Rating** (technical debt)
- **Code Coverage** (target: ≥85%)
- **Code Duplication** (target: <3%)
- **Cognitive Complexity** (target: ≤15 per function)

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
