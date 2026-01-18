# Diagram Usage Examples

This file demonstrates how to use the generated PNG diagrams and manifest.json in various contexts.

## Example 1: Markdown Document with Diagrams

```markdown
# LLM-First Development Tutorial

## Chapter 1: Complete Development Lifecycle

![Complete Development Lifecycle](../docs/diagrams/complete-development-lifecycle.png)

**Summary**: This diagram shows the complete 12-phase development lifecycle organized in four horizontal rows stacked vertically for optimal 4:3 slide format...

**Purpose**: Provide 10,000-foot view of entire development process with quality checkpoints.

---

## Chapter 2: The Plan-Execute-Refine Loop

![LLM Plan-Execute-Refine Loop](../docs/diagrams/llm-plan-execute-refine-loop.png)

**Summary**: This diagram captures the iterative cycle at the heart of LLM-first development...
```

## Example 2: Programmatic Access to Metadata

```python
import json
from pathlib import Path

# Load manifest
manifest_path = Path("docs/diagrams/manifest.json")
with open(manifest_path) as f:
    manifest = json.load(f)

# Print all diagram titles
print(f"Total diagrams: {manifest['metadata']['total_diagrams']}")
print("\nDiagrams:")
for diagram in manifest['diagrams']:
    print(f"  {diagram['number']}. {diagram['title']}")
    print(f"     File: {diagram['filename']}")
    print(f"     Usage: {diagram['usage']}")
    print()

# Find specific diagram
phase_0 = next(d for d in manifest['diagrams'] if d['number'] == 4)
print(f"\nPhase 0 Details:")
print(f"  Title: {phase_0['title']}")
print(f"  Path: {phase_0['path']}")
print(f"  Summary: {phase_0['summary'][:100]}...")
```

**Output:**
```
Total diagrams: 15

Diagrams:
  1. Complete Development Lifecycle
     File: complete-development-lifecycle.png
     Usage: Tutorial introduction to show complete journey from idea to published package.

  2. Tool Ecosystem Map
     File: tool-ecosystem-map.png
     Usage: Architecture overview to understand tool selection, configuration order, and integration points.

  ...
```

## Example 3: Generating HTML Documentation

```python
import json
from pathlib import Path

manifest_path = Path("docs/diagrams/manifest.json")
with open(manifest_path) as f:
    manifest = json.load(f)

html = []
html.append("<html><head><title>Tutorial Diagrams</title></head><body>")
html.append("<h1>LLM-First Development Tutorial Diagrams</h1>")

for diagram in manifest['diagrams']:
    html.append(f"<h2>{diagram['number']}. {diagram['title']}</h2>")
    html.append(f"<img src='{diagram['path']}' alt='{diagram['title']}' style='max-width:100%;'/>")
    html.append(f"<p><strong>Purpose:</strong> {diagram['purpose']}</p>")
    html.append(f"<p><strong>Summary:</strong> {diagram['summary']}</p>")
    html.append(f"<p><strong>Usage:</strong> {diagram['usage']}</p>")
    html.append("<hr/>")

html.append("</body></html>")

output_file = Path("docs/diagrams_gallery.html")
output_file.write_text('\n'.join(html))
print(f"Generated: {output_file}")
```

## Example 4: PowerPoint Integration (Manual)

1. **Open PowerPoint** and create a new presentation
2. **For each phase**, create a new slide:
   - **Title**: Use the diagram title from manifest.json (e.g., "Phase 0: Concept to Requirements")
   - **Insert Image**: Insert → Picture → Browse to `docs/diagrams/phase-0-concept-to-requirements.png`
   - **Resize**: Scale to fit slide (diagrams are 1024x768px, 4:3 ratio)
   - **Add Text Box**: Insert the "purpose" from manifest.json as subtitle
   - **Speaker Notes**: Add the full "summary" from manifest.json

3. **Automated approach** (using python-pptx):

