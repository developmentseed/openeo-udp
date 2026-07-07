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
    """

    # Bands required for the EVI2 algorithm: B08 (NIR), B04 (Red)
    evi2_bands = ["B08", "B04"]

    parameter_sets = {
        "umag_town_istria_croatia": {
            "location_name": "Umag Town, Istria Coast, Croatia",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for Umag Town, Istria Coast, Croatia",
                default={"west": 13.4986, "south": 45.4166, "east": 13.5876, "north": 45.4558},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
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
        },
    }

    return parameter_sets
