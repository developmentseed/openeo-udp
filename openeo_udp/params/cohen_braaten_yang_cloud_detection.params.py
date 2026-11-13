# License: CC-BY-SA-4.0
# Origin: Converted from Sentinel Hub evalscript
# Original evalscript: https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/cby_cloud_detection/
# Source: Sentinel Hub Custom Scripts (CC-BY-SA-4.0)
# Conversion: Development Seed (openEO-UDP project)
"""Parameter definitions for the Braaten-Cohen-Yang cloud detection algorithm.

This file defines parameter sets that can be used with the Braaten-Cohen-Yang
(BCY) cloud detector, which flags thick and thin clouds on Sentinel-2 imagery
using simple threshold tests on the green band, NDGR (green/red normalized
difference) and a SWIR constraint used to reduce snow misclassification.

Note:
    The threshold tests expect 0-1 reflectance. On integer-scaled backends
    (e.g. CDSE, where values are 0-10000) the bands are divided by
    ``reflectance_scale`` (injected by the endpoint mapper) before the
    thresholds are evaluated.
"""

from openeo.api.process import Parameter


def get_parameters():
    """Return available parameter sets for the BCY cloud-detection algorithm.

    Returns:
        Dictionary mapping parameter set names to parameter dictionaries.
        Each parameter set includes:
        - location_name: Human-readable location identifier
        - bounding_box: Spatial extent as Parameter object (runtime)
        - time: Temporal range as Parameter object (runtime)
        - bands: Required Sentinel-2 bands as Parameter object
        - collection: Data collection identifier as Parameter object
        - cloud_cover: Maximum scene-level cloud cover percentage
        - swir_threshold: SWIR (B11) reflectance threshold (tau) used to gate
          both the thick- and thin-cloud tests
        - gain: Brightness gain applied to the clear-sky natural-color output
    """

    # Bands required for the BCY cloud detector, as listed in the original
    # notebook: B02 (Blue), B03 (Green), B04 (Red), B11 (SWIR), SCL (Scene
    # Classification Layer, loaded alongside the reflectance bands).
    cby_bands = [
        "B02",
        "B03",
        "B04",
        "B11",
        "SCL",
    ]

    parameter_sets = {
        "orbetello_italy": {
            "location_name": "Orbetello, Italy",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for Orbetello, Italy",
                schema={"type": "object", "subtype": "bounding-box"},
                default={
                    "west": 10.964957345155742,
                    "south": 42.36019378945439,
                    "east": 11.573568254047242,
                    "north": 42.59206255158802,
                },
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                schema={"type": "array", "subtype": "temporal-interval"},
                default=["2017-10-06", "2017-10-07"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for BCY cloud detection",
                default=cby_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="SENTINEL2_L2A",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum scene-level cloud cover percentage",
                schema={"type": "number"},
                default=0,
            ),
            "swir_threshold": Parameter(
                "swir_threshold",
                description="SWIR (B11) reflectance threshold (tau) gating the cloud tests",
                schema={"type": "number"},
                default=0.1,
            ),
            "gain": Parameter(
                "gain",
                description="Brightness gain for the clear-sky natural-color output",
                schema={"type": "number"},
                default=2.5,
            ),
        },
        "pitigliano_tuscany_italy": {
            "location_name": "Pitigliano, Tuscany, Italy",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for Pitigliano, Tuscany, Italy",
                schema={"type": "object", "subtype": "bounding-box"},
                default={
                    "west": 11.51452075637124,
                    "south": 42.54849900247214,
                    "east": 11.838960758813727,
                    "north": 42.701080340603454,
                },
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                schema={"type": "array", "subtype": "temporal-interval"},
                default=["2025-10-01", "2025-10-31"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for BCY cloud detection",
                default=cby_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="SENTINEL2_L2A",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum scene-level cloud cover percentage",
                schema={"type": "number"},
                default=60,
            ),
            "swir_threshold": Parameter(
                "swir_threshold",
                description="SWIR (B11) reflectance threshold (tau) gating the cloud tests",
                schema={"type": "number"},
                default=0.1,
            ),
            "gain": Parameter(
                "gain",
                description="Brightness gain for the clear-sky natural-color output",
                schema={"type": "number"},
                default=2.5,
            ),
        },
    }

    return parameter_sets
