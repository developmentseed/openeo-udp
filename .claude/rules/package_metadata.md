---
paths:
  - "openeo_portable/params/**"
  - "openeo_portable/__init__.py"
  - ".github/workflows/publish.yml"
---

# Rules for openeo-portable package metadata

Apply whenever a file is added to or removed from `openeo_portable/params/`, or the package is released.

- Update the exact parameter-file count in the `.github/workflows/publish.yml` smoke test (`assert len(files) == N`).
- Bump `__version__` in `openeo_portable/__init__.py` (`pyproject.toml` reads it from there).
- Update the `%pip install openeo-portable==X` cell in **every** notebook and in `templates/simple_openeo_notebook.ipynb`. Each must have exactly one, matching `__version__` (folders in `STANDALONE_NOTEBOOK_DIRS` excepted). Batch several new algorithms into one release.
