"""Endpoint configuration for EOPF Explorer (Copernicus Explorer).

This module contains both connection configuration and the canonical->native
collection/band mapping table for the EOPF Explorer OpenEO backend. The actual
mapping logic lives in :func:`openeo_udp.collections.make_mapper`.
"""

import openeo

from openeo_udp.collections import Collection, make_mapper

# Endpoint configuration
ENDPOINT_CONFIG = {
    "name": "EOPF Explorer API",
    "url": "https://api.explorer.eopf.copernicus.eu/openeo",
    "auth_method": "oidc_authorization_code",
    "collection_id": "sentinel-2-l2a",
    "reflectance_scale": 1.0,
    "bands_dimension": "bands",
    "time_dimension": "time",
    "description": "Primary endpoint for interactive development and exploration",
    "capabilities": [
        "load_collection",
        "apply_dimension",
        "save_result",
        "create_service",
    ],
    "cloud_cover_filter": True,
    "max_area_km2": 10000,
    "enabled": True,
}

# Canonical (lowercase STAC-style) -> EOPF-native collection ids and band names.
# Sentinel-2 bands are served under the "reflectance|" asset prefix.
#
# TODO: verify the Sentinel-1 GRD collection id and band asset names on EOPF
# Explorer. The values below are placeholders and must be confirmed before
# relying on S1 here.
_S1_COLLECTION_ID = "sentinel-1-l1-grd"  # TODO: verify
COLLECTIONS = {
    Collection.SENTINEL2_L2A: {
        "collection_id": "sentinel-2-l2a",
        "bands": {
            "b01": "reflectance|b01", "b02": "reflectance|b02",
            "b03": "reflectance|b03", "b04": "reflectance|b04",
            "b05": "reflectance|b05", "b06": "reflectance|b06",
            "b07": "reflectance|b07", "b08": "reflectance|b08",
            "b8a": "reflectance|b8a", "b09": "reflectance|b09",
            "b10": "reflectance|b10", "b11": "reflectance|b11",
            "b12": "reflectance|b12", "scl": "reflectance|scl",
            # Viewing-/sun-angle metadata bands.
            # TODO: verify the native asset names for these on EOPF Explorer.
            "viewzenithmean": "viewZenithMean",
            "viewazimuthmean": "viewAzimuthMean",
            "sunzenithangles": "sunZenithAngles",
            "sunazimuthangles": "sunAzimuthAngles",
        },
    },
    Collection.SENTINEL1_GRD: {
        "collection_id": _S1_COLLECTION_ID,
        "bands": {"vh": "grd|vh", "vv": "grd|vv"},  # TODO: verify
    },
}

map_parameters = make_mapper(ENDPOINT_CONFIG, COLLECTIONS)


def get_connection():
    """Create connection to EOPF Explorer endpoint.

    Returns:
        Authenticated OpenEO connection
    """
    connection = openeo.connect(ENDPOINT_CONFIG["url"])

    # EOPF Explorer uses OIDC authorization code authentication
    connection.authenticate_oidc_authorization_code()

    return connection
