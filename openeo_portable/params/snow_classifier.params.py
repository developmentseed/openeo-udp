# License: CC-BY-SA-4.0
# Origin: Converted from Sentinel Hub evalscript
# Original evalscript: https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/snow_classifier/
# Source: Sentinel Hub Custom Scripts (CC-BY-SA-4.0)
# Conversion: Development Seed (openEO-UDP project)
"""Parameter definitions for the Snow Classifier algorithm.

This file defines parameter sets for detecting snow from Sentinel-2 green,
SWIR, NIR and red reflectance using NDSI as the primary indicator and NDVI as
an additional constraint.

Note:
    NDSI and NDVI expect 0-1 reflectance. On integer-scaled backends (e.g.
    CDSE, where values are 0-10000) the bands are divided by
    ``reflectance_scale`` (injected by the endpoint mapper) before the indices
    are computed, so the same notebook runs unchanged on float and integer
    backends.
"""

from openeo.api.process import Parameter


def get_parameters():
    """Return available parameter sets for the Snow Classifier algorithm.

    Returns:
        Dictionary mapping parameter set names to parameter dictionaries.
        Each parameter set includes:
        - location_name: Human-readable location identifier
        - bounding_box: Spatial extent as Parameter object (runtime)
        - time: Temporal range as Parameter object (runtime)
        - bands: Required Sentinel-2 bands as Parameter object
        - collection: Data collection identifier as Parameter object
        - cloud_cover: Maximum scene-level cloud cover percentage
        - ndsi_threshold: NDSI value above which a pixel is classified as snow
        - target_resolution: Spatial resolution (meters) to resample to before
          classification
    """

    # Bands required by the snow classifier, in the order consumed by the
    # notebook callback: B02 (Blue), B03 (Green), B11 (SWIR), B08 (NIR), B04 (Red).
    snow_bands = ["b02", "b03", "b11", "b08", "b04"]

    parameter_sets = {
        "bovec_slovenia": {
            "location_name": "Bovec, Slovenia",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for Bovec, Slovenia",
                schema={"type": "object", "subtype": "bounding-box"},
                default={"west": 13.40, "south": 46.32, "east": 13.54, "north": 46.39},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                schema={"type": "array", "subtype": "temporal-interval"},
                default=["2019-10-26", "2019-10-30"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for the snow classifier",
                default=snow_bands,
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
            "ndsi_threshold": Parameter(
                "ndsi_threshold",
                description="NDSI value above which a pixel is classified as snow",
                schema={"type": "number"},
                default=0.4,
            ),
            "target_resolution": Parameter(
                "target_resolution",
                description=(
                    "Spatial resolution (meters) to resample to before "
                    "classification. Defaults to 20m, the coarsest native "
                    "resolution among the requested bands (B11 SWIR), so no "
                    "band is upsampled beyond its native resolution."
                ),
                schema={"type": "number"},
                default=20,
            ),
        },
    }

    return parameter_sets