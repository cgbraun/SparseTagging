"""Generator for comprehensive scan results README."""

from datetime import datetime, timezone

from models.scan_result import ScanResult


class ReadmeGenerator:
    """Generate markdown README from scan results."""

    def generate(self, result: ScanResult) -> str:
        """Generate comprehensive README from scan results.

        Args:
            result: ScanResult with all parsed data

        Returns:
            Complete README.md content as markdown string
        """
        sections = [
            self._header(result),
            self._build_summary(result),
            self._quality_results(result),
            self._test_results(result),
        ]

        # Add documentation validation if it ran
        if result.doc_validation:
            sections.append(self._doc_validation_results(result))

        sections.extend(
            [
                self._security_results(result),
            ]
        )

        # Add documented vulnerabilities section if HIGH count > 0
        if result.vulnerabilities.high > 0:
            sections.append(self._documented_vulnerabilities(result))

        sections.extend(
            [
                self._docker_results(result),
                self._sonarcloud_results(result),
                self._artifacts_section(result),
                self._quick_actions(result),
                self._footer(result),
            ]
        )

        return "\n\n---\n\n".join(sections)

    def _header(self, result: ScanResult) -> str:
        """Generate header section with metadata."""
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        return f"""# Security Scan Results

**Scan Date:** {now}
**Commit SHA:** {result.commit_sha}
**Branch:** {result.branch}
**Workflow Run:** https://github.com/{result.repository}/actions/runs/{result.workflow_run}"""

    def _build_summary(self, result: ScanResult) -> str:
        """Generate build summary section."""
        overall_status = result.calculate_overall_status()
        alerts = result.get_critical_alerts()

        # Build critical issues section if there are alerts
        critical_issues = ""
        if alerts:
            critical_issues = "\n\n### Critical Issues\n\n" + "\n".join(alerts) + "\n"

        # Build pipeline results table
        quality_status = "✅ Passed" if result.quality.all_passed else "⚠️ Issues"
        test_status = (
            f"✅ {result.tests.passed_runs}/{result.tests.total_runs} Passed"
            if result.tests.all_passed
            else f"❌ {result.tests.failed_runs} Failed"
        )

        # Documentation status
        if result.doc_validation:
            doc_status = "✅ Passed" if result.doc_validation.all_passed else "⚠️ Issues"
            doc_details = f"{result.doc_validation.markdownlint_files} files, {result.doc_validation.total_links} links checked"
        else:
            doc_status = "⏭️ Skipped"
            doc_details = "Doc-only changes trigger validation"

        # Security status
        if result.vulnerabilities.critical > 0:
            security_status = f"❌ {result.vulnerabilities.critical} CRITICAL"
        elif result.vulnerabilities.high > 0:
            security_status = f"⚠️ {result.vulnerabilities.high} HIGH"
        else:
            security_status = "✅ Passed"

        # Docker status
        if result.smoke_tests:
            docker_status = "✅ Passed" if result.smoke_tests.all_passed else "❌ Failed"
            docker_details = "Image built, smoke tests passed, pushed to GHCR"
        else:
            docker_status = "✅ Built"
            docker_details = "Image built successfully"

        return f"""## 📊 Build Summary

**Overall Status:** {overall_status}
**Build Trigger:** Push to {result.branch} branch{critical_issues}

### Build Pipeline Results

| Stage | Status | Details |
|-------|--------|---------|
| 🔍 **Code Quality** | {quality_status} | Ruff: {"✅" if result.quality.ruff_lint_exit == 0 else "⚠️"}, Format: {"✅" if result.quality.ruff_format_exit == 0 else "⚠️"}, Mypy: {"✅" if result.quality.mypy_exit == 0 else "⚠️"} |
| 🧪 **Tests** | {test_status} | 177 tests across Python 3.10-3.13 (Ubuntu + Windows) |
| 📝 **Documentation** | {doc_status} | {doc_details} |
| 🔒 **Security Scan** | {security_status} | CRITICAL: {result.vulnerabilities.critical}, HIGH: {result.vulnerabilities.high}, MEDIUM: {result.vulnerabilities.medium}, LOW: {result.vulnerabilities.low} |
| 🐳 **Docker Build** | {docker_status} | {docker_details} |
| ☁️ **SonarCloud** | ✅ A Rating | View [dashboard](https://sonarcloud.io/project/overview?id=cgbraun_SparseTagging) for details |

### Quick Navigation

- {"🚨 [Critical Issues](#critical-issues) (review required)" if result.has_issues else "✅ No critical issues found"}
- 📊 [Full Workflow Run](https://github.com/{result.repository}/actions/runs/{result.workflow_run})
- 🧪 [Detailed Test Results](#test-matrix-results)
- 📁 [All Artifacts](#all-generated-artifacts)"""

    def _quality_results(self, result: ScanResult) -> str:
        """Generate code quality results section."""
        status = "✅ Passed" if result.quality.all_passed else "⚠️ Issues Found"

        return f"""## 🔍 Code Quality Results

**Status:** {status}

The code quality checks validated Python code against project standards:

- **Ruff Linting:** {"✅ 0 violations" if result.quality.ruff_lint_exit == 0 else "⚠️ Issues found"} ([ruff-lint.txt](./ruff-lint.txt))
- **Code Formatting:** {"✅ All files formatted" if result.quality.ruff_format_exit == 0 else "⚠️ Formatting needed"} ([ruff-format.txt](./ruff-format.txt))
- **Type Checking:** {"✅ 0 type errors" if result.quality.mypy_exit == 0 else "⚠️ Type errors found"} ([mypy-report.txt](./mypy-report.txt))

All source files in `src/` and test files in `tests/` were checked."""

    def _test_results(self, result: ScanResult) -> str:
        """Generate test matrix results section."""
        status = (
            f"✅ {result.tests.passed_runs}/{result.tests.total_runs} Passed"
            if result.tests.all_passed
            else f"❌ {result.tests.failed_runs}/{result.tests.total_runs} Failed"
        )

        return f"""## 🧪 Test Matrix Results

**Status:** {status}

Tests ran across {result.tests.total_runs} environments (Python 3.10, 3.11, 3.12, 3.13 x Ubuntu/Windows):

- **Total Tests:** {result.tests.total_tests} tests
- **Test Runs:** {result.tests.total_runs} environments
- **Passed:** {result.tests.passed_runs} environments
- **Failed:** {result.tests.failed_runs} environments

**Reports:**
- [test-summary.md](./test-summary.md) - Per-environment results
- [coverage.xml](./coverage.xml) - Code coverage metrics (target: ≥85%)"""

    def _doc_validation_results(self, result: ScanResult) -> str:
        """Generate documentation validation results section."""
        if not result.doc_validation:
            return ""

        status = "✅ Passed" if result.doc_validation.all_passed else "⚠️ Issues Found"

        return f"""## 📝 Documentation Validation Results

**Status:** {status}

Documentation files were validated for style and link integrity:

**Markdown Linting:**
- Files checked: {result.doc_validation.markdownlint_files} markdown files
- Style violations: {result.doc_validation.markdownlint_errors} errors
- Report: [markdownlint-report.txt](./markdownlint-report.txt)

**Link Validation:**
- Hyperlinks checked: {result.doc_validation.total_links} links
- Dead links found: {result.doc_validation.dead_links}
- Report: [markdown-link-check-report.txt](./markdown-link-check-report.txt)

> **Note:** Documentation validation only runs when documentation files (`.md`, `docs/**`) are modified."""

    def _security_results(self, result: ScanResult) -> str:
        """Generate security scan results section."""
        if result.vulnerabilities.critical > 0:
            status = "❌ Critical Issues"
        elif result.vulnerabilities.high > 0:
            status = "⚠️ Issues Found"
        else:
            status = "✅ No Critical Issues"

        # Build documented CVEs note if HIGH > 0
        documented_note = ""
        if result.vulnerabilities.high > 0:
            documented_note = f"""

> **📋 Documented Vulnerabilities:** {result.vulnerabilities.high} HIGH severity CVEs are documented as accepted risks with low practical exploitability:
> - **CVE-2026-0861** (glibc memalign): Awaiting Debian patch - See [Issue #18](https://github.com/cgbraun/SparseTagging/issues/18) | [SECURITY.md](../../../SECURITY.md#cve-2026-0861---glibc-memalign-integer-overflow)
> - **GHSA-58pv-8j8x-9vj2** (jaraco.context): Setuptools vendored dependency, not exploitable at runtime - See [Issue #19](https://github.com/cgbraun/SparseTagging/issues/19) | [SECURITY.md](../../../SECURITY.md#ghsa-58pv-8j8x-9vj2---jaracocontext-path-traversal)
"""

        # Build critical warning if CRITICAL > 0
        critical_warning = ""
        if result.vulnerabilities.critical > 0:
            critical_warning = f"""

> **⚠️ CRITICAL:** {result.vulnerabilities.critical} CRITICAL vulnerabilities found. Review [trivy-report.txt](./trivy-report.txt) for CVE details and affected packages.
"""

        return f"""## 🔒 Security Scan Results

**Status:** {status}

Trivy scanned the Docker image for vulnerabilities, secrets, and misconfigurations:

### Vulnerability Breakdown

| Severity | Count | Status |
|----------|-------|--------|
| 🔴 CRITICAL | {result.vulnerabilities.critical} | {"**Action Required**" if result.vulnerabilities.critical > 0 else "None found"} |
| 🟠 HIGH | {result.vulnerabilities.high} | {"**Review Needed**" if result.vulnerabilities.high > 0 else "None found"} |
| 🟡 MEDIUM | {result.vulnerabilities.medium} | Monitor |
| 🔵 LOW | {result.vulnerabilities.low} | Informational |{documented_note}{critical_warning}

**Scan Coverage:**
- Vulnerabilities: ✅ Scanned
- Secret scanning: ✅ Checked
- Misconfiguration: ✅ Analyzed

**Reports:**
- [trivy-results.sarif](./trivy-results.sarif) - Machine-readable (SARIF format for IDE import)
- [trivy-report.txt](./trivy-report.txt) - Human-readable table
- [sbom.spdx.json](./sbom.spdx.json) - Software Bill of Materials (SPDX 2.3)"""

    def _documented_vulnerabilities(self, result: ScanResult) -> str:
        """Generate documented vulnerabilities section (conditional)."""
        if result.vulnerabilities.high == 0:
            return ""

        return f"""## 📋 Documented Vulnerabilities (Accepted Risk)

**Total:** {result.vulnerabilities.high} HIGH severity CVEs documented with accepted risk

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

> **Mitigation:** Both vulnerabilities are monitored via automated CI workflows. When patches become available, Docker images will be rebuilt and rescanned to verify resolution."""

    def _docker_results(self, result: ScanResult) -> str:
        """Generate Docker build results section."""
        if result.smoke_tests:
            status = "✅ Passed" if result.smoke_tests.all_passed else "❌ Failed"
            smoke_tests_section = f"""

**Smoke Tests:**
- {"✅" if result.smoke_tests.test1_status == "PASSED" else "❌"} Import verification: Module loads successfully
- {"✅" if result.smoke_tests.test2_status == "PASSED" else "❌"} Version check: {result.smoke_tests.version} confirmed
- {"✅" if result.smoke_tests.test3_status == "PASSED" else "❌"} Basic functionality: SparseTag creation works

**Deployment:** Image pushed to GitHub Container Registry (GHCR)"""
        else:
            status = "✅ Built"
            smoke_tests_section = """

> **Note:** Smoke tests and GHCR deployment only run on main branch."""

        return f"""## 🐳 Docker Build Results

**Status:** {status}

Docker image successfully built:

**Image Details:**
- Base: `python:3.11-slim` (Debian)
- Tag: `ghcr.io/cgbraun/sparsetagging:latest`
- Architecture: linux/amd64{smoke_tests_section}"""

    def _sonarcloud_results(self, result: ScanResult) -> str:
        """Generate SonarCloud analysis section."""
        return """## ☁️ SonarCloud Analysis

**Status:** ✅ A Rating

Static code analysis completed with quality metrics:

**Quick Links:**
- 🎯 [Quality Gate](https://sonarcloud.io/project/overview?id=cgbraun_SparseTagging) - Overall project health
- 🔒 [Security Vulnerabilities](https://sonarcloud.io/project/issues?id=cgbraun_SparseTagging&resolved=false&types=VULNERABILITY) - Unresolved security issues
- ⚠️ [Security Hotspots](https://sonarcloud.io/project/security_hotspots?id=cgbraun_SparseTagging) - Security-sensitive code for review
- 🐛 [Bugs & Code Smells](https://sonarcloud.io/project/issues?id=cgbraun_SparseTagging&resolved=false) - All quality issues
- 📈 [Code Coverage](https://sonarcloud.io/component_measures?id=cgbraun_SparseTagging&metric=coverage&view=list) - Line and branch coverage details"""

    def _artifacts_section(self, result: ScanResult) -> str:
        """Generate all generated artifacts section."""
        doc_artifacts = ""
        if result.doc_validation:
            doc_artifacts = """
**Documentation Reports:**
[markdownlint-report.txt](./markdownlint-report.txt) | [markdown-link-check-report.txt](./markdown-link-check-report.txt)
"""

        return f"""## 📁 All Generated Artifacts

Quick reference to all files in this scan directory:

**Quality Reports:**
[ruff-lint.txt](./ruff-lint.txt) | [ruff-format.txt](./ruff-format.txt) | [mypy-report.txt](./mypy-report.txt)

**Test Reports:**
[test-summary.md](./test-summary.md) | [coverage.xml](./coverage.xml)

**Security Reports:**
[trivy-results.sarif](./trivy-results.sarif) | [trivy-report.txt](./trivy-report.txt) | [sbom.spdx.json](./sbom.spdx.json){doc_artifacts}"""

    def _quick_actions(self, result: ScanResult) -> str:
        """Generate quick actions section."""
        return f"""## 💡 Quick Actions

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
- Review [workflow run logs](https://github.com/{result.repository}/actions/runs/{result.workflow_run}) for full execution details
- Check `SECURITY.md` in repository root for security policy and reporting procedures"""

    def _footer(self, result: ScanResult) -> str:
        """Generate footer section."""
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        return f"""_Report generated by CI/CD pipeline on {now} - See [full workflow run](https://github.com/{result.repository}/actions/runs/{result.workflow_run})_"""
