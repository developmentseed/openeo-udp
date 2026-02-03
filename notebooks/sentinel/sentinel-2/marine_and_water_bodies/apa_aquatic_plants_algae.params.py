"""Parameter definitions for Aquatic Plants and Algae (APA) Detection.

This file defines parameter sets that can be used with the APA algorithm
for detecting aquatic plants and algae in water bodies using Sentinel-2 imagery.
"""

from openeo.api.process import Parameter


def get_parameters():
    """Return available parameter sets for the APA algorithm.

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
        "venice_lagoon": {
            "location_name": "Venice Lagoon, Italy",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for Venice Lagoon",
                default={"west": 12.2, "south": 45.3, "east": 12.6, "north": 45.6},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                default=["2023-06-01", "2023-08-31"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for APA calculation",
                default=["B02", "B03", "B04", "B05", "B08", "B8A", "B11"],
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
        "lake_victoria": {
            "location_name": "Lake Victoria, East Africa",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for Lake Victoria",
                default={"west": 33.94, "south": -0.53, "east": 34.88, "north": -0.10},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                default=["2023-07-01", "2023-09-30"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for APA calculation",
                default=["B02", "B03", "B04", "B05", "B08", "B8A", "B11"],
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="sentinel-2-l2a",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum cloud cover percentage",
                default=25,
            ),
        },
        "nile_delta": {
            "location_name": "Nile Delta, Egypt",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for Nile Delta",
                default={"west": 30.5, "south": 30.8, "east": 31.8, "north": 31.6},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                default=["2023-05-01", "2023-07-31"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for APA calculation",
                default=["B02", "B03", "B04", "B05", "B08", "B8A", "B11"],
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
        "florida_everglades": {
            "location_name": "Florida Everglades, USA",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for Florida Everglades",
                default={"west": -81.0, "south": 25.3, "east": -80.3, "north": 25.9},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                default=["2023-06-01", "2023-08-31"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for APA calculation",
                default=["B02", "B03", "B04", "B05", "B08", "B8A", "B11"],
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
        "tonle_sap_lake": {
            "location_name": "Tonle Sap Lake, Cambodia",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for Tonle Sap Lake",
                default={"west": 103.5, "south": 12.8, "east": 104.5, "north": 13.5},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                default=["2023-08-01", "2023-10-31"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for APA calculation",
                default=["B02", "B03", "B04", "B05", "B08", "B8A", "B11"],
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="SENTINEL2_L2A",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum cloud cover percentage",
                default=35,
            ),
        },
    }

    return parameter_sets
