---
paths:
  - "notebooks/**/*.ipynb"
  - "templates/*.ipynb"
---

# Rules notebook code must follow

See CONTRIBUTING.md "ParameterManager Best Practices".

- **Intrinsic vs runtime params:** pass `.default` for algorithm-intrinsic values (collection, bands) and the bare `Parameter` for runtime knobs (bounding_box, time, cloud_cover) so the exported graph keeps `{"from_parameter": ...}` refs. Only runtime params go in the UDP `parameters` array (via `.to_dict()`).
- **Before any sync `.download()`/`.execute()`** call `param_manager.resolve(cube, current_params)` — the `/result` endpoint rejects unresolved refs. Keep the unresolved cube for UDP export.
- Never hardcode dimension names (`"t"`, `"bands"`); use `current_params["time_dimension"]` / `["bands_dimension"]`.
- Always divide reflectance bands by `current_params["reflectance_scale"]` (10000 on CDSE, 1.0 on float backends).
- Look up native band names with `param_manager.band_name_map(current_params)["b08"]`, never by scanning `cube.metadata.band_names`.
