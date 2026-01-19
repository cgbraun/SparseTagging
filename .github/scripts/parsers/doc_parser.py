"""Parser for documentation validation results."""

import re
from pathlib import Path

from models.scan_result import DocValidationResults


class DocValidationParser:
    """Parse documentation validation results from markdownlint and markdown-link-check."""

    def parse(self, reports_dir: str | Path) -> DocValidationResults | None:
        """Parse documentation validation reports.

        Args:
            reports_dir: Directory containing doc validation reports

        Returns:
            DocValidationResults if reports exist, None otherwise

        Expected files:
            - markdownlint-report.txt
            - markdown-link-check-report.txt
        """
        reports_path = Path(reports_dir)

        markdownlint_file = reports_path / "markdownlint-report.txt"
        link_check_file = reports_path / "markdown-link-check-report.txt"

        # If neither file exists, return None (doc validation didn't run)
        if not markdownlint_file.exists() and not link_check_file.exists():
            return None

        # Parse markdownlint results
        if markdownlint_file.exists():
            markdownlint_errors, markdownlint_files = self._parse_markdownlint(markdownlint_file)
        else:
            markdownlint_errors, markdownlint_files = 0, 0

        # Parse link check results
        if link_check_file.exists():
            dead_links, total_links = self._parse_link_check(link_check_file)
        else:
            dead_links, total_links = 0, 0

        return DocValidationResults(
            markdownlint_errors=markdownlint_errors,
            markdownlint_files=markdownlint_files,
            dead_links=dead_links,
            total_links=total_links,
        )

    def _parse_markdownlint(self, report_path: Path) -> tuple[int, int]:
        """Parse markdownlint report to extract error and file counts.

        Args:
            report_path: Path to markdownlint-report.txt

        Returns:
            Tuple of (errors, files_checked)
        """
        try:
            with open(report_path, encoding="utf-8") as f:
                content = f.read()

            # Count files checked (lines ending with .md)
            files_checked = content.count(".md")

            # Look for error summary like "15 error(s)" or "0 errors"
            error_match = re.search(r"(\d+)\s+error", content)
            # If no error summary, assume 0 errors if file exists
            errors = int(error_match.group(1)) if error_match else 0

            return errors, files_checked

        except OSError:
            return 0, 0

    def _parse_link_check(self, report_path: Path) -> tuple[int, int]:
        """Parse markdown-link-check report to extract link counts.

        Args:
            report_path: Path to markdown-link-check-report.txt

        Returns:
            Tuple of (dead_links, total_links)
        """
        try:
            with open(report_path, encoding="utf-8") as f:
                content = f.read()

            # Count total links (lines with [✓] or [✗])
            total_links = content.count("[✓]") + content.count("[✗]")

            # Count dead links (lines with [✗])
            dead_links = content.count("[✗]")

            return dead_links, total_links

        except OSError:
            return 0, 0
