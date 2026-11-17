"""Parameter definitions for Atmospherically Resistant Vegetation Index (ARVI) notebook.

This file defines parameter sets that can be used with the ARVI algorithm
for computing an atmospherically corrected vegetation index using Sentinel-2 imagery.
"""

from openeo.api.process import Parameter


def get_parameters():
    """Return available parameter sets for the ARVI algorithm.

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

    # Bands required for the ARVI algorithm: B02 (Blue), B04 (Red), B8A (Narrow NIR)
    arvi_bands = ["B02", "B04", "B8A"]

    parameter_sets = {
        "cepic_plain_croatia": {
            "location_name": "Čepić plain, Istria, Croatia",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for the Čepić plain agricultural area",
                schema={"type": "object", "subtype": "bounding-box"},
                default={"west": 14.09, "east": 14.27, "south": 45.174, "north": 45.25},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                schema={"type": "array", "subtype": "temporal-interval"},
                default=["2025-05-10", "2025-05-12"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for ARVI calculation",
                default=arvi_bands,
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