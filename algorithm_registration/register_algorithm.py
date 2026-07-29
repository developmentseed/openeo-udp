#!/usr/bin/env python3
"""
Set up algorithm_registration folder structure to store UDP artifacts.

Can be used as a module (e.g. from the last cell of a notebook):

    from algorithm_registration.set_up_record_dir import register
    register(
        notebook_path=Path("notebooks/.../lai.ipynb"),
        udp_path=Path("lai.json"),
        preview_path=Path("preview.png"),
    )

Or as a CLI:

    python set_up_record_dir.py <notebook> [--udp <path>] [--preview <path>]
"""

import argparse
import shutil
import sys
from pathlib import Path

from algorithm_registration.populate_record import run as generate_record

# TODO: Ensure that algorithm_registration comes with the repository
def _find_repo_root(start: Path) -> Path:
    for p in [start, *start.parents]:
        if (p / "algorithm_registration").exists():
            return p
    raise FileNotFoundError(
        "Could not find repo root — no algorithm_registration/ directory found upstream."
    )


def register(
    notebook_path: Path,
    udp_path: Path | None = None,
    preview_path: Path | None = None,
) -> Path:
    """Register UDP artifact and preview image into algorithm_registration/ and generate the OGC API record.

    Args:
        notebook_path: Path to the algorithm notebook (used to derive alg_id and metadata).
        udp_path: Path to the UDP process graph JSON. Optional — CI will fail if not provided.
        preview_path: Path to the preview image (PNG). Optional — CI will fail if not provided.

    Returns:
        Path to the algorithm directory in algorithm_registration/.
    """
    notebook_path = Path(notebook_path).resolve()
    alg_id = notebook_path.stem
    repo_root = _find_repo_root(notebook_path)
    alg_dir = repo_root / "algorithm_registration" / alg_id
    records_dir = alg_dir / "records"
    udp_dir = alg_dir / "openeo_udp"

    records_dir.mkdir(parents=True, exist_ok=True)
    udp_dir.mkdir(parents=True, exist_ok=True)
    print(f"Algorithm directory: {alg_dir}")

    if udp_path is not None:
        udp_path = Path(udp_path).resolve()
        dest = udp_dir / f"{alg_id}.json"
        shutil.copy2(udp_path, dest)
        print(f"UDP registered: {dest}")

    if preview_path is not None:
        preview_path = Path(preview_path).resolve()
        dest = records_dir / "preview.png"
        shutil.copy2(preview_path, dest)
        print(f"Preview registered: {dest}")

    generate_record(notebook_path)

    print("Commit all the records before pushing to openeo-udp repository")

    return alg_dir


def main():
    parser = argparse.ArgumentParser(
        description="Register a UDP algorithm into algorithm_registration/."
    )
    parser.add_argument("notebook", type=Path, help="Path to the algorithm notebook")
    parser.add_argument("--udp", type=Path, default=None, help="Path to the UDP process graph JSON")
    parser.add_argument("--preview", type=Path, default=None, help="Path to the preview image (PNG)")
    args = parser.parse_args()

    notebook_path = args.notebook.resolve()
    if not notebook_path.exists():
        print(f"Error: notebook not found: {notebook_path}")
        sys.exit(1)

    register(notebook_path, udp_path=args.udp, preview_path=args.preview)


if __name__ == "__main__":
    main()
