# Python-Only Endpoint Configuration

This directory contains endpoint configurations using pure Python modules for maximum flexibility and developer-friendliness.

## Structure

Each endpoint is configured in a separate Python file:

- `eopf_explorer.py` - EOPF Explorer API configuration
- `copernicus_dataspace.py` - Copernicus Data Space configuration
- `ds_development.py` - Development Seed OpenEO Backend configuration
- `localhost_dev.py` - Local TiTiler-openEO development backend

## ENDPOINT_CONFIG keys

Each `ENDPOINT_CONFIG` dict must define the connection metadata and the
backend-intrinsic attributes that notebooks read at graph-build time. The
attributes flow into `current_params` via `map_parameters` (see below) so
notebook code stays backend-agnostic.

| Key | Purpose |
| --- | --- |
| `name`, `url`, `auth_method` | Connection metadata. |
| `collection_id` | Canonical collection identifier on this backend (e.g. `SENTINEL2_L2A` vs `sentinel-2-l2a`). |
| `band_format` | Template for band names, e.g. `{band}` or `reflectance\|{band}`. |
| `reflectance_scale` | Divisor to convert raw band values to 0-1 reflectance. `1.0` if the backend already serves reflectance; `10000.0` for integer L2A. |
| `bands_dimension` | Name of the band/spectral dimension (openEO spec default is `bands`; some backends still use `spectral`). |
| `time_dimension` | Name of the time dimension (`t` per spec; a few backends use `time`). |
| `description`, `capabilities`, `enabled` | Free-form metadata used by the widget / listing helpers. |

## Adding New Endpoints

To add a new endpoint, create a new Python file with:

```python
"""Endpoint configuration for Your Backend."""

from typing import Any, Dict

from openeo.api.process import Parameter

# Endpoint configuration
ENDPOINT_CONFIG = {
    "name": "Your Backend Name",
    "url": "https://your-backend-url/",
    "auth_method": "oidc",  # or "basic", "oidc_authorization_code"
    "collection_id": "your-collection-id",
    "band_format": "{band}",  # or "prefix|{band}"
    # Backend-intrinsic attributes consumed by notebook UDPs
    "reflectance_scale": 10000.0,  # 1.0 if bands are already 0-1 reflectance
    "bands_dimension": "bands",    # name of the band dimension on this backend
    "time_dimension": "t",         # "t" or "time" depending on the backend
    "description": "Your backend description",
    "capabilities": ["load_collection", "apply_dimension", "save_result"],
    "cloud_cover_filter": True,
    "max_area_km2": 10000,
    "enabled": True,
}


def map_parameters(params: Dict[str, Any]) -> Dict[str, Any]:
    """Map parameters for your endpoint."""
    mapped_params = params.copy()

    # Propagate intrinsic backend attributes into current_params so notebooks
    # can read them as plain scalars via current_params["reflectance_scale"] etc.
    mapped_params["reflectance_scale"] = ENDPOINT_CONFIG["reflectance_scale"]
    mapped_params["bands_dimension"] = ENDPOINT_CONFIG["bands_dimension"]
    mapped_params["time_dimension"] = ENDPOINT_CONFIG["time_dimension"]

    # Add any collection / band name rewrites here
    return mapped_params
```

## Advantages of Python-Only Configuration

- **🐍 Developer-Friendly**: Native Python syntax and capabilities
- **🔧 Flexible Mapping**: Full programming power for parameter transformations
- **📦 Self-Contained**: No external dependencies or file formats
- **🚀 Dynamic**: Runtime parameter calculation and conditional logic
- **🧪 Testable**: Easy unit testing of configuration logic
