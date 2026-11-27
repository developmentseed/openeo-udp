---
paths:
  - "**/*.params.py"
  - "openeo_portable/collections.py"
  - "openeo_portable/endpoints/*.py"
---

# Rules parameter files must follow

Applies to `openeo_portable/params/<id>.params.py` (and params files in `STANDALONE_NOTEBOOK_DIRS`).

- Start with `# License: CC-BY-SA-4.0` and include `# Original evalscript: https://...` within the first 5 lines (`test_packaged_params_file_has_license_header`). Converted evalscripts keep CC-BY-SA-4.0.
- Define `get_parameters()` returning `{param_set_name: {location_name, bounding_box, time, bands, collection, cloud_cover, ...}}` with `openeo.api.process.Parameter` values.
- Use canonical collection ids (`sentinel-2-l2a`, `sentinel-1-grd`) and lowercase STAC band names (`b04`, `b8a`, `scl`, `vv`) from `openeo_portable/collections.py`.
- A new collection or band must also be added to `collections.py` and to the `COLLECTIONS` table (canonical → native) of every `openeo_portable/endpoints/*.py` that supports it; otherwise `make_mapper` raises `UnsupportedCollectionError` / `UnsupportedBandError`. Each endpoint's `ENDPOINT_CONFIG` supplies `reflectance_scale`, `bands_dimension` and `time_dimension`, which `ParameterManager` injects into `current_params`.
