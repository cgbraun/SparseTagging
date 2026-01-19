"""Unit tests for pytest results parser."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from parsers.pytest_parser import PytestParser


class TestPytestParser(unittest.TestCase):
    """Test cases for PytestParser."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = PytestParser()

    def test_parse_matrix_all_passed(self):
        """Test parsing test matrix where all runs passed."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_results = Path(tmpdir)

            # Create 3 test result directories with passing tests
            for env in ["ubuntu-latest-py3.11", "ubuntu-latest-py3.12", "windows-latest-py3.11"]:
                env_dir = test_results / f"test-results-{env}"
                env_dir.mkdir()

                output_file = env_dir / "pytest-output.txt"
                output_file.write_text("177 passed in 5.23s\n\nExit code: 0", encoding="utf-8")

            result = self.parser.parse_matrix(test_results)

            self.assertEqual(result.total_runs, 3)
            self.assertEqual(result.passed_runs, 3)
            self.assertEqual(result.failed_runs, 0)
            self.assertTrue(result.all_passed)

    def test_parse_matrix_some_failed(self):
        """Test parsing test matrix where some runs failed."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_results = Path(tmpdir)

            # Create passing run
            env_dir1 = test_results / "test-results-ubuntu-latest-py3.11"
            env_dir1.mkdir()
            (env_dir1 / "pytest-output.txt").write_text(
                "177 passed in 5.23s\n\nExit code: 0", encoding="utf-8"
            )

            # Create failing run
            env_dir2 = test_results / "test-results-ubuntu-latest-py3.12"
            env_dir2.mkdir()
            (env_dir2 / "pytest-output.txt").write_text(
                "170 passed, 7 failed in 6.42s\n\nExit code: 1", encoding="utf-8"
            )

            result = self.parser.parse_matrix(test_results)

            self.assertEqual(result.total_runs, 2)
            self.assertEqual(result.passed_runs, 1)
            self.assertEqual(result.failed_runs, 1)
            self.assertFalse(result.all_passed)

    def test_parse_matrix_nonexistent_directory(self):
        """Test parsing when test results directory doesn't exist."""
        result = self.parser.parse_matrix("nonexistent_dir")

        self.assertEqual(result.total_runs, 0)
        self.assertEqual(result.passed_runs, 0)
        self.assertTrue(result.all_passed)  # Vacuously true (no failures)

    def test_parse_matrix_missing_output_files(self):
        """Test parsing when pytest-output.txt files are missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_results = Path(tmpdir)

            # Create test directories but no output files
            (test_results / "test-results-ubuntu-latest-py3.11").mkdir()
            (test_results / "test-results-ubuntu-latest-py3.12").mkdir()

            result = self.parser.parse_matrix(test_results)

            # Should count directories but no passed runs
            self.assertEqual(result.total_runs, 2)
            self.assertEqual(result.passed_runs, 0)
            self.assertEqual(result.failed_runs, 2)

    def test_parse_single_run_passed(self):
        """Test parsing a single pytest output file that passed."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write("177 passed in 5.23s\n\nExit code: 0")
            temp_path = f.name

        try:
            result = self.parser.parse_single_run(temp_path)
            self.assertTrue(result)
        finally:
            Path(temp_path).unlink()

    def test_parse_single_run_failed(self):
        """Test parsing a single pytest output file that failed."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write("170 passed, 7 failed\n\nExit code: 1")
            temp_path = f.name

        try:
            result = self.parser.parse_single_run(temp_path)
            self.assertFalse(result)
        finally:
            Path(temp_path).unlink()

    def test_extract_test_summary(self):
        """Test extracting test summary statistics."""
        output_content = """
        ============================= test session starts ==============================
        collected 177 items

        tests/test_sparsetag.py::TestSparseTag::test_query_cache ... PASSED
        ...

        ======================== 170 passed, 7 failed in 6.42s =========================
        """

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write(output_content)
            temp_path = f.name

        try:
            summary = self.parser.extract_test_summary(temp_path)

            self.assertEqual(summary["passed"], "170")
            self.assertEqual(summary["failed"], "7")

        finally:
            Path(temp_path).unlink()


if __name__ == "__main__":
    unittest.main()
