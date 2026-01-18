#!/usr/bin/env python3
"""
Mermaid Diagram Converter - Extract and render diagrams from markdown to PNG

This script extracts Mermaid diagrams from TUTORIAL_DIAGRAMS_SLIDES.md,
renders them as PNG images using mermaid-cli (mmdc), and generates a
manifest.json file with metadata for each diagram.

Usage:
    python convert_diagrams.py

Requirements:
    - Node.js and npm installed
    - mermaid-cli: npm install -g @mermaid-js/mermaid-cli
    - Python 3.9+

Output:
    - PNG files in docs/diagrams/
    - manifest.json in docs/diagrams/
"""

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import TypedDict


class DiagramMetadata(TypedDict):
    """Metadata for a single diagram."""

    number: int
    title: str
    slug: str
    filename: str
    summary: str
    purpose: str
    usage: str
    mermaid_code: str


class DiagramExtractor:
    """Extract Mermaid diagrams and metadata from markdown files."""

    def __init__(self, markdown_file: Path):
        self.markdown_file = markdown_file
        self.content = markdown_file.read_text(encoding="utf-8")

    def extract_diagrams(self) -> list[DiagramMetadata]:
        """Extract all diagrams with metadata from the markdown file."""
        diagrams: list[DiagramMetadata] = []

        # Pattern to match diagram sections: ### N. Title
        section_pattern = r"^### (\d+)\.\s+(.+?)$"

        # Split content by diagram sections
        sections = re.split(r"^(###\s+\d+\.)", self.content, flags=re.MULTILINE)

        # Process sections (skipping first which is before any diagram)
        i = 1
        while i < len(sections):
            # sections[i] is the header marker (### 1.)
            # sections[i+1] is the content after that header
            if i + 1 < len(sections):
                header = sections[i] + (sections[i + 1].split("\n")[0] if sections[i + 1] else "")
                content = sections[i + 1] if i + 1 < len(sections) else ""

                # Extract number and title
                match = re.match(section_pattern, header.strip())
                if match:
                    number = int(match.group(1))
                    title = match.group(2).strip()

                    # Extract metadata and mermaid code
                    diagram = self._parse_diagram_section(number, title, content)
                    if diagram:
                        diagrams.append(diagram)

            i += 2

        return diagrams

    def _parse_diagram_section(
        self, number: int, title: str, content: str
    ) -> DiagramMetadata | None:
        """Parse a single diagram section for metadata and code."""
        # Extract Summary
        summary_match = re.search(
            r"\*\*Summary\*\*:\s*(.+?)(?=\n\n|\*\*Purpose\*\*)", content, re.DOTALL
        )
        summary = summary_match.group(1).strip() if summary_match else ""

        # Extract Purpose
        purpose_match = re.search(
            r"\*\*Purpose\*\*:\s*(.+?)(?=\n\n|\*\*Usage\*\*)", content, re.DOTALL
        )
        purpose = purpose_match.group(1).strip() if purpose_match else ""

        # Extract Usage
        usage_match = re.search(r"\*\*Usage\*\*:\s*(.+?)(?=\n\n|```mermaid)", content, re.DOTALL)
        usage = usage_match.group(1).strip() if usage_match else ""

        # Extract Mermaid code block
        mermaid_match = re.search(r"```mermaid\n(.*?)\n```", content, re.DOTALL)
        if not mermaid_match:
            print(f"Warning: No Mermaid code found for diagram {number}: {title}")
            return None

        mermaid_code = mermaid_match.group(1).strip()

        # Create slug from title
        slug = self._create_slug(title)

        return DiagramMetadata(
            number=number,
            title=title,
            slug=slug,
            filename=f"{slug}.png",
            summary=summary,
            purpose=purpose,
            usage=usage,
            mermaid_code=mermaid_code,
        )

    @staticmethod
    def _create_slug(title: str) -> str:
        """Convert title to URL-friendly slug."""
        # Remove special characters, convert to lowercase, replace spaces with hyphens
        slug = title.lower()
        slug = re.sub(r"[^\w\s-]", "", slug)
        slug = re.sub(r"[-\s]+", "-", slug)
        return slug.strip("-")


