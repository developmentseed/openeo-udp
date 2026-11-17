# License: CC-BY-SA-4.0
# Origin: Converted from Sentinel Hub evalscript
# Original evalscript: https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/ndsi/
# Source: Sentinel Hub Custom Scripts (CC-BY-SA-4.0)
# Conversion: Development Seed (openEO-UDP project)
"""Parameter definitions for the Normalized Difference Snow Index (NDSI) algorithm.

This file defines parameter sets for detecting snow from Sentinel-2 green and
SWIR reflectance using NDSI.

Note:
    NDSI expects 0-1 reflectance. On integer-scaled backends (e.g. CDSE, where
    values are 0-10000) the bands are divided by ``reflectance_scale`` (injected
    by the endpoint mapper) before the index is computed, so the same notebook
    runs unchanged on float and integer backends.
"""

from openeo.api.process import Parameter


def get_parameters():
    """Return available parameter sets for the NDSI algorithm.

    Returns:
        Dictionary mapping parameter set names to parameter dictionaries.
        Each parameter set includes:
        - location_name: Human-readable location identifier
        - bounding_box: Spatial extent as Parameter object (runtime)
        - time: Temporal range as Parameter object (runtime)
        - bands: Required Sentinel-2 bands as Parameter object
        - collection: Data collection identifier as Parameter object
        - cloud_cover: Maximum scene-level cloud cover percentage
        - ndsi_threshold: NDSI value above which a pixel is classified as snow
    """

    # Bands required by NDSI, in the order consumed by the notebook callback:
    # B02 (Blue), B03 (Green), B04 (Red), B11 (SWIR).
    ndsi_bands = ["b02", "b03", "b04", "b11"]

    parameter_sets = {
        "haka_conservation_park_nz": {
            "location_name": "Haka Conservation Park, New Zealand",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for Haka Conservation Park, New Zealand",
                schema={"type": "object", "subtype": "bounding-box"},
                default={"west": 168.273, "south": -45.589, "east": 169.097, "north": -45.121},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                schema={"type": "array", "subtype": "temporal-interval"},
                default=["2019-09-19", "2019-09-21"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for NDSI",
                default=ndsi_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="sentinel-2-l2a",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum scene-level cloud cover percentage",
                schema={"type": "number"},
                default=30,
            ),
            "ndsi_threshold": Parameter(
                "ndsi_threshold",
                description="NDSI value above which a pixel is classified as snow",
                schema={"type": "number"},
                default=0.42,
            ),
        },
        "aletsch_glacier_switzerland": {
            "location_name": "Aletsch Glacier, Switzerland",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for the Aletsch Glacier, Switzerland",
                schema={"type": "object", "subtype": "bounding-box"},
                default={"west": 7.9, "south": 46.42, "east": 8.1, "north": 46.54},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                schema={"type": "array", "subtype": "temporal-interval"},
                default=["2025-01-15", "2025-01-17"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for NDSI",
                default=ndsi_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="sentinel-2-l2a",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum scene-level cloud cover percentage",
                schema={"type": "number"},
                default=30,
            ),
            "ndsi_threshold": Parameter(
                "ndsi_threshold",
                description="NDSI value above which a pixel is classified as snow",
                schema={"type": "number"},
                default=0.42,
            ),
        },
    }

    return parameter_sets
