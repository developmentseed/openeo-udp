"""Parameter definitions for Enhanced Vegetation Index 2 (EVI2) notebook.

This file defines parameter sets that can be used with the EVI2 algorithm
for visualizing vegetation signal strength using Sentinel-2 imagery.
"""

from openeo.api.process import Parameter


def get_parameters():
    """Return available parameter sets for the EVI2 algorithm.

    Returns:
        Dictionary mapping parameter set names to parameter dictionaries.
        Each parameter set includes:
        - location_name: Human-readable location identifier
        - bounding_box: Spatial extent as Parameter object
        - time: Temporal range as Parameter object
        - bands: Required Sentinel-2 bands as Parameter object
        - collection: Data collection identifier as Parameter object
        - cloud_cover: Maximum cloud cover percentage as Parameter object
    """

    # Bands required for the EVI2 algorithm: B08 (NIR), B04 (Red)
    evi2_bands = ["B08", "B04"]

    parameter_sets = {
        "umag_town_istria_croatia": {
            "location_name": "Umag Town, Istria Coast, Croatia",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for Umag Town, Istria Coast, Croatia",
                schema={"type": "object", "subtype": "bounding-box"},
                default={"west": 13.4986, "south": 45.4166, "east": 13.5876, "north": 45.4558},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                schema={"type": "array", "subtype": "temporal-interval"},
                default=["2025-05-12", "2025-05-13"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for EVI2 calculation",
                default=evi2_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="SENTINEL2_L2A",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum cloud cover percentage",
                schema={"type": "number"},
                default=30,
            ),
        },
        "greater_london_uk": {
            "location_name": "Greater London, UK",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for Greater London, UK",
                schema={"type": "object", "subtype": "bounding-box"},
                default={
                    "east": -0.4650038555748272,
                    "north": 51.84594346503951,
                    "south": 51.29532901277588,
                    "west": -1.485823840631227,
                },
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                schema={"type": "array", "subtype": "temporal-interval"},
                default=["2026-07-01T00:00:00Z", "2026-07-15T00:00:00Z"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for EVI2 calculation",
                default=evi2_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="SENTINEL2_L2A",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum cloud cover percentage",
                schema={"type": "number"},
                default=30,
            ),
        },
    }

    return parameter_sets
