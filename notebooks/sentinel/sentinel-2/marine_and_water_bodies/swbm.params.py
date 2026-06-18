"""Parameter definitions for the Simple Water Bodies' Mapping (SWBM) UDP.

Locations mirror the Sentinel-2 examples shown in the original Sentinel Hub
custom script page (Lake of Sainte-Croix, Oroville Dam) plus two additional
high-contrast water bodies (Aral Sea, Poyang Lake) that exercise long-term
shrinkage and monsoon-driven seasonal flooding.
"""

from openeo.api.process import Parameter


def get_parameters():
    """Return available parameter sets for the SWBM algorithm.

    Each set includes location metadata plus openEO Parameter objects for
    spatial extent, temporal range, required bands, collection, and maximum
    cloud cover.
    """

    bands_default = ["B02", "B03", "B04", "B08", "B11"]

    parameter_sets = {
        "lake_sainte_croix": {
            "location_name": "Lake of Sainte-Croix, France",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for Lake of Sainte-Croix",
                default={"west": 6.10, "south": 43.72, "east": 6.27, "north": 43.82},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                default=["2022-08-01", "2022-08-31"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for SWBM indices",
                default=bands_default,
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="SENTINEL2_L2A",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum cloud cover percentage",
                default=22,
            ),
        },
        "oroville_dam": {
            "location_name": "Oroville Dam, California, USA",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for Oroville Dam reservoir",
                default={"west": -121.55, "south": 39.45, "east": -121.40, "north": 39.60},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                default=["2017-01-30", "2017-12-21"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for SWBM indices",
                default=bands_default,
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
        "aral_sea": {
            "location_name": "Aral Sea, Kazakhstan",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for the Aral Sea",
                default={"west": 58.00, "south": 44.50, "east": 61.50, "north": 46.80},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                default=["2023-07-01", "2023-09-30"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for SWBM indices",
                default=bands_default,
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
        "poyang_lake": {
            "location_name": "Poyang Lake, China",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for Poyang Lake",
                default={"west": 115.80, "south": 28.80, "east": 116.80, "north": 29.80},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                default=["2023-07-01", "2023-09-30"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for SWBM indices",
                default=bands_default,
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
    }

    return parameter_sets
