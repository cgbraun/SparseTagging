#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SonarCloud Issue Fetcher for SparseTagging

Fetches code quality issues from SonarCloud and CVEs from pip-audit,
then presents them for automated fixing.

Usage:
    python scripts/fetch_sonar_issues.py

    CGBraun, Jan 2026
"""

import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

# Fix Windows console encoding for emoji support
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        # Python < 3.7
        import codecs
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
        sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, "strict")

try:
    import requests
    from dotenv import load_dotenv
except ImportError:
    print("❌ ERROR: Missing dependencies. Please install:")
    print("   pip install requests python-dotenv pip-audit")
    sys.exit(1)


# Load environment variables
load_dotenv()

# Configuration
SONAR_TOKEN = os.getenv("SONAR_TOKEN")
PROJECT_KEY = os.getenv("SONAR_PROJECT_KEY", "vonbraun_SparseTagging")
ORGANIZATION = os.getenv("SONAR_ORGANIZATION", "vonbraun")
BASE_URL = "https://sonarcloud.io/api"

# Severity ordering for display
SEVERITY_ORDER = ["BLOCKER", "CRITICAL", "MAJOR", "MINOR", "INFO"]
TYPE_ORDER = ["BUG", "VULNERABILITY", "SECURITY_HOTSPOT", "CODE_SMELL"]


@dataclass
class Issue:
    """Represents a SonarCloud issue."""

    key: str
    rule: str
    severity: str
    type: str
    message: str
    component: str
    line: Optional[int]
    status: str

    @property
    def file_path(self) -> str:
        """Extract readable file path from component."""
        # Component format: "vonbraun_SparseTagging:src/sparsetag.py"
        parts = self.component.split(":", 1)
        return parts[1] if len(parts) > 1 else self.component

    @property
    def location(self) -> str:
        """Return formatted location string."""
        if self.line:
            return f"{self.file_path}:{self.line}"
        return self.file_path

    def __str__(self) -> str:
        """Format issue for display."""
        severity_emoji = {
            "BLOCKER": "🔴",
            "CRITICAL": "🔴",
            "MAJOR": "🟠",
            "MINOR": "🟡",
            "INFO": "🔵",
        }
        type_emoji = {
            "BUG": "🐛",
            "VULNERABILITY": "🔒",
            "SECURITY_HOTSPOT": "🔥",
            "CODE_SMELL": "💨",
        }

        emoji = severity_emoji.get(self.severity, "⚪")
        type_icon = type_emoji.get(self.type, "📋")

        return (
            f"{emoji} [{self.severity}] {type_icon} {self.type}\n"
            f"   Rule: {self.rule}\n"
            f"   Location: {self.location}\n"
            f"   Message: {self.message}"
        )


@dataclass
class CVE:
    """Represents a CVE from pip-audit."""

    package: str
    version: str
    cve_id: str
    severity: str
    description: str
    fixed_version: Optional[str]

    def __str__(self) -> str:
        """Format CVE for display."""
        severity_emoji = {
            "HIGH": "🔴",
            "MEDIUM": "🟠",
            "LOW": "🟡",
            "UNKNOWN": "⚪",
        }
        emoji = severity_emoji.get(self.severity.upper(), "⚪")

        fixed = f" → Fix: upgrade to {self.fixed_version}" if self.fixed_version else ""
        return (
            f"{emoji} {self.cve_id} - {self.package} {self.version}\n"
            f"   Severity: {self.severity}\n"
            f"   {self.description}{fixed}"
        )


class SonarCloudClient:
    """Client for SonarCloud API."""

    def __init__(self, token: str, project_key: str, organization: str):
        if not token:
            raise ValueError(
                "SONAR_TOKEN not found. Please set it in .env file or environment."
            )
        self.token = token
        self.project_key = project_key
        self.organization = organization
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def get_issues(self, resolved: bool = False) -> List[Issue]:
        """Fetch issues from SonarCloud."""
        url = f"{BASE_URL}/issues/search"
        params = {
            "componentKeys": self.project_key,
            "resolved": str(resolved).lower(),
            "ps": 500,  # Page size
        }

        try:
            response = requests.get(url, params=params, headers=self.headers, timeout=30)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"❌ ERROR: Failed to fetch issues from SonarCloud: {e}")
            if hasattr(e, "response") and e.response is not None:
                print(f"   Status: {e.response.status_code}")
                print(f"   Response: {e.response.text[:200]}")
            sys.exit(1)

        data = response.json()
        issues = []

        for issue_data in data.get("issues", []):
            issue = Issue(
                key=issue_data["key"],
                rule=issue_data["rule"],
                severity=issue_data["severity"],
                type=issue_data["type"],
                message=issue_data["message"],
                component=issue_data.get("component", "N/A"),
                line=issue_data.get("line"),
                status=issue_data["status"],
            )
            issues.append(issue)

        return issues

    def get_quality_gate(self) -> Dict[str, Any]:
        """Get quality gate status."""
        url = f"{BASE_URL}/qualitygates/project_status"
        params = {"projectKey": self.project_key}

        try:
            response = requests.get(url, params=params, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"⚠️  WARNING: Failed to fetch quality gate: {e}")
            return {}


def run_pip_audit() -> List[CVE]:
    """Run pip-audit to find CVEs in dependencies."""
    print("\n🔍 Scanning for CVEs with pip-audit...")

    try:
        result = subprocess.run(
            ["pip-audit", "--format", "json", "-r", "requirements.txt"],
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode == 0:
            print("✅ No CVEs found in dependencies")
            return []

        # Parse JSON output
        try:
            data = json.loads(result.stdout)
            cves = []

            for vuln in data.get("vulnerabilities", []):
                cve = CVE(
                    package=vuln.get("name", "unknown"),
                    version=vuln.get("version", "unknown"),
                    cve_id=vuln.get("id", "unknown"),
                    severity=vuln.get("severity", "UNKNOWN"),
                    description=vuln.get("description", "No description"),
                    fixed_version=vuln.get("fix_versions", [None])[0],
                )
                cves.append(cve)

            return cves
        except json.JSONDecodeError:
            print(f"⚠️  WARNING: Could not parse pip-audit output")
            return []

    except FileNotFoundError:
        print("⚠️  WARNING: pip-audit not found. Install with: pip install pip-audit")
        return []
    except subprocess.TimeoutExpired:
        print("⚠️  WARNING: pip-audit timed out")
        return []
    except Exception as e:
        print(f"⚠️  WARNING: pip-audit failed: {e}")
        return []


def display_summary(issues: List[Issue], cves: List[CVE]) -> None:
    """Display summary of issues and CVEs."""
    print("\n" + "=" * 80)
    print("📊 SONARCLOUD ISSUES SUMMARY")
    print("=" * 80)

    # Group by severity
    by_severity: Dict[str, List[Issue]] = {}
    for issue in issues:
        by_severity.setdefault(issue.severity, []).append(issue)

    # Group by type
    by_type: Dict[str, List[Issue]] = {}
    for issue in issues:
        by_type.setdefault(issue.type, []).append(issue)

    print(f"\n📈 Total Issues: {len(issues)}")
    print("\nBy Severity:")
    for severity in SEVERITY_ORDER:
        count = len(by_severity.get(severity, []))
        if count > 0:
            emoji = {"BLOCKER": "🔴", "CRITICAL": "🔴", "MAJOR": "🟠", "MINOR": "🟡", "INFO": "🔵"}
            print(f"  {emoji.get(severity, '⚪')} {severity}: {count}")

    print("\nBy Type:")
    for issue_type in TYPE_ORDER:
        count = len(by_type.get(issue_type, []))
        if count > 0:
            emoji = {"BUG": "🐛", "VULNERABILITY": "🔒", "SECURITY_HOTSPOT": "🔥", "CODE_SMELL": "💨"}
            print(f"  {emoji.get(issue_type, '📋')} {issue_type}: {count}")

    # CVE summary
    if cves:
        print(f"\n🔒 CVEs Found: {len(cves)}")
        cve_by_severity: Dict[str, int] = {}
        for cve in cves:
            cve_by_severity[cve.severity.upper()] = cve_by_severity.get(cve.severity.upper(), 0) + 1

        for severity in ["HIGH", "MEDIUM", "LOW", "UNKNOWN"]:
            count = cve_by_severity.get(severity, 0)
            if count > 0:
                emoji = {"HIGH": "🔴", "MEDIUM": "🟠", "LOW": "🟡", "UNKNOWN": "⚪"}
                print(f"  {emoji[severity]} {severity}: {count}")


def display_issues(issues: List[Issue], cves: List[CVE]) -> None:
    """Display detailed issues."""
    print("\n" + "=" * 80)
    print("📋 DETAILED ISSUES")
    print("=" * 80)

    # Sort by severity then type
    severity_rank = {s: i for i, s in enumerate(SEVERITY_ORDER)}
    type_rank = {t: i for i, t in enumerate(TYPE_ORDER)}

    sorted_issues = sorted(
        issues,
        key=lambda x: (severity_rank.get(x.severity, 99), type_rank.get(x.type, 99)),
    )

    for i, issue in enumerate(sorted_issues, 1):
        print(f"\n[{i}] {issue}")

    if cves:
        print("\n" + "=" * 80)
        print("🔒 CVE DETAILS")
        print("=" * 80)
        for i, cve in enumerate(cves, 1):
            print(f"\n[CVE-{i}] {cve}")


def get_user_selection(issues: List[Issue], cves: List[CVE]) -> tuple[List[Issue], List[CVE]]:
    """Interactive selection of issues to fix."""
    print("\n" + "=" * 80)
    print("🔧 ISSUE SELECTION")
    print("=" * 80)
    print("\nWhat would you like Claude to fix?")
    print("\nOptions:")
    print("  ALL       - Fix all issues and CVEs")
    print("  NONE      - Don't fix anything (exit)")
    print("  HIGH      - Fix only BLOCKER/CRITICAL issues + HIGH CVEs")
    print("  MEDIUM    - Fix MAJOR+ issues + MEDIUM+ CVEs")
    print("  BUGS      - Fix only bugs and vulnerabilities")
    print("  CVES      - Fix only CVEs")
    print("  ISSUES    - Fix only SonarCloud issues (no CVEs)")
    print("  CUSTOM    - Select specific issues by number")

    while True:
        choice = input("\n👉 Enter your choice: ").strip().upper()

        if choice == "NONE":
            print("✅ No issues selected. Exiting.")
            return [], []

        if choice == "ALL":
            return issues, cves

        if choice == "HIGH":
            selected_issues = [i for i in issues if i.severity in ["BLOCKER", "CRITICAL"]]
            selected_cves = [c for c in cves if c.severity.upper() == "HIGH"]
            return selected_issues, selected_cves

        if choice == "MEDIUM":
            selected_issues = [i for i in issues if i.severity in ["BLOCKER", "CRITICAL", "MAJOR"]]
            selected_cves = [c for c in cves if c.severity.upper() in ["HIGH", "MEDIUM"]]
            return selected_issues, selected_cves

        if choice == "BUGS":
            selected_issues = [i for i in issues if i.type in ["BUG", "VULNERABILITY", "SECURITY_HOTSPOT"]]
            return selected_issues, cves

        if choice == "CVES":
            return [], cves

        if choice == "ISSUES":
            return issues, []

        if choice == "CUSTOM":
            print("\n📝 Enter issue numbers separated by commas (e.g., 1,3,5)")
            print(f"   Issues: 1-{len(issues)}")
            if cves:
                print(f"   CVEs: CVE-1 to CVE-{len(cves)}")

            selection = input("👉 Selection: ").strip()
            selected_issues = []
            selected_cves = []

            for item in selection.split(","):
                item = item.strip()
                if item.startswith("CVE-"):
                    try:
                        idx = int(item.replace("CVE-", "")) - 1
                        if 0 <= idx < len(cves):
                            selected_cves.append(cves[idx])
                    except ValueError:
                        print(f"⚠️  Invalid CVE number: {item}")
                else:
                    try:
                        idx = int(item) - 1
                        if 0 <= idx < len(issues):
                            selected_issues.append(issues[idx])
                    except ValueError:
                        print(f"⚠️  Invalid issue number: {item}")

            return selected_issues, selected_cves

        print(f"❌ Invalid choice: {choice}. Please try again.")


def format_for_claude(issues: List[Issue], cves: List[CVE]) -> None:
    """Format selected issues for Claude to fix."""
    print("\n" + "=" * 80)
    print("🤖 ISSUES SELECTED FOR CLAUDE")
    print("=" * 80)

    if not issues and not cves:
        print("\n✅ No issues selected.")
        return

    print(f"\n📊 Total: {len(issues)} SonarCloud issues + {len(cves)} CVEs")

    if issues:
        print("\n" + "-" * 80)
        print("SONARCLOUD ISSUES:")
        print("-" * 80)
        for i, issue in enumerate(issues, 1):
            print(f"\n{i}. {issue}")

    if cves:
        print("\n" + "-" * 80)
        print("CVEs TO FIX:")
        print("-" * 80)
        for i, cve in enumerate(cves, 1):
            print(f"\n{i}. {cve}")

    print("\n" + "=" * 80)
    print("✅ Ready for Claude to fix!")
    print("=" * 80)


def main() -> None:
    """Main execution."""
    print("🚀 SonarCloud Issue Fetcher for SparseTagging")
    print("=" * 80)

    # Initialize client
    try:
        client = SonarCloudClient(SONAR_TOKEN, PROJECT_KEY, ORGANIZATION)
    except ValueError as e:
        print(f"❌ ERROR: {e}")
        print("\n💡 To fix:")
        print("   1. Create .env file in project root")
        print("   2. Add: SONAR_TOKEN=your_token_here")
        print("   3. Generate token at: https://sonarcloud.io/account/security")
        sys.exit(1)

    # Fetch issues
    print(f"\n🔍 Fetching issues from SonarCloud...")
    print(f"   Project: {PROJECT_KEY}")
    print(f"   Organization: {ORGANIZATION}")

    issues = client.get_issues(resolved=False)
    print(f"✅ Found {len(issues)} open issues")

    # Fetch CVEs
    cves = run_pip_audit()

    if not issues and not cves:
        print("\n🎉 No issues or CVEs found! Your code is clean!")
        return

    # Display summary and details
    display_summary(issues, cves)
    display_issues(issues, cves)

    # Get quality gate status
    qg = client.get_quality_gate()
    if qg:
        status = qg.get("projectStatus", {}).get("status", "UNKNOWN")
        emoji = "✅" if status == "OK" else "❌"
        print(f"\n{emoji} Quality Gate: {status}")

    # Interactive selection
    selected_issues, selected_cves = get_user_selection(issues, cves)

    # Format for Claude
    format_for_claude(selected_issues, selected_cves)


if __name__ == "__main__":
    main()