class DiagramRenderer:
    """Render Mermaid diagrams to PNG using mermaid-cli."""

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir = output_dir / ".temp"
        self.temp_dir.mkdir(exist_ok=True)

    def check_mmdc_installed(self) -> bool:
        """Check if mermaid-cli (mmdc) is installed."""
        mmdc_path = shutil.which("mmdc")
        if mmdc_path is None:
            return False

        try:
            result = subprocess.run(
                [mmdc_path, "--version"],
                capture_output=True,
                text=True,
                check=False,
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False

    def render_diagram(self, diagram: DiagramMetadata) -> bool:
        """Render a single diagram to PNG."""
        # Write Mermaid code to temporary .mmd file
        temp_mmd = self.temp_dir / f"{diagram['slug']}.mmd"
        temp_mmd.write_text(diagram["mermaid_code"], encoding="utf-8")

        # Output PNG path
        output_png = self.output_dir / diagram["filename"]

        # Resolve mmdc path securely (avoids shell=True)
        mmdc_path = shutil.which("mmdc")
        if mmdc_path is None:
            print("[ERROR] mmdc command not found in PATH")
            return False

        # Call mmdc to render
        try:
            cmd = [
                mmdc_path,
                "-i",
                str(temp_mmd),
                "-o",
                str(output_png),
                "-b",
                "transparent",  # Transparent background
                "-w",
                "1024",  # Width 1024px (4:3 aspect ratio)
                "-H",
                "768",  # Height 768px
                "-s",
                "2",  # Scale factor for better quality
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode == 0:
                print(f"[OK] Rendered: {diagram['filename']}")
                return True
            print(f"[FAIL] Failed to render {diagram['filename']}: {result.stderr}")
            return False

        except (FileNotFoundError, OSError, subprocess.SubprocessError) as e:
            print(f"[ERROR] Error rendering {diagram['filename']}: {e}")
            return False

    def cleanup_temp_files(self) -> None:
        """Remove temporary .mmd files."""
        if self.temp_dir.exists():
            for file in self.temp_dir.iterdir():
                file.unlink()
            self.temp_dir.rmdir()


class ManifestGenerator:
    """Generate manifest.json with diagram metadata."""

    @staticmethod
    def generate(diagrams: list[DiagramMetadata], output_file: Path) -> None:
        """Generate manifest.json file."""
        manifest = {
            "metadata": {
                "total_diagrams": len(diagrams),
                "source_file": "docs/TUTORIAL_DIAGRAMS_SLIDES.md",
                "generated_by": "tools/diagram-converter/convert_diagrams.py",
            },
            "diagrams": [
                {
                    "number": d["number"],
                    "title": d["title"],
                    "slug": d["slug"],
                    "filename": d["filename"],
                    "path": f"docs/diagrams/{d['filename']}",
                    "summary": d["summary"],
                    "purpose": d["purpose"],
                    "usage": d["usage"],
                }
                for d in diagrams
            ],
        }

        output_file.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        print(f"\n[OK] Generated manifest: {output_file}")


def main() -> None:
    """Main conversion process."""
    print("=" * 70)
    print("Mermaid Diagram Converter")
    print("=" * 70)

    # Paths
    project_root = Path(__file__).parent.parent.parent
    markdown_file = project_root / "docs" / "TUTORIAL_DIAGRAMS_SLIDES.md"
    output_dir = project_root / "docs" / "diagrams"
    manifest_file = output_dir / "manifest.json"

    # Validate markdown file exists
    if not markdown_file.exists():
        print(f"[ERROR] Error: {markdown_file} not found")
        sys.exit(1)

    # Check mmdc installation
    renderer = DiagramRenderer(output_dir)
    if not renderer.check_mmdc_installed():
        print("[ERROR] Error: mermaid-cli (mmdc) not installed")
        print("\nInstall with: npm install -g @mermaid-js/mermaid-cli")
        sys.exit(1)

    print("[OK] mermaid-cli installed")
    print(f"[OK] Source: {markdown_file}")
    print(f"[OK] Output: {output_dir}")
    print()

    # Extract diagrams
    print("Extracting diagrams from markdown...")
    extractor = DiagramExtractor(markdown_file)
    diagrams = extractor.extract_diagrams()
    print(f"[OK] Found {len(diagrams)} diagrams\n")

    if not diagrams:
        print("[ERROR] No diagrams found in markdown file")
        sys.exit(1)

    # Render diagrams
    print("Rendering diagrams to PNG...")
    success_count = 0
    for diagram in diagrams:
        if renderer.render_diagram(diagram):
            success_count += 1

    print(f"\n[OK] Successfully rendered {success_count}/{len(diagrams)} diagrams")

    # Clean up temp files
    renderer.cleanup_temp_files()

    # Generate manifest
    print("\nGenerating manifest...")
    ManifestGenerator.generate(diagrams, manifest_file)

    print("\n" + "=" * 70)
    print("Conversion complete!")
    print("=" * 70)
    print(f"\nPNG files: {output_dir}")
    print(f"Manifest: {manifest_file}")


if __name__ == "__main__":
    main()
