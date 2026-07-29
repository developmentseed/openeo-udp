"""Endpoint configuration for Development Seed OpenEO Backend.

This module contains both connection configuration and the canonical->native
collection/band mapping table for the Development Seed OpenEO backend. The
actual mapping logic lives in :func:`openeo_udp.collections.make_mapper`.
"""

import openeo

from openeo_udp.collections import Collection, make_mapper

# Endpoint configuration
ENDPOINT_CONFIG = {
    "name": "Development Seed OpenEO Backend",
    "url": "https://openeo.ds.io/",
    "auth_method": "oidc_authorization_code",
    "collection_id": "sentinel-2-l2a",
    "reflectance_scale": 1.0,
    "bands_dimension": "spectral",
    "time_dimension": "t",
    "description": "Development and testing endpoint",
    "capabilities": ["load_collection", "apply_dimension", "save_result"],
    "cloud_cover_filter": True,
    "max_area_km2": 5000,
    "enabled": True,
}

# Canonical (lowercase STAC-style) -> DS-native collection ids and band names.
# Sentinel-2 bands carry an explicit resolution suffix (e.g. B04_10m).
COLLECTIONS = {
    Collection.SENTINEL2_L2A: {
        "collection_id": "sentinel-2-l2a",
        "bands": {
            "b01": "B01_60m", "b02": "B02_10m", "b03": "B03_10m",
            "b04": "B04_10m", "b05": "B05_20m", "b06": "B06_20m",
            "b07": "B07_20m", "b08": "B08_10m", "b8a": "B8A_20m",
            "b09": "B09_60m", "b10": "B10_60m", "b11": "B11_20m",
            "b12": "B12_20m", "scl": "SCL_20m",
            # Viewing-/sun-angle metadata bands (no resolution suffix).
            "viewzenithmean": "viewZenithMean",
            "viewazimuthmean": "viewAzimuthMean",
            "sunzenithangles": "sunZenithAngles",
            "sunazimuthangles": "sunAzimuthAngles",
        },
    },
    Collection.SENTINEL1_GRD: {
        "collection_id": "sentinel-1-grd",
        "bands": {"vh": "vh", "vv": "vv"},
    },
}

map_parameters = make_mapper(ENDPOINT_CONFIG, COLLECTIONS)


def get_connection():
    """Create connection to Development Seed OpenEO Backend.

    Returns:
        Authenticated OpenEO connection
    """
    connection = openeo.connect(ENDPOINT_CONFIG["url"])

    # Development Seed backend uses OIDC authentication
    connection.authenticate_oidc_authorization_code()

    return connection
