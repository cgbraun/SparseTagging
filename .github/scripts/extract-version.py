#!/usr/bin/env python3
"""Extract version from pyproject.toml for CI/CD workflows."""

import sys
import tomllib
from pathlib import Path

def get_version() -> str:
    """Read version from pyproject.toml."""
    pyproject_path = Path("pyproject.toml")

    if not pyproject_path.exists():
        print("::error::pyproject.toml not found", file=sys.stderr)
        sys.exit(1)

    try:
        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)

        version = data.get("project", {}).get("version")
        if not version:
            print("::error::Version not found in pyproject.toml", file=sys.stderr)
            sys.exit(1)

        return version

    except Exception as e:
        print(f"::error::Failed to read version: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    version = get_version()
    print(version)
