"""Unit tests for README generator."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from generators.readme_generator import ReadmeGenerator
from models.scan_result import (
    DocValidationResults,
    QualityGates,
    ScanResult,
    SmokeTestResults,
    TestResults,
    VulnerabilityCount,
)


class TestReadmeGenerator(unittest.TestCase):
    """Test cases for ReadmeGenerator."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = ReadmeGenerator()

    def test_generate_minimal_result(self):
        """Test generating README with minimal scan result."""
        result = ScanResult(
            vulnerabilities=VulnerabilityCount(critical=0, high=0, medium=0, low=0),
            tests=TestResults(total_runs=8, passed_runs=8),
            quality=QualityGates(ruff_lint_exit=0, ruff_format_exit=0, mypy_exit=0),
            commit_sha="abc123def456",
            workflow_run="1234567890",
            repository="cgbraun/SparseTagging",
            branch="main",
        )

        readme = self.generator.generate(result)

        # Check key sections are present
        self.assertIn("# Security Scan Results", readme)
        self.assertIn("## 📊 Build Summary", readme)
        self.assertIn("## 🔍 Code Quality Results", readme)
        self.assertIn("## 🧪 Test Matrix Results", readme)
        self.assertIn("## 🔒 Security Scan Results", readme)
        self.assertIn("## 🐳 Docker Build Results", readme)
        self.assertIn("## ☁️ SonarCloud Analysis", readme)

        # Check metadata
        self.assertIn("abc123def456", readme)
        self.assertIn("main", readme)
        self.assertIn("cgbraun/SparseTagging", readme)
        self.assertIn("1234567890", readme)

        # Check overall status
        self.assertIn("✅ All Checks Passed", readme)

    def test_generate_with_critical_vulns(self):
        """Test generating README with critical vulnerabilities."""
        result = ScanResult(
            vulnerabilities=VulnerabilityCount(critical=2, high=5, medium=10, low=20),
            tests=TestResults(total_runs=8, passed_runs=8),
            quality=QualityGates(ruff_lint_exit=0, ruff_format_exit=0, mypy_exit=0),
            commit_sha="abc123def456",
            workflow_run="1234567890",
            repository="cgbraun/SparseTagging",
            branch="main",
        )

        readme = self.generator.generate(result)

        # Check critical alerts section
        self.assertIn("### Critical Issues", readme)
        self.assertIn("🔴 CRITICAL:", readme)
        self.assertIn("2 CRITICAL CVEs", readme)
        self.assertIn("❌ Critical Issues Found", readme)

    def test_generate_with_test_failures(self):
        """Test generating README with test failures."""
        result = ScanResult(
            vulnerabilities=VulnerabilityCount(critical=0, high=0, medium=0, low=0),
            tests=TestResults(total_runs=8, passed_runs=6),  # 2 failed
            quality=QualityGates(ruff_lint_exit=0, ruff_format_exit=0, mypy_exit=0),
            commit_sha="abc123def456",
            workflow_run="1234567890",
            repository="cgbraun/SparseTagging",
            branch="main",
        )

        readme = self.generator.generate(result)

        # Check test failure status
        self.assertIn("❌ 2 Failed", readme)
        self.assertIn("❌ Critical Issues Found", readme)  # Overall status
        self.assertIn("2 test environment(s) failed", readme)

    def test_generate_with_doc_validation(self):
        """Test generating README with documentation validation results."""
        result = ScanResult(
            vulnerabilities=VulnerabilityCount(critical=0, high=0, medium=0, low=0),
            tests=TestResults(total_runs=8, passed_runs=8),
            quality=QualityGates(ruff_lint_exit=0, ruff_format_exit=0, mypy_exit=0),
            commit_sha="abc123def456",
            workflow_run="1234567890",
            repository="cgbraun/SparseTagging",
            branch="main",
            doc_validation=DocValidationResults(
                markdownlint_errors=3,
                markdownlint_files=25,
                dead_links=2,
                total_links=150,
            ),
        )

        readme = self.generator.generate(result)

        # Check doc validation section
        self.assertIn("## 📝 Documentation Validation Results", readme)
        self.assertIn("3 errors", readme)
        self.assertIn("25 markdown files", readme)
        self.assertIn("2", readme)  # dead links
        self.assertIn("150 links", readme)

    def test_generate_with_smoke_tests(self):
        """Test generating README with Docker smoke test results."""
        result = ScanResult(
            vulnerabilities=VulnerabilityCount(critical=0, high=0, medium=0, low=0),
            tests=TestResults(total_runs=8, passed_runs=8),
            quality=QualityGates(ruff_lint_exit=0, ruff_format_exit=0, mypy_exit=0),
            commit_sha="abc123def456",
            workflow_run="1234567890",
            repository="cgbraun/SparseTagging",
            branch="main",
            smoke_tests=SmokeTestResults(
                test1_status="PASSED",
                test2_status="PASSED",
                test3_status="PASSED",
                version="2.4.1",
            ),
        )

        readme = self.generator.generate(result)

        # Check smoke tests section
        self.assertIn("**Smoke Tests:**", readme)
        self.assertIn("2.4.1", readme)
        self.assertIn("Import verification", readme)
        self.assertIn("Version check", readme)
        self.assertIn("Basic functionality", readme)

    def test_generate_with_high_vulns_shows_documented_section(self):
        """Test that documented vulnerabilities section appears when HIGH > 0."""
        result = ScanResult(
            vulnerabilities=VulnerabilityCount(critical=0, high=2, medium=5, low=10),
            tests=TestResults(total_runs=8, passed_runs=8),
            quality=QualityGates(ruff_lint_exit=0, ruff_format_exit=0, mypy_exit=0),
            commit_sha="abc123def456",
            workflow_run="1234567890",
            repository="cgbraun/SparseTagging",
            branch="main",
        )

        readme = self.generator.generate(result)

        # Check documented vulnerabilities section
        self.assertIn("## 📋 Documented Vulnerabilities (Accepted Risk)", readme)
        self.assertIn("CVE-2026-0861", readme)
        self.assertIn("GHSA-58pv-8j8x-9vj2", readme)

    def test_overall_status_calculation(self):
        """Test overall status calculation logic."""
        # All passed
        result1 = ScanResult(
            vulnerabilities=VulnerabilityCount(critical=0, high=0, medium=0, low=0),
            tests=TestResults(total_runs=8, passed_runs=8),
            quality=QualityGates(ruff_lint_exit=0, ruff_format_exit=0, mypy_exit=0),
            commit_sha="abc",
            workflow_run="123",
            repository="repo",
            branch="main",
        )
        self.assertEqual(result1.calculate_overall_status(), "✅ All Checks Passed")

        # Critical CVE
        result2 = ScanResult(
            vulnerabilities=VulnerabilityCount(critical=1, high=0, medium=0, low=0),
            tests=TestResults(total_runs=8, passed_runs=8),
            quality=QualityGates(ruff_lint_exit=0, ruff_format_exit=0, mypy_exit=0),
            commit_sha="abc",
            workflow_run="123",
            repository="repo",
            branch="main",
        )
        self.assertEqual(result2.calculate_overall_status(), "❌ Critical Issues Found")

        # Test failure
        result3 = ScanResult(
            vulnerabilities=VulnerabilityCount(critical=0, high=0, medium=0, low=0),
            tests=TestResults(total_runs=8, passed_runs=6),
            quality=QualityGates(ruff_lint_exit=0, ruff_format_exit=0, mypy_exit=0),
            commit_sha="abc",
            workflow_run="123",
            repository="repo",
            branch="main",
        )
        self.assertEqual(result3.calculate_overall_status(), "❌ Critical Issues Found")

        # High CVEs (warning level)
        result4 = ScanResult(
            vulnerabilities=VulnerabilityCount(critical=0, high=6, medium=0, low=0),
            tests=TestResults(total_runs=8, passed_runs=8),
            quality=QualityGates(ruff_lint_exit=0, ruff_format_exit=0, mypy_exit=0),
            commit_sha="abc",
            workflow_run="123",
            repository="repo",
            branch="main",
        )
        self.assertEqual(result4.calculate_overall_status(), "⚠️ Issues Require Attention")


if __name__ == "__main__":
    unittest.main()
