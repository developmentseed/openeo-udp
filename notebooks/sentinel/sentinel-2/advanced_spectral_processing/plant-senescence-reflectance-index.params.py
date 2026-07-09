"""Parameter definitions for Plant Senescence Reflectance Index (PSRI) notebook.

This file defines parameter sets that can be used with the PSRI algorithm
for tracking the progression of leaf senescence in vegetation using Sentinel-2 imagery.
"""

from openeo.api.process import Parameter


def get_parameters():
    """Return available parameter sets for the PSRI algorithm.

    Returns:
        Dictionary mapping parameter set names to parameter dictionaries.
        Each parameter set includes:
        - location_name: Human-readable location identifier
        - bounding_box: Spatial extent as Parameter object
        - time: Temporal range as Parameter object
        - bands: Required Sentinel-2 bands as Parameter object
        - collection: Data collection identifier as Parameter object
    """

    # Bands required for the PSRI algorithm: B02 (Blue), B04 (Red), B06 (Vegetation Red Edge)
    psri_bands = ["B02", "B04", "B06"]

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
                description="Sentinel-2 bands required for PSRI calculation",
                default=psri_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="SENTINEL2_L2A",
            ),
        },
    }

    return parameter_sets
