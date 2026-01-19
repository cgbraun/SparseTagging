"""Parser for pytest test matrix results."""

import re
from pathlib import Path

from models.scan_result import TestResults


class PytestParser:
    """Parse pytest results from test matrix runs (multiple Python versions and OSes)."""

    def parse_matrix(self, test_results_dir: str | Path) -> TestResults:
        """Parse pytest results from all test matrix runs.

        Args:
            test_results_dir: Directory containing test-results-* subdirectories

        Returns:
            TestResults with counts of total runs, passed runs, and total tests

        Directory structure expected:
            test-results/
            ├── test-results-ubuntu-latest-py3.10/
            │   ├── pytest-output.txt
            │   └── pytest-results.xml
            ├── test-results-ubuntu-latest-py3.11/
            │   └── ...
            └── test-results-windows-latest-py3.10/
                └── ...

        A test run is considered "passed" if pytest-output.txt contains "Exit code: 0"
        """
        results_path = Path(test_results_dir)

        if not results_path.exists():
            print(f"Warning: Test results directory not found: {results_path}")
            return TestResults(total_runs=0, passed_runs=0)

        total_runs = 0
        passed_runs = 0

        # Iterate through all test-results-* directories
        for test_dir in results_path.glob("test-results-*"):
            if not test_dir.is_dir():
                continue

            total_runs += 1

            # Check if pytest-output.txt exists and contains "Exit code: 0"
            output_file = test_dir / "pytest-output.txt"
            if output_file.exists():
                try:
                    with open(output_file, encoding="utf-8") as f:
                        content = f.read()
                        # Look for "Exit code: 0" which indicates success
                        if "Exit code: 0" in content:
                            passed_runs += 1
                except OSError as e:
                    print(f"Warning: Failed to read {output_file}: {e}")

        return TestResults(total_runs=total_runs, passed_runs=passed_runs)

    def parse_single_run(self, output_file: str | Path) -> bool:
        """Parse a single pytest output file to determine if tests passed.

        Args:
            output_file: Path to pytest-output.txt file

        Returns:
            True if tests passed (exit code 0), False otherwise
        """
        output_path = Path(output_file)

        if not output_path.exists():
            return False

        try:
            with open(output_path, encoding="utf-8") as f:
                content = f.read()
                return "Exit code: 0" in content
        except OSError:
            return False

    def extract_test_summary(self, output_file: str | Path) -> dict[str, str]:
        """Extract test summary statistics from pytest output.

        Args:
            output_file: Path to pytest-output.txt file

        Returns:
            Dictionary with keys like 'passed', 'failed', 'error', 'skipped', etc.
        """
        output_path = Path(output_file)

        if not output_path.exists():
            return {}

        try:
            with open(output_path, encoding="utf-8") as f:
                content = f.read()

            summary = {}

            # Look for summary line like "177 passed in 5.23s"
            # or "170 passed, 7 failed in 6.42s"
            passed_match = re.search(r"(\d+)\s+passed", content)
            if passed_match:
                summary["passed"] = passed_match.group(1)

            failed_match = re.search(r"(\d+)\s+failed", content)
            if failed_match:
                summary["failed"] = failed_match.group(1)

            error_match = re.search(r"(\d+)\s+error", content)
            if error_match:
                summary["error"] = error_match.group(1)

            skipped_match = re.search(r"(\d+)\s+skipped", content)
            if skipped_match:
                summary["skipped"] = skipped_match.group(1)

            return summary

        except OSError:
            return {}
