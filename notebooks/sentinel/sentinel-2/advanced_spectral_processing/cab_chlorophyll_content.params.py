# License: CC-BY-SA-4.0
# Origin: Converted from Sentinel Hub evalscript
# Original evalscript: https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/cab/
# Source: Sentinel Hub Custom Scripts (CC-BY-SA-4.0)
# Conversion: Development Seed (openEO-UDP project)
"""Parameter definitions for the Cab (leaf chlorophyll content) calculation.

This file defines parameter sets that can be used with the Cab algorithm for
estimating leaf chlorophyll content (chlorophyll a+b, in micrograms per square
centimetre, ug/cm2) from Sentinel-2 imagery using the SNAP biophysical neural
network ported in the companion notebook.
"""

from openeo.api.process import Parameter


def get_parameters():
    """Return available parameter sets for the Cab algorithm.

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

    # Bands required for the Cab algorithm:
    # B03 (Green), B04 (Red), B05 (Red Edge 1),
    # B06 (Red Edge 2), B07 (Red Edge 3), B8A (Narrow NIR),
    # B11 (SWIR 1), B12 (SWIR 2)
    # viewZenithMean (Viewing zenith angle),
    # viewAzimuthMean (Viewing azimuth angle),
    # sunZenithAngles (Sun zenith angle),
    # sunAzimuthAngles (Sun azimuth angle)

    cab_bands = [
        "B03",
        "B04",
        "B05",
        "B06",
        "B07",
        "B8A",
        "B11",
        "B12",
        "viewZenithMean",
        "viewAzimuthMean",
        "sunZenithAngles",
        "sunAzimuthAngles",
    ]

    parameter_sets = {
        "cropland_plain_croatia": {
            "location_name": "Cropland Plain, Istria Coast, Croatia",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for Cropland Plain, Croatia",
                default={"west": 14.09, "south": 45.174, "east": 14.27, "north": 45.25},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                default=["2025-05-10", "2025-05-12"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for Cab calculation",
                default=cab_bands,
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
                description="Sentinel-2 bands required for Cab calculation",
                default=cab_bands,
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
                description="Sentinel-2 bands required for Cab calculation",
                default=cab_bands,
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
            "reflectance_scale": Parameter(
                "reflectance_scale",
                description="Scale factor to convert band values to 0-1 reflectance (10000.0 for integer-scaled L2A, 1.0 for endpoints that already return reflectance)",
                default=10000.0,
            ),
        },
    }

    return parameter_sets
