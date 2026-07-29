# Python-Only Endpoint Configuration

This directory contains endpoint configurations using pure Python modules for maximum flexibility and developer-friendliness.

## Structure

Each endpoint is configured in a separate Python file:

- `eopf_explorer.py` - EOPF Explorer API configuration
- `copernicus_dataspace.py` - Copernicus Data Space configuration
- `ds_development.py` - Development Seed OpenEO Backend configuration
- `localhost_dev.py` - Local TiTiler-openEO development backend

## Canonical collections and bands

`*.params.py` files reference **canonical** collection ids and band names
(lowercase STAC-style), defined once in `openeo_udp/collections.py`:

- collections: `sentinel-2-l2a`, `sentinel-1-grd` (see the `Collection` enum)
- bands: `b01`..`b12`, `b8a`, `scl` (Sentinel-2); `vh`, `vv` (Sentinel-1); plus
  the viewing-/sun-angle metadata bands.

Each endpoint declares an explicit `COLLECTIONS` table that maps these canonical
identifiers to its backend-native ids. The shared mapper
(`openeo_udp.collections.make_mapper`) rewrites the `collection` and `bands`
Parameters using that table and **raises** rather than guessing:

- `UnsupportedCollectionError` — the endpoint's `COLLECTIONS` has no entry for the
  requested canonical collection.
- `UnsupportedBandError` — the requested band is not in that collection's band map.

Band lookups are case-insensitive, so `B04` and `b04` both resolve to the same
canonical band.

## ENDPOINT_CONFIG keys

Each `ENDPOINT_CONFIG` dict defines the connection metadata and the
backend-intrinsic attributes that notebooks read at graph-build time. The
attributes flow into `current_params` via `map_parameters` so notebook code stays
backend-agnostic.

| Key | Purpose |
| --- | --- |
| `name`, `url`, `auth_method` | Connection metadata. |
| `collection_id` | Default/display collection id for this backend (informational; the per-collection `COLLECTIONS` table is the mapping source). |
| `reflectance_scale` | Divisor to convert raw band values to 0-1 reflectance. `1.0` if the backend already serves reflectance; `10000.0` for integer L2A. |
| `bands_dimension` | Name of the band/spectral dimension (openEO spec default is `bands`; some backends still use `spectral`). |
| `time_dimension` | Name of the time dimension (`t` per spec; a few backends use `time`). |
| `description`, `capabilities`, `enabled` | Free-form metadata used by the widget / listing helpers. |

## Adding New Endpoints

To add a new endpoint, create a new Python file with an `ENDPOINT_CONFIG`, a
`COLLECTIONS` mapping table, and delegate `map_parameters` to the shared mapper:

```python
"""Endpoint configuration for Your Backend."""

import openeo

from openeo_udp.collections import Collection, make_mapper

# Endpoint configuration
ENDPOINT_CONFIG = {
    "name": "Your Backend Name",
    "url": "https://your-backend-url/",
    "auth_method": "oidc",  # or "basic", "oidc_authorization_code"
    "collection_id": "your-default-collection-id",
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

# Map canonical collection/band ids to this backend's native names. Only declare
# the collections this backend actually serves; anything else raises an error.
COLLECTIONS = {
    Collection.SENTINEL2_L2A: {
        "collection_id": "your-native-s2-id",
        "bands": {"b02": "...", "b04": "...", "b08": "..."},  # canonical -> native
    },
}

map_parameters = make_mapper(ENDPOINT_CONFIG, COLLECTIONS)


def get_connection():
    connection = openeo.connect(ENDPOINT_CONFIG["url"])
    connection.authenticate_oidc()
    return connection
```

## Advantages of Python-Only Configuration

- **🐍 Developer-Friendly**: Native Python syntax and capabilities
- **🔧 Flexible Mapping**: Full programming power for parameter transformations
- **📦 Self-Contained**: No external dependencies or file formats
- **🚀 Dynamic**: Runtime parameter calculation and conditional logic
- **🧪 Testable**: Easy unit testing of configuration logic
