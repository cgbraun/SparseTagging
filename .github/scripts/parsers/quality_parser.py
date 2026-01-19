"""Parser for code quality gate results."""

import re
from pathlib import Path

from models.scan_result import QualityGates


class QualityParser:
    """Parse quality gate results from ruff and mypy reports."""

    def parse(self, quality_reports_dir: str | Path) -> QualityGates:
        """Parse all quality gate reports to extract exit codes.

        Args:
            quality_reports_dir: Directory containing quality report files

        Returns:
            QualityGates with exit codes for ruff-lint, ruff-format, and mypy

        Expected files:
            - ruff-lint.txt
            - ruff-format.txt
            - mypy-report.txt

        Each file should end with "Exit code: N" where N is the exit status.
        Exit code 0 means passed, non-zero means issues found.
        """
        reports_path = Path(quality_reports_dir)

        return QualityGates(
            ruff_lint_exit=self._get_exit_code(reports_path / "ruff-lint.txt"),
            ruff_format_exit=self._get_exit_code(reports_path / "ruff-format.txt"),
            mypy_exit=self._get_exit_code(reports_path / "mypy-report.txt"),
        )

    def _get_exit_code(self, file_path: Path) -> int:
        """Extract exit code from a report file.

        Args:
            file_path: Path to report file

        Returns:
            Exit code (0 for success, >0 for failure, -1 if file not found)

        The file is expected to end with a line like:
            Exit code: 0
        """
        if not file_path.exists():
            print(f"Warning: Report file not found: {file_path}")
            return -1

        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            # Look for "Exit code: N" pattern (usually at end of file)
            match = re.search(r"Exit code:\s*(\d+)", content)
            if match:
                return int(match.group(1))
            print(f"Warning: No exit code found in {file_path}")
            return -1

        except OSError as e:
            print(f"Warning: Failed to read {file_path}: {e}")
            return -1

    def parse_ruff_lint(self, report_path: str | Path) -> dict[str, int]:
        """Parse ruff lint report to extract violation counts.

        Args:
            report_path: Path to ruff-lint.txt

        Returns:
            Dictionary with violation counts by category
        """
        report_file = Path(report_path)

        if not report_file.exists():
            return {}

        try:
            with open(report_file, encoding="utf-8") as f:
                content = f.read()

            violations = {}

            # Count occurrences of different ruff error codes (e.g., E501, F401)
            # Pattern: filename:line:col: CODE message
            for match in re.finditer(r"\b([A-Z]\d{3,4})\b", content):
                code = match.group(1)
                violations[code] = violations.get(code, 0) + 1

            return violations

        except OSError:
            return {}

    def parse_mypy(self, report_path: str | Path) -> dict[str, int]:
        """Parse mypy report to extract type error counts.

        Args:
            report_path: Path to mypy-report.txt

        Returns:
            Dictionary with error counts by type
        """
        report_file = Path(report_path)

        if not report_file.exists():
            return {}

        try:
            with open(report_file, encoding="utf-8") as f:
                content = f.read()

            # Count total errors/notes (look for "error:" and "note:" patterns)
            errors = content.count("error:")
            notes = content.count("note:")

            return {"errors": errors, "notes": notes}

        except OSError:
            return {}
