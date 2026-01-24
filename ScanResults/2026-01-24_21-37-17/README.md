# Security Scan Results

**Scan Date:** 2026-01-24 21:37:18 UTC
**Commit SHA:** c37c7c552516fa1320ad6e9a8da91c9c7c312b76
**Branch:** main
**Workflow Run:** https://github.com/cgbraun/SparseTagging/actions/runs/21321951748

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
| 🔒 **Security Scan** | ⚠️ 3 HIGH | CRITICAL: 0, HIGH: 3, MEDIUM: 4, LOW: 25 |
| 🐳 **Docker Build** | ✅ Built | Image built successfully |
| ☁️ **SonarCloud** | ✅ A Rating | View [dashboard](https://sonarcloud.io/project/overview?id=cgbraun_SparseTagging) for details |

### Quick Navigation

- ✅ No critical issues found
- 📊 [Full Workflow Run](https://github.com/cgbraun/SparseTagging/actions/runs/21321951748)
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

Tests ran across 8 environments (Python 3.10, 3.11, 3.12, 3.13 x Ubuntu/Windows):

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
| 🟠 HIGH | 3 | **Review Needed** |
| 🟡 MEDIUM | 4 | Monitor |
| 🔵 LOW | 25 | Informational |

> **📋 Documented Vulnerabilities:** 3 HIGH severity CVEs are documented as accepted risks with low practical exploitability:
> - **CVE-2026-0861** (glibc memalign): Awaiting Debian patch - See [Issue #18](https://github.com/cgbraun/SparseTagging/issues/18) | [SECURITY.md](../../../SECURITY.md#cve-2026-0861---glibc-memalign-integer-overflow)
> - **GHSA-58pv-8j8x-9vj2** (jaraco.context): Setuptools vendored dependency, not exploitable at runtime - See [Issue #19](https://github.com/cgbraun/SparseTagging/issues/19) | [SECURITY.md](../../../SECURITY.md#ghsa-58pv-8j8x-9vj2---jaracocontext-path-traversal)


**Scan Coverage:**
- Vulnerabilities: ✅ Scanned
- Secret scanning: ✅ Checked
- Misconfiguration: ✅ Analyzed

**Reports:**
- [trivy-results.sarif](./trivy-results.sarif) - Machine-readable (SARIF format for IDE import)
- [trivy-report.txt](./trivy-report.txt) - Human-readable table
- [sbom.spdx.json](./sbom.spdx.json) - Software Bill of Materials (SPDX 2.3)

---

## 📋 Documented Vulnerabilities (Accepted Risk)

**Total:** 3 HIGH severity CVEs documented with accepted risk

The following vulnerabilities have been reviewed, documented, and accepted as low practical risk:

### CVE-2026-0861 - glibc memalign Integer Overflow
- **Severity:** HIGH (CVSS 8.0)
- **Package:** glibc (libc6, libc-bin)
- **Status:** ⏳ Awaiting Debian security patch
- **Risk Level:** VERY LOW (requires precise control of size + alignment arguments)
- **Tracking:** [GitHub Issue #18](https://github.com/cgbraun/SparseTagging/issues/18)
- **Documentation:** [SECURITY.md](../../../SECURITY.md#cve-2026-0861---glibc-memalign-integer-overflow)
- **Review Schedule:** First Monday of each month (automated CI checks)

### GHSA-58pv-8j8x-9vj2 - jaraco.context Path Traversal
- **Severity:** HIGH (CVSS 8.6)
- **Package:** jaraco.context (setuptools vendored dependency)
- **Status:** ⏳ Awaiting setuptools to update vendored copy
- **Risk Level:** VERY LOW (build-time only, not accessible at runtime)
- **Tracking:** [GitHub Issue #19](https://github.com/cgbraun/SparseTagging/issues/19)
- **Documentation:** [SECURITY.md](../../../SECURITY.md#ghsa-58pv-8j8x-9vj2---jaracocontext-path-traversal)
- **Review Schedule:** First Monday of each month (automated CI checks)

> **Mitigation:** Both vulnerabilities are monitored via automated CI workflows. When patches become available, Docker images will be rebuilt and rescanned to verify resolution.

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
- Review [workflow run logs](https://github.com/cgbraun/SparseTagging/actions/runs/21321951748) for full execution details
- Check `SECURITY.md` in repository root for security policy and reporting procedures

---

_Report generated by CI/CD pipeline on 2026-01-24 21:37:18 UTC - See [full workflow run](https://github.com/cgbraun/SparseTagging/actions/runs/21321951748)_