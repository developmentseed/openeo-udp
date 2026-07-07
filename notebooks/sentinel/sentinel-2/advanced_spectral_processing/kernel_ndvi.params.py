"""Parameter definitions for Kernel NDVI (kNDVI) notebook.

This file defines parameter sets that can be used with the kNDVI algorithm
for computing a nonlinear, RBF-kernel generalization of NDVI using Sentinel-2
imagery.
"""

from openeo.api.process import Parameter


def get_parameters():
    """Return available parameter sets for the kNDVI algorithm.

    Returns:
        Dictionary mapping parameter set names to parameter dictionaries.
        Each parameter set includes:
        - location_name: Human-readable location identifier
        - bounding_box: Spatial extent as Parameter object
        - time: Temporal range as Parameter object
        - bands: Required Sentinel-2 bands as Parameter object
        - collection: Data collection identifier as Parameter object
    """

    # Bands required for the kNDVI algorithm:
    # B04 (Red), B08 (NIR), SCL (Scene Classification Layer)
    kndvi_bands = ["B04", "B08", "SCL"]

    parameter_sets = {
        "cepic_plain_croatia": {
            "location_name": "Čepić plain, Istria, Croatia",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for the Čepić plain agricultural area",
                default={"west": 14.09, "east": 14.27, "south": 45.174, "north": 45.25},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                default=["2025-05-10", "2025-05-12"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for kNDVI calculation",
                default=kndvi_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="SENTINEL2_L2A",
            ),
        },
    }

    return parameter_sets
