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
    # L1C is served without the resolution suffix that L2A carries, and has no
    # SCL layer. Angle bands are not exposed, so they are deliberately unmapped.
    Collection.SENTINEL2_L1C: {
        "collection_id": "sentinel-2-l1c",
        "bands": {
            "b01": "B01", "b02": "B02", "b03": "B03", "b04": "B04",
            "b05": "B05", "b06": "B06", "b07": "B07", "b08": "B08",
            "b8a": "B8A", "b09": "B09", "b10": "B10", "b11": "B11",
            "b12": "B12",
        },
    },
    Collection.SENTINEL1_GRD: {
        "collection_id": "sentinel-1-grd",
        "bands": {"vh": "vh", "vv": "vv"},
    },
    # Sentinel-3 SLSTR, served as the raw ESA RBT product rather than a
    # harmonised view, so band names carry a view/grid suffix:
    #   _in / _io = nadir / oblique on the 1 km thermal grid
    #   _an / _ao = nadir / oblique on the 500 m reflective grid
    # We map the canonical names to the NADIR view, which is what retrievals
    # expect. NOTE the units differ from CDSE: s1-s6 are radiance here (CDSE
    # serves reflectance), while s7-s9/f1/f2 are brightness temperature in
    # Kelvin on both backends. The NRT variant is `sentinel-3-sl-1-rbt-nrt`.
    Collection.SENTINEL3_SLSTR: {
        "collection_id": "sentinel-3-sl-1-rbt-ntc",
        "bands": {
            "s1": "S1_radiance_an", "s2": "S2_radiance_an",
            "s3": "S3_radiance_an", "s4": "S4_radiance_an",
            "s5": "S5_radiance_an", "s6": "S6_radiance_an",
            "s7": "S7_BT_in", "s8": "S8_BT_in", "s9": "S9_BT_in",
            "f1": "F1_BT_in", "f2": "F2_BT_in",
        },
    },
    # Sentinel-3 OLCI L1B EFR, again the raw ESA product. IMPORTANT: these are
    # top-of-atmosphere RADIANCE, whereas CDSE serves 0-1 reflectance. Band
    # ratios such as NDVI are NOT interchangeable between the two, because the
    # solar irradiance differs per band — an NDVI computed from radiance is
    # biased low. Convert to reflectance before using any index here.
    # The NRT variant is `sentinel-3-olci-1-efr-nrt`.
    Collection.SENTINEL3_OLCI_L1B: {
        "collection_id": "sentinel-3-olci-1-efr-ntc",
        "bands": {f"b{i:02d}": f"Oa{i:02d}_radianceData" for i in range(1, 22)},
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
