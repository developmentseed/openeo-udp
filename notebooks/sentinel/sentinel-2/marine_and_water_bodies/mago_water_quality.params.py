"""Parameter definitions for the MAGO Water Quality Monitoring Tool.

Defines parameter sets for running the MAGO algorithm on inland water bodies.
MAGO was developed and validated on Mediterranean reservoirs and lakes,
so default locations focus on that context with one larger reservoir for
broader testing.
"""

from openeo.api.process import Parameter


def get_parameters():
    """Return available parameter sets for the MAGO algorithm.

    Each set includes location metadata plus openEO Parameter objects for
    spatial extent, temporal range, required bands, collection, and maximum
    cloud cover.
    """

    bands_default = ["B02", "B03", "B04", "B05", "B07", "B08"]

    parameter_sets = {
        "barrage_lebna": {
            "location_name": "Barrage Lebna, Tunisia",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for Barrage Lebna reservoir",
                default={"west": 10.85, "south": 36.70, "east": 10.95, "north": 36.79},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                default=["2025-01-15", "2026-04-15"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for MAGO indicators",
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
        "alqueva_reservoir": {
            "location_name": "Alqueva Reservoir, Portugal",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for Alqueva reservoir",
                default={"west": -7.55, "south": 38.15, "east": -7.25, "north": 38.45},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                default=["2023-07-01", "2023-08-31"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for MAGO indicators",
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
        "albufera_valencia": {
            "location_name": "L'Albufera de Valencia, Spain",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for L'Albufera lagoon",
                default={"west": -0.37, "south": 39.30, "east": -0.28, "north": 39.37},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                default=["2023-07-01", "2023-09-30"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for MAGO indicators",
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
        "mar_menor_lagoon": {
            "location_name": "Mar Menor Lagoon, Spain",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for Mar Menor lagoon",
                default={"west": -0.90, "south": 37.60, "east": -0.70, "north": 37.80},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                default=["2022-06-01", "2022-08-31"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for MAGO indicators",
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
