# License: CC-BY-SA-4.0
# Origin: Converted from Sentinel Hub evalscript
# Original evalscript: https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/cloudless_mosaic/
# Source: Sentinel Hub Custom Scripts (CC-BY-SA-4.0)
# Conversion: Development Seed (openEO-UDP project)
"""Parameter definitions for the Cloudless Mosaic algorithm.

This file defines parameter sets that can be used with the cloudless mosaic
algorithm, which builds a cloud-free RGB mosaic from Sentinel-2 L2A imagery by
taking, per pixel and per band, the median of valid (SCL-passing) reflectance
values over a time window, falling back to the median of invalid values when
no valid observation exists.

Note:
    The compositing window is expressed as ``end_date`` + ``window_weeks``
    rather than a fixed ``time`` range, matching the original evalscript
    (which walks back N weeks/months from a reference date). The companion
    notebook derives the concrete ``time`` interval from these two values.
"""

from openeo.api.process import Parameter


def get_parameters():
    """Return available parameter sets for the cloudless mosaic algorithm.

    Returns:
        Dictionary mapping parameter set names to parameter dictionaries.
        Each parameter set includes:
        - location_name: Human-readable location identifier
        - bounding_box: Spatial extent as Parameter object
        - end_date: Last day of the compositing window as Parameter object
        - window_weeks: Number of weeks to look back from end_date as Parameter object
        - bands: Required Sentinel-2 bands as Parameter object
        - collection: Data collection identifier as Parameter object
        - cloud_cover: Maximum scene-level cloud cover percentage as Parameter object
        - brighten_scale: Brightening multiplier applied before merging valid/invalid
          arrays (the constant ``5`` used in the original evalscript)
    """

    # Bands required for the cloudless mosaic algorithm:
    # B02 (Blue), B03 (Green), B04 (Red) for the RGB composite;
    # SCL (Scene Classification Layer) for validity/cloud masking.
    cloudless_mosaic_bands = ["B02", "B03", "B04", "SCL"]

    parameter_sets = {
        "west_corsica_france": {
            "location_name": "West Corsica, France",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for West Corsica, France",
                schema={"type": "object", "subtype": "bounding-box"},
                default={"west": 8.53, "south": 42.10, "east": 8.72, "north": 42.19},
            ),
            "end_date": Parameter(
                "end_date",
                description="Last day of the compositing window (YYYY-MM-DD)",
                schema={"type": "string", "format": "date"},
                default="2025-11-30",
            ),
            "window_weeks": Parameter(
                "window_weeks",
                description="Number of weeks to look back from end_date for the compositing window",
                schema={"type": "number"},
                default=1,
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for the cloudless mosaic",
                default=cloudless_mosaic_bands,
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
                default=30,
            ),
            "brighten_scale": Parameter(
                "brighten_scale",
                description=(
                    "Brightening multiplier applied to valid/invalid reflectance "
                    "values before merging (mirrors the constant 5 used in the "
                    "original evalscript for visual brightness)"
                ),
                schema={"type": "number"},
                default=5,
            ),
        },
    }

    return parameter_sets
