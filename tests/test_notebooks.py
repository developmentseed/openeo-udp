"""Checks that notebooks and templates follow the PyPI/JupyterLite conventions.

Notebooks run for users (locally and in APEx JupyterLite, with no repository
checkout), so they must not register algorithms or depend on the repository
layout. Registration is a maintainer step run from the repository root.
"""

import json
import re
from pathlib import Path

import pytest

import openeo_udp
from tests.test_packaged_params import STANDALONE_NOTEBOOK_DIRS

REPO_ROOT = Path(__file__).resolve().parents[1]

NOTEBOOKS = sorted(
    path
    for path in REPO_ROOT.glob("notebooks/**/*.ipynb")
    if ".ipynb_checkpoints" not in path.parts
)
PACKAGED_NOTEBOOKS = [
    path
    for path in NOTEBOOKS
    if not any(
        path.relative_to(REPO_ROOT).is_relative_to(d) for d in STANDALONE_NOTEBOOK_DIRS
    )
]
TEMPLATES = sorted(REPO_ROOT.glob("templates/*.ipynb"))

FORBIDDEN = {
    "imports algorithm_registration": re.compile(r"\balgorithm_registration\b"),
    "calls register()": re.compile(r"^\s*register\(", re.M),
    "looks up the repository root": re.compile(r"\b_repo_root\b"),
    "uses ipynbname": re.compile(r"\bipynbname\b"),
}
INSTALL = re.compile(r"%pip install openeo-udp==([\w.]+)")


def _code(path: Path) -> str:
    cells = json.loads(path.read_text(encoding="utf-8"))["cells"]
    return "\n".join("".join(c["source"]) for c in cells if c["cell_type"] == "code")


def _ids(paths):
    return [str(p.relative_to(REPO_ROOT)) for p in paths]


@pytest.mark.parametrize("path", NOTEBOOKS + TEMPLATES, ids=_ids(NOTEBOOKS + TEMPLATES))
def test_no_in_notebook_registration(path):
    code = _code(path)
    problems = [name for name, pattern in FORBIDDEN.items() if pattern.search(code)]
    assert not problems, f"{path.name} {', '.join(problems)}"


@pytest.mark.parametrize(
    "path", PACKAGED_NOTEBOOKS + TEMPLATES, ids=_ids(PACKAGED_NOTEBOOKS + TEMPLATES)
)
def test_install_cell_pins_current_version(path):
    pins = INSTALL.findall(_code(path))
    assert len(pins) == 1, f"{path.name} should have exactly one install cell"
    assert pins[0] == openeo_udp.__version__, (
        f"{path.name} installs openeo-udp=={pins[0]}, "
        f"but the package version is {openeo_udp.__version__}"
    )
