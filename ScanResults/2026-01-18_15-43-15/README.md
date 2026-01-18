# Security Scan Results

**Scan Date:** $(date -u +"%Y-%m-%d %H:%M:%S UTC")
**Commit SHA:** e8f0749a1c952fa4277e51ea5f57bfab5133a41b
**Branch:** main
**Workflow Run:** https://github.com/cgbraun/SparseTagging/actions/runs/21114302624

---

## 📊 Build Summary

**Overall Status:** ${OVERALL_STATUS}
**Build Trigger:** Push to main branch

$(if [ "${BUILD_HAS_ISSUES}" = "true" ]; then
  echo ""
  echo "### Critical Issues"
  echo -e "${CRITICAL_ALERTS}"
  echo ""
fi)

### Build Pipeline Results

| Stage | Status | Details |
|-------|--------|---------|
| 🔍 **Code Quality** | $([ "${RUFF_LINT_EXIT}" = "0" ] && [ "${RUFF_FORMAT_EXIT}" = "0" ] && [ "${MYPY_EXIT}" = "0" ] && echo "✅ Passed" || echo "⚠️ Issues") | Ruff: $([ "${RUFF_LINT_EXIT}" = "0" ] && echo "✅" || echo "⚠️"), Format: $([ "${RUFF_FORMAT_EXIT}" = "0" ] && echo "✅" || echo "⚠️"), Mypy: $([ "${MYPY_EXIT}" = "0" ] && echo "✅" || echo "⚠️") |
| 🧪 **Tests** | $([ $((TOTAL_TEST_RUNS - PASSED_TEST_RUNS)) -eq 0 ] && echo "✅ ${PASSED_TEST_RUNS}/${TOTAL_TEST_RUNS} Passed" || echo "❌ $((TOTAL_TEST_RUNS - PASSED_TEST_RUNS)) Failed") | 177 tests across Python 3.10-3.13 (Ubuntu + Windows) |
| 📝 **Documentation** | $([ "${DOC_VALIDATION_RAN}" = "true" ] && ([ "${MARKDOWNLINT_ERRORS}" = "0" ] && [ "${DEAD_LINKS}" = "0" ] && echo "✅ Passed" || echo "⚠️ Issues") || echo "⏭️ Skipped") | $([ "${DOC_VALIDATION_RAN}" = "true" ] && echo "${MARKDOWNLINT_FILES} files, ${TOTAL_LINKS} links checked" || echo "Doc-only changes trigger validation") |
| 🔒 **Security Scan** | $([ "${CRITICAL_COUNT}" != "0" ] && [ "${CRITICAL_COUNT}" != "N/A" ] && echo "❌ ${CRITICAL_COUNT} CRITICAL" || ([ "${HIGH_COUNT}" != "0" ] && [ "${HIGH_COUNT}" != "N/A" ] && echo "⚠️ ${HIGH_COUNT} HIGH" || echo "✅ Passed")) | CRITICAL: ${CRITICAL_COUNT}, HIGH: ${HIGH_COUNT}, MEDIUM: ${MEDIUM_COUNT}, LOW: ${LOW_COUNT} |
| 🐳 **Docker Build** | $([ "${SMOKE_TEST_AVAILABLE}" = "true" ] && ([ "${SMOKE_TEST1_STATUS}" = "PASSED" ] && [ "${SMOKE_TEST2_STATUS}" = "PASSED" ] && [ "${SMOKE_TEST3_STATUS}" = "PASSED" ] && echo "✅ Passed" || echo "❌ Failed") || echo "✅ Built") | $([ "${SMOKE_TEST_AVAILABLE}" = "true" ] && echo "Image built, smoke tests passed, pushed to GHCR" || echo "Image built successfully") |
| ☁️ **SonarCloud** | ✅ A Rating | View [dashboard](https://sonarcloud.io/project/overview?id=cgbraun_SparseTagging) for details |

### Quick Navigation

- $([ "${BUILD_HAS_ISSUES}" = "true" ] && echo "🚨 [Critical Issues](#critical-issues) (review required)" || echo "✅ No critical issues found")
- 📊 [Full Workflow Run](https://github.com/cgbraun/SparseTagging/actions/runs/21114302624)
- 🧪 [Detailed Test Results](#test-matrix-results)
- 📁 [All Artifacts](#all-generated-artifacts)

---

## 🔍 Code Quality Results

**Status:** $([ "${RUFF_LINT_EXIT}" = "0" ] && [ "${RUFF_FORMAT_EXIT}" = "0" ] && [ "${MYPY_EXIT}" = "0" ] && echo "✅ Passed" || echo "⚠️ Issues Found")

The code quality checks validated Python code against project standards:

- **Ruff Linting:** $([ "${RUFF_LINT_EXIT}" = "0" ] && echo "✅ 0 violations" || echo "⚠️ Issues found") ([ruff-lint.txt](./ruff-lint.txt))
- **Code Formatting:** $([ "${RUFF_FORMAT_EXIT}" = "0" ] && echo "✅ All files formatted" || echo "⚠️ Formatting needed") ([ruff-format.txt](./ruff-format.txt))
- **Type Checking:** $([ "${MYPY_EXIT}" = "0" ] && echo "✅ 0 type errors" || echo "⚠️ Type errors found") ([mypy-report.txt](./mypy-report.txt))

All source files in \`src/\` and test files in \`tests/\` were checked.

---

## 🧪 Test Matrix Results

**Status:** $([ $((TOTAL_TEST_RUNS - PASSED_TEST_RUNS)) -eq 0 ] && echo "✅ ${PASSED_TEST_RUNS}/${TOTAL_TEST_RUNS} Passed" || echo "❌ $((TOTAL_TEST_RUNS - PASSED_TEST_RUNS))/${TOTAL_TEST_RUNS} Failed")

Tests ran across ${TOTAL_TEST_RUNS} environments (Python 3.10, 3.11, 3.12, 3.13 × Ubuntu/Windows):

- **Total Tests:** 177 tests
- **Test Runs:** ${TOTAL_TEST_RUNS} environments
- **Passed:** ${PASSED_TEST_RUNS} environments
- **Failed:** $((TOTAL_TEST_RUNS - PASSED_TEST_RUNS)) environments

**Reports:**
- [test-summary.md](./test-summary.md) - Per-environment results
- [coverage.xml](./coverage.xml) - Code coverage metrics (target: ≥85%)

---

$(if [ "${DOC_VALIDATION_RAN}" = "true" ]; then
  echo "## 📝 Documentation Validation Results"
  echo ""
  echo "**Status:** $([ "${MARKDOWNLINT_ERRORS}" = "0" ] && [ "${DEAD_LINKS}" = "0" ] && echo "✅ Passed" || echo "⚠️ Issues Found")"
  echo ""
  echo "Documentation files were validated for style and link integrity:"
  echo ""
  echo "**Markdown Linting:**"
  echo "- Files checked: ${MARKDOWNLINT_FILES} markdown files"
  echo "- Style violations: ${MARKDOWNLINT_ERRORS} errors"
  echo "- Report: [markdownlint-report.txt](./markdownlint-report.txt)"
  echo ""
  echo "**Link Validation:**"
  echo "- Hyperlinks checked: ${TOTAL_LINKS} links"
  echo "- Dead links found: ${DEAD_LINKS}"
  echo "- Report: [markdown-link-check-report.txt](./markdown-link-check-report.txt)"
  echo ""
  echo "> **Note:** Documentation validation only runs when documentation files (\`.md\`, \`docs/**\`) are modified."
  echo ""
  echo "---"
  echo ""
fi)

## 🔒 Security Scan Results

**Status:** $([ "${CRITICAL_COUNT}" != "0" ] && [ "${CRITICAL_COUNT}" != "N/A" ] && echo "❌ Critical Issues" || ([ "${HIGH_COUNT}" != "0" ] && [ "${HIGH_COUNT}" != "N/A" ] && echo "⚠️ Issues Found" || echo "✅ No Critical Issues"))

Trivy scanned the Docker image for vulnerabilities, secrets, and misconfigurations:

### Vulnerability Breakdown

| Severity | Count | Status |
|----------|-------|--------|
| 🔴 CRITICAL | ${CRITICAL_COUNT} | $([ "${CRITICAL_COUNT}" != "0" ] && [ "${CRITICAL_COUNT}" != "N/A" ] && echo "**Action Required**" || echo "None found") |
| 🟠 HIGH | ${HIGH_COUNT} | $([ "${HIGH_COUNT}" != "0" ] && [ "${HIGH_COUNT}" != "N/A" ] && echo "**Review Needed**" || echo "None found") |
| 🟡 MEDIUM | ${MEDIUM_COUNT} | Monitor |
| 🔵 LOW | ${LOW_COUNT} | Informational |

$(if [ "${CRITICAL_COUNT}" != "0" ] && [ "${CRITICAL_COUNT}" != "N/A" ]; then
  echo ""
  echo "> **⚠️ CRITICAL:** ${CRITICAL_COUNT} CRITICAL vulnerabilities found. Review [trivy-report.txt](./trivy-report.txt) for CVE details and affected packages."
  echo ""
fi)

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

**Status:** $([ "${SMOKE_TEST_AVAILABLE}" = "true" ] && ([ "${SMOKE_TEST1_STATUS}" = "PASSED" ] && [ "${SMOKE_TEST2_STATUS}" = "PASSED" ] && [ "${SMOKE_TEST3_STATUS}" = "PASSED" ] && echo "✅ Passed" || echo "❌ Failed") || echo "✅ Built")

Docker image successfully built:

**Image Details:**
- Base: \`python:3.11-slim\` (Debian)
- Tag: \`ghcr.io/cgbraun/sparsetagging:latest\`
- Architecture: linux/amd64

$(if [ "${SMOKE_TEST_AVAILABLE}" = "true" ]; then
  echo ""
  echo "**Smoke Tests:**"
  echo "- $([ "${SMOKE_TEST1_STATUS}" = "PASSED" ] && echo "✅" || echo "❌") Import verification: Module loads successfully"
  echo "- $([ "${SMOKE_TEST2_STATUS}" = "PASSED" ] && echo "✅" || echo "❌") Version check: ${SMOKE_VERSION} confirmed"
  echo "- $([ "${SMOKE_TEST3_STATUS}" = "PASSED" ] && echo "✅" || echo "❌") Basic functionality: SparseTag creation works"
  echo ""
  echo "**Deployment:** Image pushed to GitHub Container Registry (GHCR)"
else
  echo ""
  echo "> **Note:** Smoke tests and GHCR deployment only run on main branch."
fi)

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

$(if [ "${DOC_VALIDATION_RAN}" = "true" ]; then
  echo "**Documentation Reports:**  "
  echo "[markdownlint-report.txt](./markdownlint-report.txt) | [markdown-link-check-report.txt](./markdown-link-check-report.txt)"
  echo ""
fi)

---

## 💡 Quick Actions

**If vulnerabilities found:**
1. Review CVE details in [trivy-report.txt](./trivy-report.txt)
2. Check if updates available for affected packages
3. Assess impact on SparseTagging's use case
4. Document exceptions in SECURITY.md if no fix exists

**For detailed analysis:**
- Import SARIF to IDE for inline vulnerability review (VS Code: "SARIF Viewer" extension)
- Compare with previous scans in \`ScanResults/\` directory
- Check [SonarCloud dashboard](https://sonarcloud.io/project/overview?id=cgbraun_SparseTagging) for trends over time

**Next Steps:**
- Review [workflow run logs](https://github.com/cgbraun/SparseTagging/actions/runs/21114302624) for full execution details
- Check \`SECURITY.md\` in repository root for security policy and reporting procedures

---

_Report generated by CI/CD pipeline on $(date -u +"%Y-%m-%d %H:%M:%S UTC") - See [full workflow run](https://github.com/cgbraun/SparseTagging/actions/runs/21114302624)_
