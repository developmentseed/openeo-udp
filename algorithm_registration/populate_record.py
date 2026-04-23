#!/usr/bin/env python3
"""
Populate records/records_template.json with metadata from a notebook's metadata cell.

Usage:
    python populate_record.py <path-to-notebook>

Example:
    python populate_record.py ../notebooks/sentinel/sentinel-2/fire_and_disaster_monitoring/fire_boundary_2.ipynb
"""
import base64
import json
import os
import re
import sys
from pathlib import Path

from PIL import Image


def extract_metadata_from_notebook(notebook_path: Path) -> dict:
    """Find the cell containing 'metadata = {' and execute it to get the dict."""
    with open(notebook_path) as f:
        nb = json.load(f)

    metadata_source = next(
        (
            "".join(cell["source"])
            for cell in nb["cells"]
            if cell["cell_type"] == "code"
            and "notebook_metadata" in cell.get("metadata", {}).get("tags", [])
        ),
        None,
    )

    if metadata_source is None:
        raise ValueError(f"No code cell tagged 'notebook_metadata' found in {notebook_path}")

    # Execute the cell in the notebook's directory so Path.cwd() resolves correctly
    exec_globals = {"Path": Path, "json": json}
    original_cwd = os.getcwd()
    os.chdir(notebook_path.parent)
    try:
        exec(metadata_source, exec_globals)
    finally:
        os.chdir(original_cwd)

    if "metadata" not in exec_globals:
        raise ValueError("Cell executed but 'metadata' variable was not defined")

    return exec_globals["metadata"]


def fill_template(template_str: str, metadata: dict) -> dict:
    """Replace all {{PLACEHOLDER}} markers in the template string with metadata values."""

    # --- Structured (list/object) replacements first ---
    template_str = template_str.replace(
        '"{{KEYWORDS}}"',
        json.dumps(metadata["keywords"])
    )
    template_str = template_str.replace(
        '"{{THEMES}}"',
        json.dumps([{"id": t} for t in metadata.get("themes", [])])
    )

    # --- Simple string replacements ---
    replacements = {
        "{{ID}}":                   metadata["id"],
        "{{TITLE}}":                metadata["title"],
        "{{DESCRIPTION}}":          metadata["description"],
        "{{CREATED}}":              metadata["created"],
        "{{UPDATED}}":              metadata["updated"],
        "{{LICENSE}}":              metadata["license"],
        "{{NOTEBOOK_PATH}}":        metadata.get("notebook_github_location", ""),
        "{{TARGET_OPENEO_BACKEND}}": metadata.get("openeo_backend_url", ""),
        "{{PREVIEW_TITLE}}":        metadata.get("preview_title", "{{PREVIEW_TITLE}}"),
    }

    for placeholder, value in replacements.items():
        template_str = template_str.replace(placeholder, value)

    # Warn about any placeholders that couldn't be filled
    remaining = re.findall(r"\{\{[A-Z_]+\}\}", template_str)
    if remaining:
        print(f"Warning: unfilled placeholders: {', '.join(set(remaining))}")

    return json.loads(template_str)


def export_images(notebook_path: Path, records_dir: Path) -> None:
    """Extract the preview_image-tagged cell output and write preview.png and thumbnail.png."""
    with open(notebook_path) as f:
        nb = json.load(f)

    preview_cell = next(
        (
            cell
            for cell in nb["cells"]
            if cell["cell_type"] == "code"
            and "preview_image" in cell.get("metadata", {}).get("tags", [])
        ),
        None,
    )

    if preview_cell is None:
        print("Warning: no cell tagged 'preview_image' found — skipping image export")
        return

    png_b64 = next(
        (
            output["data"]["image/png"]
            for output in preview_cell.get("outputs", [])
            if output.get("output_type") in ("display_data", "execute_result")
            and "image/png" in output.get("data", {})
        ),
        None,
    )

    if png_b64 is None:
        print("Warning: preview_image cell has no image/png output — skipping image export")
        return

    png_bytes = base64.b64decode(png_b64)

    preview_path = records_dir / "preview.png"
    preview_path.write_bytes(png_bytes)
    print(f"Preview written: {preview_path}")

    with Image.open(preview_path) as img:
        thumb = img.resize((img.width // 2, img.height // 2), Image.LANCZOS)
        thumb_path = records_dir / "thumbnail.png"
        thumb.save(thumb_path)
    print(f"Thumbnail written: {thumb_path}")


def run(notebook_path: Path) -> Path:
    """Extract metadata from notebook and write the record JSON. Returns the output path."""
    notebook_path = Path(notebook_path).resolve()
    script_dir = Path(__file__).parent
    template_path = script_dir / "records_template.json"

    print(f"Notebook : {notebook_path}")
    print(f"Template : {template_path}")

    metadata = extract_metadata_from_notebook(notebook_path)
    print(f"Metadata extracted — id: '{metadata['id']}'")

    with open(template_path) as f:
        template_str = f.read()

    record = fill_template(template_str, metadata)

    output_path = script_dir / metadata["id"] / "records" / f"{metadata['id']}.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(record, f, indent=2)

    print(f"Record written: {output_path}")

    export_images(notebook_path, output_path.parent)

    return output_path


def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {Path(__file__).name} <path-to-notebook>")
        sys.exit(1)

    notebook_path = Path(sys.argv[1])
    if not notebook_path.exists():
        print(f"Error: notebook not found: {notebook_path}")
        sys.exit(1)

    run(notebook_path)


if __name__ == "__main__":
    main()
