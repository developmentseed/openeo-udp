# License: CC-BY-SA-4.0
# Origin: Converted from Sentinel Hub evalscript
# Original evalscript: https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/agriculture_growth_stage/
# Source: Sentinel Hub Custom Scripts (CC-BY-SA-4.0)
# Conversion: Development Seed (openEO-UDP project)
"""Parameter definitions for the Agricultural Growth Stage algorithm.

This file defines parameter sets for the agricultural growth stage visualization,
a multi-temporal NDVI composite. The companion notebook computes a mean NDVI for
each of the three calendar months in the ``time`` window and assigns them to the
red, green and blue channels (oldest month -> R, middle -> G, newest -> B). The
resulting colour encodes *when* in the season vegetation peaked, which separates
crops by their growth stage / phenology.

The ``time`` parameter therefore defines a **three-month window** that should span
the growing season of interest.
"""

from openeo.api.process import Parameter


def get_parameters():
    """Return available parameter sets for the agricultural growth stage algorithm.

    Returns:
        Dictionary mapping parameter set names to parameter dictionaries.
        Each parameter set includes:
        - location_name: Human-readable location identifier
        - bounding_box: Spatial extent as Parameter object (runtime)
        - time: Three-month growing-season window as Parameter object (runtime)
        - bands: Required Sentinel-2 bands as Parameter object
        - collection: Data collection identifier as Parameter object
        - cloud_cover: Maximum scene-level cloud cover percentage
        - reflectance_scale: Scale factor to convert band values to 0-1 reflectance

    Note:
        NDVI is a normalized ratio and is therefore invariant to ``reflectance_scale``;
        the parameter is kept for consistency with the other notebooks and so the
        same masking conventions apply.
    """

    # Bands required for the agricultural growth stage algorithm:
    # B04 (Red, 665 nm) and B08 (NIR, 842 nm) for NDVI, plus SCL (Scene
    # Classification Layer) for cloud/shadow masking (an idiomatic openEO
    # addition; the original ORBIT evalscript had no explicit cloud mask).
    growth_stage_bands = [
        "B04",
        "B08",
        "SCL",
    ]

    parameter_sets = {
        # Po Valley: intensive, irrigated mixed cropland with staggered sowing
        # dates, so different fields peak in different months -> vivid colours.
        "po_valley_cropland_italy": {
            "location_name": "Po Valley Cropland, Italy",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for the Po Valley agricultural plain, Italy",
                default={"west": 10.80, "south": 44.95, "east": 11.05, "north": 45.10},
            ),
            "time": Parameter(
                "time",
                description="Three-month growing-season window (oldest->R, middle->G, newest->B)",
                default=["2024-04-01", "2024-07-01"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for the growth stage composite",
                default=growth_stage_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="SENTINEL2_L2A",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum scene-level cloud cover percentage",
                default=70,
            ),
            "reflectance_scale": Parameter(
                "reflectance_scale",
                description="Scale factor to convert band values to 0-1 reflectance (10000.0 for integer-scaled L2A, 1.0 for endpoints that already return reflectance)",
                default=10000.0,
            ),
        },
        # Beauce: France's main cereal plain (winter wheat, barley, maize, beet)
        # west of Paris, with a clear spring green-up.
        "beauce_cropland_france": {
            "location_name": "Beauce Cropland, France",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for the Beauce cereal plain, France",
                default={"west": 1.60, "south": 48.10, "east": 1.85, "north": 48.28},
            ),
            "time": Parameter(
                "time",
                description="Three-month growing-season window (oldest->R, middle->G, newest->B)",
                default=["2024-03-01", "2024-06-01"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for the growth stage composite",
                default=growth_stage_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="SENTINEL2_L2A",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum scene-level cloud cover percentage",
                default=70,
            ),
            "reflectance_scale": Parameter(
                "reflectance_scale",
                description="Scale factor to convert band values to 0-1 reflectance (10000.0 for integer-scaled L2A, 1.0 for endpoints that already return reflectance)",
                default=10000.0,
            ),
        },
        # Central Valley: highly diverse Californian irrigated agriculture with
        # year-round cropping, a strong showcase for phenological separation.
        "central_valley_california_usa": {
            "location_name": "Central Valley, California, USA",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for the San Joaquin Valley cropland, California, USA",
                default={
                    "west": -120.55,
                    "south": 36.80,
                    "east": -120.30,
                    "north": 37.00,
                },
            ),
            "time": Parameter(
                "time",
                description="Three-month growing-season window (oldest->R, middle->G, newest->B)",
                default=["2024-03-01", "2024-06-01"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for the growth stage composite",
                default=growth_stage_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="SENTINEL2_L2A",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum scene-level cloud cover percentage",
                default=60,
            ),
            "reflectance_scale": Parameter(
                "reflectance_scale",
                description="Scale factor to convert band values to 0-1 reflectance (10000.0 for integer-scaled L2A, 1.0 for endpoints that already return reflectance)",
                default=10000.0,
            ),
        },
    }

    return parameter_sets
