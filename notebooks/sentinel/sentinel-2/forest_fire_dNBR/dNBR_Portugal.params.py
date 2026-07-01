"""Parameter definitions for dNBR fire area detection.
"""

from openeo.api.process import Parameter


def get_parameters():
    """Return available parameter sets for the dNBR algorithm.

    Returns:
        Dictionary mapping parameter set names to parameter dictionaries.
        Each parameter set includes:
        - location_name: Human-readable location identifier
        - bounding_box: Spatial extent as Parameter object
        - time: Temporal range for data acquisition as Parameter object
        - time_pre: Pre-fire temporal range as Parameter object
        - time_post: Post-fire temporal range as Parameter object
        - bands_fire: Sentinel-2 bands required for NBR/dNBR calculation as Parameter object
        - bands_ml: Sentinel-2 bands required for ML classification as Parameter object
        - collection: Data collection identifier as Parameter object
        - cloud_cover: Maximum cloud cover percentage as Parameter object
        - reflectance_scale: Scale factor to convert band values to 0-1 reflectance as Parameter object
          (10000.0 for integer-scaled L2A, 1.0 for endpoints that already return reflectance)
    """
    ml_bands = ["B04", "B08"]  
    fire_bands = ["B8A", "B12"]
    default_collection = "SENTINEL2_L2A"
    default_reflectance_scale = 10000.0

    parameter_sets = {
        "forest_north_portugal_2025": {
            "location_name": "Forest, North Portugal",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent of the 2025 fire area in North Portugal",
                default={"west": -7.987061, "south": 40.012891, "east": -7.434998, "north": 40.359103},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                default=["2025-07-25", "2025-07-31"],
            ),
            "time_pre": Parameter(
                "time_pre",
                description="Pre-fire temporal range",
                default=["2025-07-25", "2025-07-31"],
            ),
            "time_post": Parameter(
                "time_post",
                description="Post-fire temporal range",
                default=["2025-10-15", "2025-10-16"],
            ),
            "bands_fire": Parameter(
                "bands_fire",
                description="Sentinel-2 bands required for NBR calculation",
                default=fire_bands,
            ),
            "bands_ml": Parameter(
                "bands_ml",
                description="Sentinel-2 bands required for ML classification",
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
            "reflectance_scale": Parameter(
                "reflectance_scale",
                description="Scale factor to convert band values to 0-1 reflectance",
                default=default_reflectance_scale,
            ),
        },
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
                default=["2024-09-30", "2024-10-15"],
            ),
            "bands_fire": Parameter(
                "bands_fire",
                description="Sentinel-2 bands required for NBR calculation",
                default=fire_bands,
            ),
            "bands_ml": Parameter(
                "bands_ml",
                description="Sentinel-2 bands required for ML classification",
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
            "reflectance_scale": Parameter(
                "reflectance_scale",
                description="Scale factor to convert band values to 0-1 reflectance",
                default=default_reflectance_scale,
            ),
        },
    }

    return parameter_sets
