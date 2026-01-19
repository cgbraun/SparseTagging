"""Unit tests for Trivy SARIF parser."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from parsers.trivy_parser import TrivyParser


class TestTrivyParser(unittest.TestCase):
    """Test cases for TrivyParser."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = TrivyParser()

    def test_parse_valid_sarif(self):
        """Test parsing a valid SARIF file with vulnerabilities."""
        # Create sample SARIF structure
        sarif_data = {
            "runs": [
                {
                    "tool": {
                        "driver": {
                            "rules": [
                                {"properties": {"tags": ["CRITICAL"]}},
                                {"properties": {"tags": ["CRITICAL"]}},
                                {"properties": {"tags": ["HIGH"]}},
                                {"properties": {"tags": ["HIGH"]}},
                                {"properties": {"tags": ["HIGH"]}},
                                {"properties": {"tags": ["MEDIUM"]}},
                                {"properties": {"tags": ["LOW"]}},
                            ]
                        }
                    }
                }
            ]
        }

        # Write to temporary file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".sarif", delete=False) as f:
            json.dump(sarif_data, f)
            temp_path = f.name

        try:
            result = self.parser.parse(temp_path)

            self.assertEqual(result.critical, 2)
            self.assertEqual(result.high, 3)
            self.assertEqual(result.medium, 1)
            self.assertEqual(result.low, 1)
            self.assertTrue(result.has_critical())
            self.assertTrue(result.has_high())

        finally:
            Path(temp_path).unlink()

    def test_parse_empty_sarif(self):
        """Test parsing SARIF with no vulnerabilities."""
        sarif_data = {"runs": [{"tool": {"driver": {"rules": []}}}]}

        with tempfile.NamedTemporaryFile(mode="w", suffix=".sarif", delete=False) as f:
            json.dump(sarif_data, f)
            temp_path = f.name

        try:
            result = self.parser.parse(temp_path)

            self.assertEqual(result.critical, 0)
            self.assertEqual(result.high, 0)
            self.assertEqual(result.medium, 0)
            self.assertEqual(result.low, 0)
            self.assertFalse(result.has_critical())
            self.assertFalse(result.has_high())

        finally:
            Path(temp_path).unlink()

    def test_parse_nonexistent_file(self):
        """Test parsing when SARIF file doesn't exist."""
        result = self.parser.parse("nonexistent.sarif")

        # Should return zero counts gracefully
        self.assertEqual(result.critical, 0)
        self.assertEqual(result.high, 0)
        self.assertEqual(result.medium, 0)
        self.assertEqual(result.low, 0)

    def test_parse_invalid_json(self):
        """Test parsing malformed SARIF JSON."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".sarif", delete=False) as f:
            f.write("{ invalid json }")
            temp_path = f.name

        try:
            result = self.parser.parse(temp_path)

            # Should return zero counts gracefully
            self.assertEqual(result.critical, 0)
            self.assertEqual(result.high, 0)

        finally:
            Path(temp_path).unlink()

    def test_parse_text_fallback(self):
        """Test text-based fallback parser."""
        text_content = """
        CVE-2024-1234 CRITICAL vulnerability in package1
        CVE-2024-5678 CRITICAL vulnerability in package2
        CVE-2024-9012 HIGH vulnerability in package3
        CVE-2024-3456 MEDIUM vulnerability in package4
        CVE-2024-7890 LOW vulnerability in package5
        """

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write(text_content)
            temp_path = f.name

        try:
            result = self.parser.parse_text_fallback(temp_path)

            self.assertEqual(result.critical, 2)
            self.assertEqual(result.high, 1)
            self.assertEqual(result.medium, 1)
            self.assertEqual(result.low, 1)

        finally:
            Path(temp_path).unlink()

    def test_parse_multiple_runs(self):
        """Test parsing SARIF with multiple runs."""
        sarif_data = {
            "runs": [
                {
                    "tool": {
                        "driver": {
                            "rules": [
                                {"properties": {"tags": ["CRITICAL"]}},
                                {"properties": {"tags": ["HIGH"]}},
                            ]
                        }
                    }
                },
                {
                    "tool": {
                        "driver": {
                            "rules": [
                                {"properties": {"tags": ["CRITICAL"]}},
                                {"properties": {"tags": ["MEDIUM"]}},
                            ]
                        }
                    }
                },
            ]
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".sarif", delete=False) as f:
            json.dump(sarif_data, f)
            temp_path = f.name

        try:
            result = self.parser.parse(temp_path)

            # Should count from both runs
            self.assertEqual(result.critical, 2)
            self.assertEqual(result.high, 1)
            self.assertEqual(result.medium, 1)
            self.assertEqual(result.low, 0)

        finally:
            Path(temp_path).unlink()


if __name__ == "__main__":
    unittest.main()
