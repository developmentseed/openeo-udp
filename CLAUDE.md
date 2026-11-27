# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

Converts Sentinel Hub evalscripts into backend-agnostic openEO User-Defined Processes (UDPs) for ESA's APEx project. It has three parts that work together:

1. **`notebooks/`** — one Jupyter notebook per algorithm (organized by sensor/category). Each builds a parameterised process graph, validates it, and exports the UDP JSON and catalogue metadata.
2. **`openeo_portable/`** — a Python package (published to PyPI as `openeo-portable`) that the notebooks install with `%pip install openeo-portable==<version>`. It manages per-algorithm parameter sets and maps them onto different openEO backends.
3. **`algorithm_registration/`** — maintainer tooling plus the committed deliverables (`<id>/openeo_udp/<id>.json`, `<id>/records/<id>.json`, `preview.png`, `thumbnail.png`) that are copied into `developmentseed/apex_algorithms` / `ESA-APEx/apex_algorithms`.

## Commands

```bash
uv sync --group dev                       # install everything for development
uv run pytest                             # full test suite (fast, no backend access)
uv run pytest tests/test_packaged_params.py::test_local_file_takes_precedence   # single test
uv run black . && uv run ruff check .     # format / lint (line length 88)
pre-commit run --all-files                # black, ruff --fix, nbstripout, JSON/YAML checks
uv run jupyter lab

# Register an algorithm (maintainers, from repo root, after running the notebook with its DEFAULT param set)
uv run python -m algorithm_registration.register_algorithm \
    notebooks/<folder>/<id>.ipynb --udp notebooks/<folder>/<id>.json --preview notebooks/<folder>/<base>_preview.png
```

## Adding an algorithm (notebook + parameter file)

Follow these steps when an openEO process developer asks for a new notebook. First ask which `notebooks/<sensor>/<category>/` folder it belongs in, listing the actual folders under `notebooks/`. Once answered, continue with step 1.

1. **Pin down the algorithm.** Point out algorithms already in `notebooks/` that may cover the need. For the developer's own algorithm, ask for its inputs, bands, formula/thresholds and outputs.
2. **Choose where the parameter file lives.**
   - Recommended: packaged, as `openeo_portable/params/<algorithm_id>.params.py`. Notebooks run in the repo load it straight from the local package; notebooks run in APEx JupyterLite only get it after an `openeo-portable` release (steps 4 and 8). Tell the developer.
   - Alternative: next to the notebook, with that folder added to `STANDALONE_NOTEBOOK_DIRS` in `tests/test_packaged_params.py`. Skip steps 4 and 8. Any other `*.params.py` outside `openeo_portable/params/` fails the tests.
3. **Write the parameter file.** Read `.claude/rules/parameter.md` first.
4. **Update the package metadata** (packaged params only). Read `.claude/rules/package_metadata.md` first.
5. **Build the notebook draft.**
   - Copy `templates/simple_openeo_notebook.ipynb` to `notebooks/<sensor>/<category>/<algorithm_id>.ipynb`. Use `notebooks/sentinel/sentinel-2/cloud_and_atmospheric_processing/monthly_composite.ipynb` as the canonical `ParameterManager` reference. Read `.claude/rules/notebooks.md` before editing.
   - `ParameterManager("<algorithm_id>.params.py")` resolves a bare name to the packaged file; a local file with the same name takes precedence.
   - Notebooks run in APEx JupyterLite with no checkout: no `algorithm_registration`, `register(`, `_repo_root` or `ipynbname` (`tests/test_notebooks.py`). Write outputs only next to the notebook; hardcode `_algorithm_id` and `_nb_href`.
   - Keep the cell tagged `notebook_metadata` self-contained: registration `exec()`s it in isolation.
   - Do not run it end-to-end; give the developer the notebook path to check. `nbstripout` runs in pre-commit, so outputs are not committed.
6. **Propose a validation scenario:** a different location/time with a small spatial and temporal extent, to check the process works beyond the default parameter set.
7. **Check locally:** `uv run pytest`, `uv run black . && uv run ruff check .`, `pre-commit run --all-files`.
8. **Release `openeo-portable` (packaged params only).** After merging, push a tag such as `v0.3.0` to publish to PyPI; the smoke test checks the version and the parameter-file count.
9. **Register (maintainers).** Run the notebook with its DEFAULT param set, then run `register_algorithm` (see Commands).
   - It copies the UDP + preview into `algorithm_registration/<id>/` and fills `records_template.json` via `populate_record.py`. Watch for `Warning: unfilled placeholders` (a missing `metadata` key leaves literal `{{PLACEHOLDER}}`).
   - Generated files are regenerated on every registration; don't hand-edit them. Commit the whole `<id>/` directory.
   - PRs touching `algorithm_registration/<id>/` trigger `run_apex_qa_tests.yml`, which lints the UDP JSON and validates the record against the APEx schema in the `apex_algorithms` fork.
   - `docs/publication.md` covers publishing to `apex_algorithms` (keep `service` and the webapp `server=` on the same backend; pin/clean branch refs before merge).

## Licensing

MIT by default, but anything converted from a Sentinel Hub evalscript must stay CC-BY-SA-4.0 with an origin header — see `LICENSING.md` for the template.
