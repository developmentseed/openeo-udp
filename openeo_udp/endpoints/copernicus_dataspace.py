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
    # Top-of-atmosphere L1C: same uppercase band names as L2A, minus SCL.
    Collection.SENTINEL2_L1C: {
        "collection_id": "SENTINEL2_L1C",
        "bands": {
            "b01": "B01", "b02": "B02", "b03": "B03", "b04": "B04",
            "b05": "B05", "b06": "B06", "b07": "B07", "b08": "B08",
            "b8a": "B8A", "b09": "B09", "b10": "B10", "b11": "B11",
            "b12": "B12",
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
    # Sentinel-3 SLSTR. s7-s9/f1/f2 are brightness temperature in KELVIN, not
    # reflectance — do not apply reflectance_scale to them.
    Collection.SENTINEL3_SLSTR: {
        "collection_id": "SENTINEL3_SLSTR",
        "bands": {
            "s1": "S1", "s2": "S2", "s3": "S3", "s4": "S4", "s5": "S5",
            "s6": "S6", "s7": "S7", "s8": "S8", "s9": "S9",
            "f1": "F1", "f2": "F2",
        },
    },
    # Sentinel-3 OLCI L1B, delivered as 0-1 reflectance (not 0-10000).
    Collection.SENTINEL3_OLCI_L1B: {
        "collection_id": "SENTINEL3_OLCI_L1B",
        "bands": {f"b{i:02d}": f"B{i:02d}" for i in range(1, 22)},
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
