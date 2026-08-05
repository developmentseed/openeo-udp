# License: CC-BY-SA-4.0
# Origin: Converted from Sentinel Hub evalscript
# Original evalscript: https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/oil-spill-index/
# Source: Sentinel Hub Custom Scripts (CC-BY-SA-4.0)
# Conversion: Development Seed (openEO-UDP project)
"""Parameter definitions for the Oil Spill Index (OSI) algorithm.

This file defines parameter sets for detecting oil slick signatures over
coastal and marine Sentinel-2 scenes using OSI-derived band ratios.
"""

from openeo.api.process import Parameter


def get_parameters():
    """Return available parameter sets for the OSI algorithm.

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

    # Bands required by the OSI false-color composite, in the order consumed by
    # the notebook callback: B02, B03, B04, B05, B06, B07, B08, B11, B12.
    osi_bands = ["b02", "b03", "b04", "b05", "b06", "b07", "b08", "b11", "b12"]

    parameter_sets = {
        "wakashio_mauritius": {
            "location_name": "Mauritius shore (Wakashio oil spill)",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent covering the Mauritius shore affected by the Wakashio oil spill",
                schema={"type": "object", "subtype": "bounding-box"},
                default={"west": 57.70, "south": -20.45, "east": 57.77, "north": -20.41},
            ),
            "time": Parameter(
                "time",
                description="Temporal range spanning before, during, and after the oil spill event",
                schema={"type": "array", "subtype": "temporal-interval"},
                default=["2020-07-17", "2020-09-06"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for the OSI false-color composite",
                default=osi_bands,
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
        },
    }

    return parameter_sets
