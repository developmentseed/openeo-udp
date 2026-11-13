# License: CC-BY-SA-4.0
# Origin: Converted from Sentinel Hub evalscript
# Original evalscript: https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/barren_soil/
# Source: Sentinel Hub Custom Scripts (CC-BY-SA-4.0)
# Conversion: Development Seed (openEO-UDP project)
"""Parameter definitions for the Barren Soil Index (BSI) algorithm.

This file defines parameter sets for visualizing barren/bare soil from
Sentinel-2 SWIR, red, NIR and blue reflectance using the Barren Soil Index
(Nguyen et al., 2021).

Note:
    BSI expects 0-1 reflectance. On integer-scaled backends (e.g. CDSE, where
    values are 0-10000) the bands are divided by ``reflectance_scale`` (injected
    by the endpoint mapper) before the index is computed, so the same notebook
    runs unchanged on float and integer backends.
"""

from openeo.api.process import Parameter


def get_parameters():
    """Return available parameter sets for the Barren Soil Index algorithm.

    Returns:
        Dictionary mapping parameter set names to parameter dictionaries.
        Each parameter set includes:
        - location_name: Human-readable location identifier
        - bounding_box: Spatial extent as Parameter object (runtime)
        - time: Temporal range as Parameter object (runtime)
        - bands: Required Sentinel-2 bands as Parameter object
        - collection: Data collection identifier as Parameter object
        - cloud_cover: Maximum scene-level cloud cover percentage
        - brightness: Gain applied to the BSI channel of the RGB composite
    """

    # Bands required by BSI, in the order consumed by the notebook callback:
    # B02 (Blue), B04 (Red), B08 (NIR), B11 (SWIR).
    bsi_bands = ["b02", "b04", "b08", "b11"]

    parameter_sets = {
        "south_ljubljana": {
            "location_name": "South of Ljubljana, Slovenia",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for South of Ljubljana, Slovenia",
                schema={"type": "object", "subtype": "bounding-box"},
                default={"west": 14.44, "south": 45.95, "east": 14.58, "north": 46.01},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                schema={"type": "array", "subtype": "temporal-interval"},
                default=["2019-04-15", "2019-04-20"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for BSI",
                default=bsi_bands,
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
            "brightness": Parameter(
                "brightness",
                description="Gain applied to the BSI channel of the RGB composite",
                schema={"type": "number"},
                default=2.5,
            ),
        },
        "tabernas_desert_spain": {
            "location_name": "Tabernas Desert, Almeria, Spain",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for the Tabernas Desert, Almeria, Spain",
                schema={"type": "object", "subtype": "bounding-box"},
                default={"west": -2.51, "south": 37.03, "east": -2.32, "north": 37.14},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                schema={"type": "array", "subtype": "temporal-interval"},
                default=["2025-07-01", "2025-07-05"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for BSI",
                default=bsi_bands,
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
            "brightness": Parameter(
                "brightness",
                description="Gain applied to the BSI channel of the RGB composite",
                schema={"type": "number"},
                default=2.5,
            ),
        },
    }

    return parameter_sets