```python
from pptx import Presentation
from pptx.util import Inches
import json

# Load manifest
with open("docs/diagrams/manifest.json") as f:
    manifest = json.load(f)

# Create presentation
prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(7.5)

for diagram in manifest['diagrams']:
    # Add blank slide
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # Add title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.5))
    title_frame = title_box.text_frame
    title_frame.text = diagram['title']

    # Add image (centered)
    left = Inches(1)
    top = Inches(1.5)
    width = Inches(8)
    pic = slide.shapes.add_picture(diagram['path'], left, top, width=width)

    # Add notes
    notes_slide = slide.notes_slide
    notes_slide.notes_text_frame.text = f"{diagram['summary']}\n\nPurpose: {diagram['purpose']}\n\nUsage: {diagram['usage']}"

# Save presentation
prs.save("docs/tutorial_diagrams.pptx")
print("PowerPoint presentation created!")
```

## Example 5: Markdown with Metadata Tables

```markdown
# Diagram Reference

| # | Title | Purpose | File |
|---|-------|---------|------|
| 1 | Complete Development Lifecycle | Provide 10,000-foot view of entire development process | [PNG](diagrams/complete-development-lifecycle.png) |
| 2 | Tool Ecosystem Map | Show interconnected tool landscape | [PNG](diagrams/tool-ecosystem-map.png) |
| 3 | LLM Plan-Execute-Refine Loop | Show iterative planning-execution-validation cycle | [PNG](diagrams/llm-plan-execute-refine-loop.png) |

## Diagram 1: Complete Development Lifecycle

![Complete Development Lifecycle](diagrams/complete-development-lifecycle.png)

**Summary**: This diagram shows the complete 12-phase development lifecycle...

**Purpose**: Provide 10,000-foot view of entire development process with quality checkpoints.

**Usage**: Tutorial introduction to show complete journey from idea to published package.

---
```

## Example 6: JSON Processing with jq

```bash
# Get all diagram titles
jq '.diagrams[].title' docs/diagrams/manifest.json

# Get diagram by number
jq '.diagrams[] | select(.number == 5)' docs/diagrams/manifest.json

# Get all Phase diagrams
jq '.diagrams[] | select(.title | startswith("Phase"))' docs/diagrams/manifest.json

# Extract just filenames
jq '.diagrams[].filename' docs/diagrams/manifest.json

# Count diagrams
jq '.metadata.total_diagrams' docs/diagrams/manifest.json

# Create CSV of titles and files
jq -r '.diagrams[] | [.number, .title, .filename] | @csv' docs/diagrams/manifest.json
```

## Example 7: Word Document Integration

For Microsoft Word integration:

1. **Manual approach**:
   - Insert diagrams as images: Insert → Pictures
   - Add captions: Right-click image → Insert Caption
   - Use metadata from manifest.json for captions and body text

2. **Automated approach** (using python-docx):

```python
from docx import Document
from docx.shared import Inches
import json

# Load manifest
with open("docs/diagrams/manifest.json") as f:
    manifest = json.load(f)

# Create document
doc = Document()
doc.add_heading('LLM-First Development Tutorial Diagrams', 0)

for diagram in manifest['diagrams']:
    # Add heading
    doc.add_heading(f"{diagram['number']}. {diagram['title']}", 1)

    # Add image
    doc.add_picture(diagram['path'], width=Inches(6))

    # Add metadata
    doc.add_paragraph(f"Purpose: {diagram['purpose']}", style='Intense Quote')
    doc.add_paragraph(f"Summary: {diagram['summary']}")
    doc.add_paragraph(f"Usage: {diagram['usage']}", style='Quote')

    # Page break after each diagram
    doc.add_page_break()

# Save document
doc.save("docs/tutorial_diagrams.docx")
print("Word document created!")
```

## Notes

- All diagrams are 1024x768px (4:3 aspect ratio) with transparent background
- PNG format ensures compatibility with all document types
- manifest.json provides programmatic access to all metadata
- Diagrams are version-controlled in git at `docs/diagrams/`
- Regenerate anytime by running: `python tools/diagram-converter/convert_diagrams.py`
