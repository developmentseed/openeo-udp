"""Parameter definitions for Lava Visualization notebook.

This file defines parameter sets that can be used with the lava visualization
algorithm for visualizing volcanic lava flows using Sentinel-2 imagery.
"""

from openeo.api.process import Parameter


def get_parameters():
    """Return available parameter sets for the lava visualization algorithm.

    Returns:
        Dictionary mapping parameter set names to parameter dictionaries.
        Each parameter set includes:
        - location_name: Human-readable location identifier
        - bounding_box: Spatial extent as Parameter object
        - time: Temporal range as Parameter object
        - bands: Required Sentinel-2 bands as Parameter object
        - collection: Data collection identifier as Parameter object
    """

    # Bands required for the lava visualization algorithm:
    # B02: Blue, B03: Green, B04: Red, B08: NIR, B11: SWIR, B12: SWIR
    lava_bands = ["b02", "b03", "b04", "b08", "b11", "b12"]

    parameter_sets = {
        "cumbre_vieja": {
            "location_name": "Cumbre Vieja, La Palma, Spain",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for the Cumbre Vieja volcanic eruption area",
                default={"west": -17.94, "south": 28.58, "east": -17.86, "north": 28.64},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                default=["2021-10-10", "2021-10-11"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for lava visualization",
                default=lava_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="sentinel-2-l2a",
            ),
        },
    }

    return parameter_sets
