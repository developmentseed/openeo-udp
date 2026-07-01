"""Parameter definitions for burned forest ML classification.
"""

from openeo.api.process import Parameter


def get_parameters():
    """Return available parameter sets for the ML classification algorithm.

    Returns:
        Dictionary mapping parameter set names to parameter dictionaries.
        Each parameter set includes:
        - location_name: Human-readable location identifier
        - bounding_box: Spatial extent as Parameter object
        - time: Temporal range for data acquisition as Parameter object
        - time_pre: Pre-fire temporal range as Parameter object
        - time_post: Post-fire temporal range as Parameter object
        - bands: Required Sentinel-2 bands as Parameter object
        - collection: Data collection identifier as Parameter object
        - cloud_cover: Maximum cloud cover percentage as Parameter object
        - time_frame: Full-year temporal range for broad data acquisition as Parameter object
    """

    ml_bands = ["B02", "B03", "B04", "B05", "B07", "B08", "B8A", "B11", "B12"]
    default_collection = "SENTINEL2_L2A"

    parameter_sets = {
        "reriz_gafanhao_north_portugal_2024": {
            "location_name": "Reriz e Gafanhao, North Portugal",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent of the 2024 fire area in North Portugal",
                default={"west": -8.23, "south": 40.76, "east": -7.78, "north": 41},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                default=["2024-08-01", "2024-09-01"],
            ),
            "time_pre": Parameter(
                "time_pre",
                description="Pre-fire temporal range",
                default=["2024-08-20", "2024-09-01"],
            ),
            "time_post": Parameter(
                "time_post",
                description="Post-fire temporal range",
                default=["2024-09-30", "2024-10-10"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for APA calculation",
                default=ml_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default=default_collection,
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum cloud cover percentage",
                default=30,
            ),
            "time_frame": Parameter(
                "time_frame",
                description="Full-year temporal range for broad data acquisition",
                default=["2024-01-01", "2024-12-30"],
            ),
        },
    }

    return parameter_sets
