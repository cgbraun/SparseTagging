"""Data models for CI scan results."""

from dataclasses import dataclass


@dataclass
class VulnerabilityCount:
    """Vulnerability counts by severity from Trivy scan."""

    critical: int
    high: int
    medium: int
    low: int

    def has_critical(self) -> bool:
        """Check if there are critical vulnerabilities."""
        return self.critical > 0

    def has_high(self) -> bool:
        """Check if there are high severity vulnerabilities."""
        return self.high > 0


@dataclass
class TestResults:
    """Test matrix results across multiple environments."""

    total_runs: int
    passed_runs: int
    total_tests: int = 177  # SparseTagging has 177 tests

    @property
    def failed_runs(self) -> int:
        """Number of failed test runs."""
        return self.total_runs - self.passed_runs

    @property
    def all_passed(self) -> bool:
        """Check if all test runs passed."""
        return self.failed_runs == 0


@dataclass
class QualityGates:
    """Code quality gate results (ruff, mypy)."""

    ruff_lint_exit: int
    ruff_format_exit: int
    mypy_exit: int

    @property
    def all_passed(self) -> bool:
        """Check if all quality gates passed."""
        return self.ruff_lint_exit == 0 and self.ruff_format_exit == 0 and self.mypy_exit == 0


@dataclass
class DocValidationResults:
    """Documentation validation results."""

    markdownlint_errors: int
    markdownlint_files: int
    dead_links: int
    total_links: int

    @property
    def all_passed(self) -> bool:
        """Check if documentation validation passed."""
        return self.markdownlint_errors == 0 and self.dead_links == 0


@dataclass
class SmokeTestResults:
    """Docker smoke test results."""

    test1_status: str  # "PASSED" or "FAILED"
    test2_status: str
    test3_status: str
    version: str

    @property
    def all_passed(self) -> bool:
        """Check if all smoke tests passed."""
        return (
            self.test1_status == "PASSED"
            and self.test2_status == "PASSED"
            and self.test3_status == "PASSED"
        )


@dataclass
class ScanResult:
    """Complete scan results from CI/CD pipeline."""

    vulnerabilities: VulnerabilityCount
    tests: TestResults
    quality: QualityGates
    commit_sha: str
    workflow_run: str
    repository: str
    branch: str
    doc_validation: DocValidationResults | None = None
    smoke_tests: SmokeTestResults | None = None

    def calculate_overall_status(self) -> str:
        """Calculate overall build status based on all results.

        Returns:
            Status string like "✅ All Checks Passed", "❌ Critical Issues Found", etc.
        """
        if self.vulnerabilities.has_critical() or not self.tests.all_passed:
            return "❌ Critical Issues Found"
        if self.vulnerabilities.high > 5 or not self.quality.all_passed:
            return "⚠️ Issues Require Attention"
        return "✅ All Checks Passed"

    def get_critical_alerts(self) -> list[str]:
        """Get list of critical alert messages.

        Returns:
            List of alert strings for display in the README.
        """
        alerts = []

        if self.vulnerabilities.has_critical():
            alerts.append(
                f"> **🔴 CRITICAL:** {self.vulnerabilities.critical} CRITICAL CVEs in dependencies"
            )

        if self.vulnerabilities.high > 5:
            alerts.append(
                f"> **🟡 WARNING:** {self.vulnerabilities.high} HIGH severity vulnerabilities require review"
            )

        if not self.tests.all_passed:
            alerts.append(f"> **🔴 CRITICAL:** {self.tests.failed_runs} test environment(s) failed")

        if self.quality.mypy_exit != 0:
            alerts.append(
                f"> **🟡 WARNING:** Type checking failed with {self.quality.mypy_exit} errors"
            )

        return alerts

    @property
    def has_issues(self) -> bool:
        """Check if there are any issues (not all checks passed)."""
        return self.calculate_overall_status() != "✅ All Checks Passed"
