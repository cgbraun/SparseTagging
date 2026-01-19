"""Unit tests for quality gate parser."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from parsers.quality_parser import QualityParser


class TestQualityParser(unittest.TestCase):
    """Test cases for QualityParser."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = QualityParser()

    def test_parse_all_passed(self):
        """Test parsing when all quality gates passed."""
        with tempfile.TemporaryDirectory() as tmpdir:
            reports_dir = Path(tmpdir)

            # Create reports with exit code 0
            (reports_dir / "ruff-lint.txt").write_text(
                "All checks passed\n\nExit code: 0", encoding="utf-8"
            )
            (reports_dir / "ruff-format.txt").write_text(
                "All files formatted\n\nExit code: 0", encoding="utf-8"
            )
            (reports_dir / "mypy-report.txt").write_text(
                "Success: no issues found\n\nExit code: 0", encoding="utf-8"
            )

            result = self.parser.parse(reports_dir)

            self.assertEqual(result.ruff_lint_exit, 0)
            self.assertEqual(result.ruff_format_exit, 0)
            self.assertEqual(result.mypy_exit, 0)
            self.assertTrue(result.all_passed)

    def test_parse_some_failed(self):
        """Test parsing when some quality gates failed."""
        with tempfile.TemporaryDirectory() as tmpdir:
            reports_dir = Path(tmpdir)

            # Ruff lint passed
            (reports_dir / "ruff-lint.txt").write_text(
                "All checks passed\n\nExit code: 0", encoding="utf-8"
            )

            # Format failed
            (reports_dir / "ruff-format.txt").write_text(
                "3 files need formatting\n\nExit code: 1", encoding="utf-8"
            )

            # Mypy failed
            (reports_dir / "mypy-report.txt").write_text(
                "Found 5 errors in 2 files\n\nExit code: 1", encoding="utf-8"
            )

            result = self.parser.parse(reports_dir)

            self.assertEqual(result.ruff_lint_exit, 0)
            self.assertEqual(result.ruff_format_exit, 1)
            self.assertEqual(result.mypy_exit, 1)
            self.assertFalse(result.all_passed)

    def test_parse_missing_files(self):
        """Test parsing when some report files are missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            reports_dir = Path(tmpdir)

            # Only create one report file
            (reports_dir / "ruff-lint.txt").write_text(
                "All checks passed\n\nExit code: 0", encoding="utf-8"
            )

            result = self.parser.parse(reports_dir)

            self.assertEqual(result.ruff_lint_exit, 0)
            self.assertEqual(result.ruff_format_exit, -1)  # Missing file
            self.assertEqual(result.mypy_exit, -1)  # Missing file
            self.assertFalse(result.all_passed)

    def test_parse_nonexistent_directory(self):
        """Test parsing when reports directory doesn't exist."""
        result = self.parser.parse("nonexistent_dir")

        # All should return -1 (file not found)
        self.assertEqual(result.ruff_lint_exit, -1)
        self.assertEqual(result.ruff_format_exit, -1)
        self.assertEqual(result.mypy_exit, -1)

    def test_get_exit_code_no_exit_code_line(self):
        """Test extracting exit code when file has no exit code line."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write("Some output without exit code footer")
            temp_path = f.name

        try:
            result = self.parser._get_exit_code(Path(temp_path))
            self.assertEqual(result, -1)  # No exit code found
        finally:
            Path(temp_path).unlink()

    def test_parse_ruff_lint_violations(self):
        """Test parsing ruff lint violations."""
        lint_output = """
        src/sparsetag.py:123:45: E501 Line too long (120 > 88 characters)
        src/sparsetag.py:456:78: F401 'numpy as np' imported but unused
        src/cache_manager.py:99:12: E501 Line too long (95 > 88 characters)
        src/cache_manager.py:101:5: W291 Trailing whitespace

        Exit code: 1
        """

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write(lint_output)
            temp_path = f.name

        try:
            violations = self.parser.parse_ruff_lint(temp_path)

            self.assertEqual(violations["E501"], 2)
            self.assertEqual(violations["F401"], 1)
            self.assertEqual(violations["W291"], 1)

        finally:
            Path(temp_path).unlink()

    def test_parse_mypy_errors(self):
        """Test parsing mypy error counts."""
        mypy_output = """
        src/sparsetag.py:123: error: Incompatible return value type
        src/sparsetag.py:456: note: See documentation for details
        src/cache_manager.py:99: error: Argument 1 has incompatible type
        src/cache_manager.py:100: error: Name 'foo' is not defined

        Exit code: 1
        """

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write(mypy_output)
            temp_path = f.name

        try:
            result = self.parser.parse_mypy(temp_path)

            self.assertEqual(result["errors"], 3)
            self.assertEqual(result["notes"], 1)

        finally:
            Path(temp_path).unlink()


if __name__ == "__main__":
    unittest.main()
