"""Parser for Trivy SARIF vulnerability scan results."""

import json
from pathlib import Path

from models.scan_result import VulnerabilityCount


class TrivyParser:
    """Parse Trivy SARIF output to extract vulnerability counts by severity."""

    def parse(self, sarif_path: str | Path) -> VulnerabilityCount:
        """Parse Trivy SARIF file for vulnerability counts.

        Args:
            sarif_path: Path to trivy-results.sarif file

        Returns:
            VulnerabilityCount with counts by severity

        Note:
            Trivy stores vulnerabilities in .runs[].tool.driver.rules[], not .runs[].results[].
            Each rule has properties.tags[] containing severity levels.
        """
        sarif_path = Path(sarif_path)

        if not sarif_path.exists():
            # Return zero counts if SARIF file doesn't exist
            return VulnerabilityCount(critical=0, high=0, medium=0, low=0)

        try:
            with open(sarif_path, encoding="utf-8") as f:
                sarif = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            print(f"Warning: Failed to parse SARIF file: {e}")
            return VulnerabilityCount(critical=0, high=0, medium=0, low=0)

        # Count vulnerabilities by severity from rules array
        counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}

        # Navigate to rules array in SARIF structure
        runs = sarif.get("runs", [])
        for run in runs:
            tool = run.get("tool", {})
            driver = tool.get("driver", {})
            rules = driver.get("rules", [])

            for rule in rules:
                properties = rule.get("properties", {})
                tags = properties.get("tags", [])

                # Check each tag for severity levels
                # Note: Tags are uppercase in SARIF (e.g., "CRITICAL", "HIGH")
                for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
                    if severity in tags:
                        counts[severity.lower()] += 1

        return VulnerabilityCount(
            critical=counts["critical"],
            high=counts["high"],
            medium=counts["medium"],
            low=counts["low"],
        )

    def parse_text_fallback(self, text_report_path: str | Path) -> VulnerabilityCount:
        """Fallback parser for text-based Trivy reports (less accurate).

        Args:
            text_report_path: Path to trivy-report.txt file

        Returns:
            VulnerabilityCount with approximate counts

        Note:
            This is less accurate than SARIF parsing because it counts occurrences
            of severity keywords, which may include duplicates or false matches.
        """
        text_path = Path(text_report_path)

        if not text_path.exists():
            return VulnerabilityCount(critical=0, high=0, medium=0, low=0)

        try:
            with open(text_path, encoding="utf-8") as f:
                content = f.read()
        except OSError as e:
            print(f"Warning: Failed to read text report: {e}")
            return VulnerabilityCount(critical=0, high=0, medium=0, low=0)

        # Count occurrences of severity keywords (simple but less accurate)
        counts = {
            "critical": content.count("CRITICAL"),
            "high": content.count("HIGH"),
            "medium": content.count("MEDIUM"),
            "low": content.count("LOW"),
        }

        return VulnerabilityCount(
            critical=counts["critical"],
            high=counts["high"],
            medium=counts["medium"],
            low=counts["low"],
        )
