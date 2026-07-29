"""Parameter definitions for wildfire visualization calculation.

This file defines parameter sets that can be used with the wildfire viz algorithm
for visualizing areas affected by fires using Sentinel-2 imagery.
"""

from openeo.api.process import Parameter


def get_parameters():
    """Return available parameter sets for the wildfire visualization algorithm.

    Returns:
        Dictionary mapping parameter set names to parameter dictionaries.
        Each parameter set includes:
        - location_name: Human-readable location identifier
        - bounding_box: Spatial extent as Parameter object
        - time: Temporal range as Parameter object
        - bands: Required Sentinel-2 bands as Parameter object
        - collection: Data collection identifier as Parameter object
        - cloud_cover: Maximum cloud cover percentage as Parameter object
        - reflectance_scale: Scale factor to convert band values to 0-1 reflectance
    """

    # Bands required for the wildfire visualization algorithm:
    # B02: Blue
    # B03: Green
    # B04: Red
    # B08: NIR
    # B11: SWIR
    # B12: SWIR

    wildfire_bands = [
        "b02",
        "b03",
        "b04",
        "b08",
        "b11",
        "b12"
    ]

    parameter_sets = {
        "central_portugal": {
            "location_name": "Central Portugal",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for a plain in central Portugal",
                default={"west": -8.05, "south": 40.03, "east": -7.47, "north": 40.45},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                default=["2025-08-19", "2025-08-22"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for wildfire visualization",
                default=wildfire_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="sentinel-2-l2a",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum cloud cover percentage",
                default=30,
            ),
            "reflectance_scale": Parameter(
                "reflectance_scale",
                description="Scale factor to convert band values to 0-1 reflectance (10000.0 for integer-scaled L2A, 1.0 for endpoints that already return reflectance)",
                default=10000.0,
            ),
        },
        "natural_parks_provence": {
            "location_name": "Natural Parks in Provence-Alpes, France",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for Natural Parks in Provence-Alpes, France",
                default={"west": 3.17, "south": 43.85, "east": 4.72, "north": 44.54},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                default=["2025-08-01", "2025-08-03"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for wildfire visualization",
                default=wildfire_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="sentinel-2-l2a",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum cloud cover percentage",
                default=30,
            ),
            "reflectance_scale": Parameter(
                "reflectance_scale",
                description="Scale factor to convert band values to 0-1 reflectance (10000.0 for integer-scaled L2A, 1.0 for endpoints that already return reflectance)",
                default=10000.0,
            ),
        },
        "natural_reserve_rome": {
            "location_name": "Natural Reserve in Rome, Italy",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for a Natural Reserve in Rome, Italy",
                default={"west": 12.09, "south": 41.78, "east": 12.39, "north": 41.92},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                default=["2025-10-06", "2025-10-08"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for wildfire visualization",
                default=wildfire_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="sentinel-2-l2a",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum cloud cover percentage",
                default=30,
            ),
            "reflectance_scale": Parameter(
                "reflectance_scale",
                description="Scale factor to convert band values to 0-1 reflectance (10000.0 for integer-scaled L2A, 1.0 for endpoints that already return reflectance)",
                default=10000.0,
            ),
        },
    }

    return parameter_sets
