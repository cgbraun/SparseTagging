"""Parser for Docker smoke test results."""

from pathlib import Path

from models.scan_result import SmokeTestResults


class SmokeTestParser:
    """Parse Docker smoke test results."""

    def parse(self, results_file: str | Path) -> SmokeTestResults | None:
        """Parse smoke test results file.

        Args:
            results_file: Path to docker-smoke-test-results.txt

        Returns:
            SmokeTestResults if file exists, None otherwise

        Expected format in results file:
            TEST1=PASSED
            TEST2=PASSED
            TEST3=PASSED
            VERSION=2.4.1
        """
        results_path = Path(results_file)

        if not results_path.exists():
            return None

        try:
            with open(results_path, encoding="utf-8") as f:
                content = f.read()

            # Extract test results
            test1 = self._extract_value(content, "TEST1")
            test2 = self._extract_value(content, "TEST2")
            test3 = self._extract_value(content, "TEST3")
            version = self._extract_value(content, "VERSION")

            return SmokeTestResults(
                test1_status=test1 or "N/A",
                test2_status=test2 or "N/A",
                test3_status=test3 or "N/A",
                version=version or "N/A",
            )

        except OSError as e:
            print(f"Warning: Failed to read smoke test results: {e}")
            return None

    def _extract_value(self, content: str, key: str) -> str | None:
        """Extract value for a given key from content.

        Args:
            content: File content
            key: Key to search for (e.g., "TEST1")

        Returns:
            Value string or None if not found
        """
        for line in content.splitlines():
            if line.startswith(f"{key}="):
                return line.split("=", 1)[1].strip()
        return None
