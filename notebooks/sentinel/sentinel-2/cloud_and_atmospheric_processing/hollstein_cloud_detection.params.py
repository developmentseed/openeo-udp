# License: CC-BY-SA-4.0
# Origin: Converted from Sentinel Hub evalscript
# Original evalscript: https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/hollstein/
# Source: Sentinel Hub Custom Scripts (CC-BY-SA-4.0)
# Conversion: Development Seed (openEO-UDP project)
"""Parameter definitions for the Hollstein cloud-detection algorithm (titiler variant).

This file defines parameter sets for the Hollstein et al. (2016) decision-tree
classification of clouds, cirrus, shadow, water, snow and clear sky from
Sentinel-2 reflectance spectra.

This *titiler* variant runs on Sentinel-2 **L2A**, which does not expose the
cirrus band ``b10`` used by the original L1C decision tree; the companion notebook
substitutes blue/SWIR proxies for the two ``b10`` tests. The ``b10`` band is
therefore intentionally absent from the band list below.

Note:
    The decision-tree thresholds expect 0-1 reflectance. On integer-scaled
    backends (e.g. CDSE, where values are 0-10000) the bands are divided by
    ``reflectance_scale`` (injected by the endpoint mapper) before the tree is
    evaluated, so the same notebook runs unchanged on float and integer backends.
"""

from openeo.api.process import Parameter


def get_parameters():
    """Return available parameter sets for the Hollstein cloud-detection algorithm.

    Returns:
        Dictionary mapping parameter set names to parameter dictionaries.
        Each parameter set includes:
        - location_name: Human-readable location identifier
        - bounding_box: Spatial extent as Parameter object (runtime)
        - time: Temporal range as Parameter object (runtime)
        - bands: Required Sentinel-2 bands as Parameter object
        - collection: Data collection identifier as Parameter object
        - gain: Brightness gain applied to the clear/shadow natural-color output
    """

    # Bands required by the Hollstein decision tree on Sentinel-2 L2A.
    # b10 (cirrus) is omitted because it is not available in L2A; the notebook
    # replaces the two b10-based tests with blue/SWIR proxies.
    hollstein_bands = [
        "b01",
        "b02",
        "b03",
        "b04",
        "b05",
        "b06",
        "b07",
        "b8a",
        "b09",
        "b11",
    ]

    parameter_sets = {
        "veneto_italy": {
            "location_name": "Veneto, Italy",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for an area in Veneto, Italy",
                default={
                    "west": 12.3793,
                    "south": 45.8996,
                    "east": 12.7918,
                    "north": 46.1364,
                },
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                default=["2025-05-12", "2025-05-13"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required by the Hollstein decision tree",
                default=hollstein_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="sentinel-2-l2a",
            ),
            "gain": Parameter(
                "gain",
                description="Brightness gain for the clear/shadow natural-color output",
                default=2.5,
            ),
        },
        "slovenia": {
            "location_name": "Slovenia",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for an area in Slovenia",
                default={
                    "west": 14.95484125321093,
                    "south": 45.80183674806176,
                    "east": 15.323545428919687,
                    "north": 45.95608490378885,
                },
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                default=["2025-05-12", "2025-05-13"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required by the Hollstein decision tree",
                default=hollstein_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="sentinel-2-l2a",
            ),
            "gain": Parameter(
                "gain",
                description="Brightness gain for the clear/shadow natural-color output",
                default=2.5,
            ),
        },
    }

    return parameter_sets
