# Security Scan Results

**Scan Date:** 2026-01-18 20:30:50 UTC
**Commit SHA:** 6e8f84d94de0814fe68636bbe77859f2f9417db5
**Branch:** main
**Workflow Run:** https://github.com/cgbraun/SparseTagging/actions/runs/21118086535

---

## 📊 Build Summary

**Overall Status:** ✅ All Checks Passed
**Build Trigger:** Push to main branch



### Build Pipeline Results

| Stage | Status | Details |
|-------|--------|---------|
| 🔍 **Code Quality** | ✅ Passed | Ruff: ✅, Format: ✅, Mypy: ✅ |
| 🧪 **Tests** | ✅ 8/8 Passed | 177 tests across Python 3.10-3.13 (Ubuntu + Windows) |
| 📝 **Documentation** | ⏭️ Skipped | Doc-only changes trigger validation |
| 🔒 **Security Scan** | ⚠️ 2 HIGH | CRITICAL: 0, HIGH: 2, MEDIUM: 3, LOW: 25 |
| 🐳 **Docker Build** | ✅ Built | Image built successfully |
| ☁️ **SonarCloud** | ✅ A Rating | View [dashboard](https://sonarcloud.io/project/overview?id=cgbraun_SparseTagging) for details |

### Quick Navigation

- ✅ No critical issues found
- 📊 [Full Workflow Run](https://github.com/cgbraun/SparseTagging/actions/runs/21118086535)
- 🧪 [Detailed Test Results](#test-matrix-results)
- 📁 [All Artifacts](#all-generated-artifacts)

---

## 🔍 Code Quality Results

**Status:** ✅ Passed

The code quality checks validated Python code against project standards:

- **Ruff Linting:** ✅ 0 violations ([ruff-lint.txt](./ruff-lint.txt))
- **Code Formatting:** ✅ All files formatted ([ruff-format.txt](./ruff-format.txt))
- **Type Checking:** ✅ 0 type errors ([mypy-report.txt](./mypy-report.txt))

All source files in `src/` and test files in `tests/` were checked.

---

## 🧪 Test Matrix Results

**Status:** ✅ 8/8 Passed

Tests ran across 8 environments (Python 3.10, 3.11, 3.12, 3.13 × Ubuntu/Windows):

- **Total Tests:** 177 tests
- **Test Runs:** 8 environments
- **Passed:** 8 environments
- **Failed:** 0 environments

**Reports:**
- [test-summary.md](./test-summary.md) - Per-environment results
- [coverage.xml](./coverage.xml) - Code coverage metrics (target: ≥85%)

---



## 🔒 Security Scan Results

**Status:** ⚠️ Issues Found

Trivy scanned the Docker image for vulnerabilities, secrets, and misconfigurations:

### Vulnerability Breakdown

| Severity | Count | Status |
|----------|-------|--------|
| 🔴 CRITICAL | 0 | None found |
| 🟠 HIGH | 2 | **Review Needed** |
| 🟡 MEDIUM | 3 | Monitor |
| 🔵 LOW | 25 | Informational |



**Scan Coverage:**
- Vulnerabilities: ✅ Scanned
- Secret scanning: ✅ Checked
- Misconfiguration: ✅ Analyzed

**Reports:**
- [trivy-results.sarif](./trivy-results.sarif) - Machine-readable (SARIF format for IDE import)
- [trivy-report.txt](./trivy-report.txt) - Human-readable table
- [sbom.spdx.json](./sbom.spdx.json) - Software Bill of Materials (SPDX 2.3)

---

## 🐳 Docker Build Results

**Status:** ✅ Built

Docker image successfully built:

**Image Details:**
- Base: `python:3.11-slim` (Debian)
- Tag: `ghcr.io/cgbraun/sparsetagging:latest`
- Architecture: linux/amd64


> **Note:** Smoke tests and GHCR deployment only run on main branch.

---

## ☁️ SonarCloud Analysis

**Status:** ✅ A Rating

Static code analysis completed with quality metrics:

**Quick Links:**
- 🎯 [Quality Gate](https://sonarcloud.io/project/overview?id=cgbraun_SparseTagging) - Overall project health
- 🔒 [Security Vulnerabilities](https://sonarcloud.io/project/issues?id=cgbraun_SparseTagging&resolved=false&types=VULNERABILITY) - Unresolved security issues
- ⚠️ [Security Hotspots](https://sonarcloud.io/project/security_hotspots?id=cgbraun_SparseTagging) - Security-sensitive code for review
- 🐛 [Bugs & Code Smells](https://sonarcloud.io/project/issues?id=cgbraun_SparseTagging&resolved=false) - All quality issues
- 📈 [Code Coverage](https://sonarcloud.io/component_measures?id=cgbraun_SparseTagging&metric=coverage&view=list) - Line and branch coverage details

---

## 📁 All Generated Artifacts

Quick reference to all files in this scan directory:

**Quality Reports:**
[ruff-lint.txt](./ruff-lint.txt) | [ruff-format.txt](./ruff-format.txt) | [mypy-report.txt](./mypy-report.txt)

**Test Reports:**
[test-summary.md](./test-summary.md) | [coverage.xml](./coverage.xml)

**Security Reports:**
[trivy-results.sarif](./trivy-results.sarif) | [trivy-report.txt](./trivy-report.txt) | [sbom.spdx.json](./sbom.spdx.json)



---

## 💡 Quick Actions

**If vulnerabilities found:**
1. Review CVE details in [trivy-report.txt](./trivy-report.txt)
2. Check if updates available for affected packages
3. Assess impact on SparseTagging's use case
4. Document exceptions in SECURITY.md if no fix exists

**For detailed analysis:**
- Import SARIF to IDE for inline vulnerability review (VS Code: "SARIF Viewer" extension)
- Compare with previous scans in `ScanResults/` directory
- Check [SonarCloud dashboard](https://sonarcloud.io/project/overview?id=cgbraun_SparseTagging) for trends over time

**Next Steps:**
- Review [workflow run logs](https://github.com/cgbraun/SparseTagging/actions/runs/21118086535) for full execution details
- Check `SECURITY.md` in repository root for security policy and reporting procedures

---

_Report generated by CI/CD pipeline on 2026-01-18 20:30:50 UTC - See [full workflow run](https://github.com/cgbraun/SparseTagging/actions/runs/21118086535)_
