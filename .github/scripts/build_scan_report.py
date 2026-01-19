#!/usr/bin/env python3
"""Generate comprehensive scan results README for CI/CD pipeline.

This script parses artifacts from CI jobs (Trivy, pytest, quality gates, doc validation)
and generates a detailed markdown README for the ScanResults directory.

Usage:
    python build_scan_report.py \\
        --scan-dir "ScanResults/2026-01-18_12-34-56" \\
        --commit-sha "abc123..." \\
        --workflow-run "1234567890" \\
        --repository "cgbraun/SparseTagging" \\
        --branch "main"
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path to allow imports
sys.path.insert(0, str(Path(__file__).parent))

from generators.readme_generator import ReadmeGenerator
from models.scan_result import ScanResult
from parsers.doc_parser import DocValidationParser
from parsers.pytest_parser import PytestParser
from parsers.quality_parser import QualityParser
from parsers.smoke_test_parser import SmokeTestParser
from parsers.trivy_parser import TrivyParser


def main() -> int:
    """Main entry point for build scan report generator.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = argparse.ArgumentParser(
        description="Generate scan results README from CI artifacts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
    python build_scan_report.py \\
        --scan-dir "ScanResults/2026-01-18_12-34-56" \\
        --commit-sha "abc123def456" \\
        --workflow-run "1234567890" \\
        --repository "cgbraun/SparseTagging" \\
        --branch "main"
        """,
    )

    parser.add_argument(
        "--scan-dir",
        required=True,
        help="Output directory for scan results (e.g., ScanResults/TIMESTAMP)",
    )
    parser.add_argument(
        "--commit-sha",
        required=True,
        help="Git commit SHA that triggered the build",
    )
    parser.add_argument(
        "--workflow-run",
        required=True,
        help="GitHub Actions workflow run ID",
    )
    parser.add_argument(
        "--repository",
        required=True,
        help="GitHub repository in format owner/repo",
    )
    parser.add_argument(
        "--branch",
        required=True,
        help="Git branch name",
    )

    args = parser.parse_args()

    try:
        # Convert paths to Path objects
        scan_dir = Path(args.scan_dir)

        print(f"📊 Generating scan results README for {args.repository}@{args.commit_sha[:7]}")
        print(f"📁 Output directory: {scan_dir}")

        # Parse Trivy SARIF results
        print("🔍 Parsing Trivy scan results...")
        trivy_parser = TrivyParser()
        trivy_sarif = scan_dir / "trivy-results.sarif"
        vulnerabilities = trivy_parser.parse(trivy_sarif)
        print(
            f"   Found: {vulnerabilities.critical} CRITICAL, {vulnerabilities.high} HIGH, "
            f"{vulnerabilities.medium} MEDIUM, {vulnerabilities.low} LOW"
        )

        # Parse pytest test matrix results
        print("🧪 Parsing test results...")
        pytest_parser = PytestParser()
        test_results = pytest_parser.parse_matrix("test-results")
        print(f"   Tests: {test_results.passed_runs}/{test_results.total_runs} environments passed")

        # Parse quality gate results
        print("🔍 Parsing quality gate results...")
        quality_parser = QualityParser()
        quality = quality_parser.parse("quality-reports")
        print(
            f"   Quality: Ruff={quality.ruff_lint_exit}, Format={quality.ruff_format_exit}, "
            f"Mypy={quality.mypy_exit}"
        )

        # Parse documentation validation (optional)
        print("📝 Parsing documentation validation...")
        doc_parser = DocValidationParser()
        doc_validation = doc_parser.parse("doc-validation-reports")
        if doc_validation:
            print(
                f"   Docs: {doc_validation.markdownlint_errors} lint errors, "
                f"{doc_validation.dead_links} dead links"
            )
        else:
            print("   Docs: Validation not run (skipped)")

        # Parse smoke test results (optional, main branch only)
        print("🐳 Parsing Docker smoke test results...")
        smoke_parser = SmokeTestParser()
        smoke_tests = smoke_parser.parse("docker-smoke-test-results.txt")
        if smoke_tests:
            print(
                f"   Docker: {smoke_tests.version}, all tests {'passed' if smoke_tests.all_passed else 'FAILED'}"
            )
        else:
            print("   Docker: Smoke tests not run (PR builds only)")

        # Build comprehensive result object
        result = ScanResult(
            vulnerabilities=vulnerabilities,
            tests=test_results,
            quality=quality,
            commit_sha=args.commit_sha,
            workflow_run=args.workflow_run,
            repository=args.repository,
            branch=args.branch,
            doc_validation=doc_validation,
            smoke_tests=smoke_tests,
        )

        # Generate README
        print("📝 Generating README.md...")
        generator = ReadmeGenerator()
        readme_content = generator.generate(result)

        # Write to file
        output_path = scan_dir / "README.md"
        output_path.write_text(readme_content, encoding="utf-8")

        print(f"✅ README generated successfully: {output_path}")
        print(f"📊 Overall status: {result.calculate_overall_status()}")

        # Exit with non-zero if there are critical issues (for CI visibility)
        if result.vulnerabilities.has_critical():
            print("⚠️  CRITICAL vulnerabilities found - review required!")
            return 1
        if not result.tests.all_passed:
            print("⚠️  Test failures detected - review required!")
            return 1

        return 0

    except Exception as e:
        print(f"❌ Error generating README: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
