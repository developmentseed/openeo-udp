"""Endpoint configuration for Copernicus Data Space.

This module contains both connection configuration and the canonical->native
collection/band mapping table for the Copernicus Data Space OpenEO backend.
The actual mapping logic lives in :func:`openeo_udp.collections.make_mapper`.
"""

import openeo

from openeo_udp.collections import Collection, make_mapper

# Endpoint configuration
ENDPOINT_CONFIG = {
    "name": "Copernicus Data Space - Production API",
    "url": "https://openeo.dataspace.copernicus.eu/",
    "auth_method": "oidc",
    "collection_id": "SENTINEL2_L2A",
    "reflectance_scale": 10000.0,
    "bands_dimension": "bands",
    "time_dimension": "t",
    "description": "Production endpoint for larger scale processing",
    "capabilities": [
        "load_collection",
        "apply_dimension",
        "save_result",
        "batch_processing",
    ],
    "cloud_cover_filter": True,
    "max_area_km2": 50000,
    "enabled": True,
}

# Canonical (lowercase STAC-style) -> CDSE-native collection ids and band names.
# CDSE serves Sentinel-2 with uppercase B-numbers and Sentinel-1 with VH/VV.
COLLECTIONS = {
    Collection.SENTINEL2_L2A: {
        "collection_id": "SENTINEL2_L2A",
        "bands": {
            "b01": "B01", "b02": "B02", "b03": "B03", "b04": "B04",
            "b05": "B05", "b06": "B06", "b07": "B07", "b08": "B08",
            "b8a": "B8A", "b09": "B09", "b10": "B10", "b11": "B11",
            "b12": "B12", "scl": "SCL",
            # Viewing-/sun-angle metadata bands (served under their original names).
            "viewzenithmean": "viewZenithMean",
            "viewazimuthmean": "viewAzimuthMean",
            "sunzenithangles": "sunZenithAngles",
            "sunazimuthangles": "sunAzimuthAngles",
        },
    },
    Collection.SENTINEL1_GRD: {
        "collection_id": "SENTINEL1_GRD",
        "bands": {"vh": "VH", "vv": "VV"},
    },
}

map_parameters = make_mapper(ENDPOINT_CONFIG, COLLECTIONS)


def get_connection():
    """Create connection to Copernicus Data Space endpoint.

    Returns:
        Authenticated OpenEO connection
    """
    connection = openeo.connect(ENDPOINT_CONFIG["url"])

    # Copernicus Data Space uses OIDC authentication
    connection.authenticate_oidc()

    return connection
