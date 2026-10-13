"""Endpoint configuration for Microsoft Planetary Computer OpenEO Backend.

This module contains both connection configuration and the canonical->native
collection/band mapping table for the Microsoft Planetary Computer OpenEO backend. The
actual mapping logic lives in :func:`openeo_udp.collections.make_mapper`.
"""

import openeo

from openeo_udp.collections import Collection, make_mapper

# Endpoint configuration
ENDPOINT_CONFIG = {
    "name": "Microsoft Planetary Computer OpenEO Backend",
    "url": "https://openeo.mpc.ds.io/",
    "auth_method": "oidc",
    "collection_id": "sentinel-2-l2a",
    # TiTiler applies the STAC raster:bands scale/offset, so Sentinel-2 L2A is
    # served as float 0-1 surface reflectance (checked on 2026-10-11: B03 median
    # 0.7 over fresh snow). Do NOT divide by 10000 here.
    "reflectance_scale": 1.0,
    "bands_dimension": "spectral",
    "time_dimension": "t",
    # Convention of the `aspect` process (titiler-openeo #456, checked
    # 2026-10-14): downslope direction, clockwise from north, in radians (GDAL).
    "aspect_convention": "cw_from_north",
    "description": "TiTiler-openEO on Microsoft Planetary Computer (synchronous only, no batch jobs)",
    "capabilities": ["load_collection", "apply_dimension", "save_result"],
    "cloud_cover_filter": True,
    "max_area_km2": 5000,
    "enabled": True,
}

# Canonical (lowercase STAC-style) -> MPC-native collection ids and band names.
COLLECTIONS = {
    Collection.SENTINEL2_L2A: {
        "collection_id": "sentinel-2-l2a",
        "bands": {
            "b01": "B01", "b02": "B02", "b03": "B03",
            "b04": "B04", "b05": "B05", "b06": "B06",
            "b07": "B07", "b08": "B08", "b8a": "B8A",
            "b09": "B09", "b11": "B11",
            "b12": "B12", "scl": "SCL",
            # MPC's L2A has no B10 (cirrus is only in L1C), so b10 is unmapped.
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
    # Copernicus DEM GLO-30, elevation in metres, served as a single "data" band.
    Collection.COPERNICUS_DEM: {
        "collection_id": "cop-dem-glo-30",
        "bands": {"dem": "data"},
    },
}

map_parameters = make_mapper(ENDPOINT_CONFIG, COLLECTIONS)


def get_connection():
    """Create connection to Microsoft Planetary Computer OpenEO Backend.

    Returns:
        Authenticated OpenEO connection
    """
    from openeo.rest.auth.oidc import OidcProviderInfo

    _orig_init = OidcProviderInfo.__init__

    def _patched_init(self, issuer=None, discovery_url=None, scopes=None, **kwargs):
        _orig_init(self, issuer=issuer, discovery_url=discovery_url, scopes=scopes, **kwargs)
        self._scopes = {"openid"} | set(scopes or [])

    OidcProviderInfo.__init__ = _patched_init

    connection = openeo.connect(ENDPOINT_CONFIG["url"])

    # Microsoft Planetary Computer backend uses OIDC authentication
    connection.authenticate_oidc()

    return connection
