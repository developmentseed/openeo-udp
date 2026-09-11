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
        - time_before: Pre-spill acquisition date as Parameter object (runtime)
        - time_oil_spill: Oil-spill acquisition date as Parameter object (runtime)
        - time_dissolute: Post-spill (dissolute) acquisition date as Parameter object (runtime)
        - time_after: Later post-spill window as Parameter object (runtime)
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
            "time_before": Parameter(
                "time_before",
                description="Pre-spill acquisition window; the first available scene within this range is used",
                schema={"type": "array", "subtype": "temporal-interval"},
                default=["2020-07-17", "2020-07-18"],
            ),
            "time_oil_spill": Parameter(
                "time_oil_spill",
                description="Oil-spill acquisition window; the first available scene within this range is used",
                schema={"type": "array", "subtype": "temporal-interval"},
                default=["2020-08-01", "2020-08-02"],
            ),
            "time_dissolute": Parameter(
                "time_dissolute",
                description="Dissolute (post-spill) acquisition window; the first available scene within this range is used",
                schema={"type": "array", "subtype": "temporal-interval"},
                default=["2020-08-06", "2020-08-20"],
            ),
            "time_after": Parameter(
                "time_after",
                description="Later post-spill window; the last available scene within this range is used",
                schema={"type": "array", "subtype": "temporal-interval"},
                default=["2020-08-30", "2020-09-06"],
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
