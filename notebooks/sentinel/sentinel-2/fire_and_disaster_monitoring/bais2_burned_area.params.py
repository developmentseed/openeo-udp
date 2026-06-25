# License: CC-BY-SA-4.0
# Origin: Converted from Sentinel Hub evalscript
# Original evalscript: https://custom-scripts.sentinel-hub.com/sentinel-2/bais2/
# Source: Sentinel Hub Custom Scripts (CC-BY-SA-4.0)
# Conversion: Development Seed (openEO-UDP project)
"""Parameter definitions for the BAIS2 (Burned Area Index for Sentinel-2) algorithm.

This file defines parameter sets for mapping burned areas and active fires from
Sentinel-2 red-edge, NIR and SWIR reflectance using the BAIS2 index
(Filipponi, 2018).

Note:
    BAIS2 expects 0-1 reflectance. On integer-scaled backends (e.g. CDSE, where
    values are 0-10000) the bands are divided by ``reflectance_scale`` (injected by
    the endpoint mapper) before the index is computed, so the same notebook runs
    unchanged on float and integer backends.
"""

from openeo.api.process import Parameter


def get_parameters():
    """Return available parameter sets for the BAIS2 algorithm.

    Returns:
        Dictionary mapping parameter set names to parameter dictionaries.
        Each parameter set includes:
        - location_name: Human-readable location identifier
        - bounding_box: Spatial extent as Parameter object (runtime)
        - time: Temporal range as Parameter object (runtime)
        - bands: Required Sentinel-2 bands as Parameter object
        - collection: Data collection identifier as Parameter object
        - cloud_cover: Maximum scene-level cloud cover percentage
    """

    # Bands required by BAIS2, in the order consumed by the notebook callback:
    # B04 (Red), B06/B07 (Red Edge), B8A (Narrow NIR), B12 (SWIR).
    bais2_bands = ["b04", "b06", "b07", "b8a", "b12"]

    parameter_sets = {
        "gran_canaria": {
            "location_name": "Las Palmas de Gran Canaria, Spain",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for Las Palmas de Gran Canaria, Spain",
                default={"west": -15.91, "south": 27.73, "east": -15.29, "north": 28.22},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                default=["2019-08-19", "2019-08-30"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for BAIS2",
                default=bais2_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="sentinel-2-l2a",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum scene-level cloud cover percentage",
                default=30,
            ),
        },
        "california_wildfire": {
            "location_name": "Central California, USA",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for a wildfire-prone area in Central California, USA",
                default={"west": -120.5, "south": 36.0, "east": -119.5, "north": 37.0},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                default=["2020-09-01", "2020-09-15"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for BAIS2",
                default=bais2_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="sentinel-2-l2a",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum scene-level cloud cover percentage",
                default=20,
            ),
        },
        "australia_bushfire": {
            "location_name": "South-East Australia",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for a bushfire-prone area in South-East Australia",
                default={"west": 149.0, "south": -37.0, "east": 150.0, "north": -36.0},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                default=["2019-12-01", "2019-12-15"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for BAIS2",
                default=bais2_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="sentinel-2-l2a",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum scene-level cloud cover percentage",
                default=25,
            ),
        },
    }

    return parameter_sets
