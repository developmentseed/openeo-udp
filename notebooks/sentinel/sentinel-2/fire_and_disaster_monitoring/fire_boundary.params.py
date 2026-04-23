"""Parameter definitions for Fire Boundary notebook.

This file defines parameter sets that can be used with the fire boundary algorithm.
"""

from openeo.api.process import Parameter


def get_parameters():
    """Return available parameter sets for the fire boundary algorithm.

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

    parameter_sets = {
        "melbourne_fire": {
            "location_name": "Melbourne, Australia",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for Melbourne fire area",
                default={"west": 146.55, "south": -37.79, "east": 146.90, "north": -37.55},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                default=["2019-03-04", "2019-03-07"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for fire boundary calculation",
                default=["B11", "B12"],
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="SENTINEL2_L2A",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum cloud cover percentage",
                default=30,
            ),
        },
        "california_wildfire": {
            "location_name": "California Wildfire, USA",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for California wildfire area",
                default={"west": -120.5, "south": 36.0, "east": -119.5, "north": 37.0},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                default=["2020-09-01", "2020-09-15"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for fire boundary calculation",
                default=["B11", "B12"],
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="SENTINEL2_L2A",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum cloud cover percentage",
                default=20,
            ),
        },
        "australia_bushfire": {
            "location_name": "Australia Bushfire",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for Australia bushfire area",
                default={"west": 149.0, "south": -37.0, "east": 150.0, "north": -36.0},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                default=["2019-12-01", "2019-12-15"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for fire boundary calculation",
                default=["B11", "B12"],
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="SENTINEL2_L2A",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum cloud cover percentage",
                default=25,
            ),
        },
    }

    return parameter_sets
