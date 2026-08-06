#!/usr/bin/env python3
"""
Populate records/records_template.json with metadata from a notebook's metadata cell.

Usage:
    python populate_record.py <path-to-notebook>

Example:
    python populate_record.py ../notebooks/sentinel/sentinel-2/fire_and_disaster_monitoring/fire_boundary.ipynb
"""

import json
import os
import re
import sys
from pathlib import Path

from PIL import Image

APEX_APPROVED_KEYWORDS = {
    "Agriculture",
    "Land Use/Land Cover Classification",
    "Land Use/Land Cover Change",
    "Deforestation",
    "Vegetation",
    "Normalized Difference Vegetation Index (NDVI)",
    "Leaf Area Index (LAI)",
    "Fraction of Absorbed Photosynthetic Active Radiation (fAPAR)",
    "Fraction of Vegetation Coverage (fCOVER)",
    "Normalized Difference Water Index (NDWI)",
    "Brightness",
    "Energy Production/Use",
    "Wind Energy Production/Use",
    "Solar Energy Production/Use",
    "Natural Hazards",
    "Wildfires",
    "Sentinel-1",
    "Sentinel-2",
    "Sentinel-3",
    "Landsat-8",
    "Digital Elevation/Terrain Model (DEM)",
    "ECMWF ERA5",
    "Data Analysis and Visualization",
    "Statistical Applications",
    "Forests",
    "Statistics",
    "Change Detection Services",
    "Urban Heat Island",
    "Land Surface Temperature",
    "Climate",
    "Soils",
    "Radar",
}


def validate_keywords(keywords: list) -> None:
    """Ensure all keywords are drawn from the approved APEX_APPROVED_KEYWORDS set."""
    invalid = sorted(set(keywords) - APEX_APPROVED_KEYWORDS)
    if invalid:
        raise ValueError(
            f"Invalid keyword(s) in metadata: {invalid}. "
            f"Allowed keywords are: {sorted(APEX_APPROVED_KEYWORDS)}"
        )


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

    # Pre-inject _algorithm_id so the cell doesn't need ipynbname (which requires a live kernel)
    exec_globals = {"Path": Path, "json": json, "_algorithm_id": notebook_path.stem}
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
    validate_keywords(metadata["keywords"])
    template_str = template_str.replace(
        '"{{KEYWORDS}}"',
        json.dumps(metadata["keywords"])
    )
    template_str = template_str.replace(
        '"{{THEMES}}"',
        json.dumps([{"id": t} for t in metadata.get("themes", [])])
    )

    # --- Simple string replacements ---
    attribution = metadata.get("attribution", {})
    authors = attribution.get("authors") or []
    author_name = ", ".join(authors) if authors else "Author of the original SentinelHub script is not listed"
    
    description_attribution = (
        f" Adapted from a SentinelHub Custom Script by {author_name}."
        if authors else
        " Adapted from a SentinelHub Custom Script (author not listed)."
    )

    contact_instructions = (
        "Original SentinelHub script. See link below."
        if authors else
        "Original SentinelHub script — author not listed. See link below."
    )

    replacements = {
        "{{ID}}":                   metadata["id"],
        "{{TITLE}}":                metadata["title"],
        "{{DESCRIPTION}}":          metadata["description"],
        "{{CREATED}}":              metadata["created"],
        "{{UPDATED}}":              metadata["updated"],
        "{{LICENSE}}":              metadata["license"],
        "{{NOTEBOOK_PATH}}":        metadata.get("notebook_github_location", ""),
        "{{TARGET_OPENEO_BACKEND_TITLE}}": metadata.get("openeo_backend_title", ""),
        "{{TARGET_OPENEO_BACKEND}}": metadata.get("openeo_backend_url", ""),
        "{{PREVIEW_TITLE}}":        metadata.get("preview_title", "{{PREVIEW_TITLE}}"),
        "{{AUTHOR_NAME}}":          author_name,
        "{{DESCRIPTION_ATTRIBUTION}}": description_attribution,
        "{{CONTACT_INSTRUCTIONS}}": contact_instructions,
        "{{ORIGINAL_SCRIPT}}":      attribution.get("original_script", ""),
        "{{SOURCE_REPOSITORY}}":    attribution.get("source_repository", ""),
    }

    for placeholder, value in replacements.items():
        template_str = template_str.replace(placeholder, value)

    # Warn about any placeholders that couldn't be filled
    remaining = re.findall(r"\{\{[A-Z_]+\}\}", template_str)
    if remaining:
        print(f"Warning: unfilled placeholders: {', '.join(set(remaining))}")

    return json.loads(template_str)


def generate_thumbnail(records_dir: Path, repo_root: Path) -> None:
    """Generate thumbnail.png from an existing preview.png in records_dir."""
    preview_path = records_dir / "preview.png"

    if not preview_path.exists():
        raise FileNotFoundError(
            f"preview.png not found in {records_dir}. "
            "Run register.py with --preview to copy it first."
        )

    with Image.open(preview_path) as img:
        thumb = img.resize((img.width // 2, img.height // 2), Image.LANCZOS)
        thumb_path = records_dir / "thumbnail.png"
        thumb.save(thumb_path)
    print(f"Thumbnail written: {thumb_path.relative_to(repo_root)}")


def run(notebook_path: Path) -> Path:
    """Extract metadata from notebook and write the record JSON. Returns the output path."""
    notebook_path = Path(notebook_path).resolve()
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    template_path = script_dir / "records_template.json"

    print(f"Notebook : {notebook_path.relative_to(repo_root)}")
    print(f"Template : {template_path.relative_to(repo_root)}")

    metadata = extract_metadata_from_notebook(notebook_path)
    print(f"Metadata extracted — id: '{metadata['id']}'")

    with open(template_path) as f:
        template_str = f.read()

    record = fill_template(template_str, metadata)

    output_path = script_dir / metadata["id"] / "records" / f"{metadata['id']}.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(record, f, indent=2)

    print(f"Record written: {output_path.relative_to(repo_root)}")

    generate_thumbnail(output_path.parent, repo_root)

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
