# License: CC-BY-SA-4.0
# Origin: Converted from Sentinel Hub evalscript
# Original evalscript: https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/monthly_composite/
# Source: Sentinel Hub Custom Scripts (CC-BY-SA-4.0)
# Conversion: Development Seed (openEO-UDP project)
"""Parameter definitions for the Monthly Composite algorithm.

This file defines parameter sets that can be used with the monthly composite
algorithm, which builds a single cloud-free RGB synthesis from one month of
Sentinel-2 imagery by selecting, per pixel, the "best" (greenest / clearest)
observation and applying an enhanced natural-color stretch.

The ``time`` parameter defines the *one-month window* to composite; the
companion notebook selects the best observation inside that window per pixel.
"""

from openeo.api.process import Parameter


def get_parameters():
    """Return available parameter sets for the monthly composite algorithm.

    Returns:
        Dictionary mapping parameter set names to parameter dictionaries.
        Each parameter set includes:
        - location_name: Human-readable location identifier
        - bounding_box: Spatial extent as Parameter object (runtime)
        - time: One-month compositing window as Parameter object (runtime)
        - bands: Required Sentinel-2 bands as Parameter object
        - collection: Data collection identifier as Parameter object
        - cloud_cover: Maximum scene-level cloud cover percentage
        - gain: Brightness gain applied in the enhanced natural-color stretch
          (the ``2.8`` multiplier from the original evalscript)

    Note:
        The original evalscript expects 0-1 reflectance; on integer-scaled L2A
        backends (e.g. CDSE) the band values are divided by ``reflectance_scale``
        (injected by the endpoint mapper, 10000.0 for CDSE) before the stretch.
    """

    # Bands required for the monthly composite algorithm:
    # B02 (Blue), B03 (Green), B04 (Red), B05 (Red Edge 1), B08 (NIR) for the
    # enhanced natural-color stretch and the B08/B03 "greenest pixel" ranking;
    # SCL (Scene Classification Layer) for cloud/shadow masking.
    monthly_composite_bands = [
        "B02",
        "B03",
        "B04",
        "B05",
        "B08",
        "SCL",
    ]

    parameter_sets = {
        "west_corsica_france": {
            "location_name": "West Corsica, France",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for West Corsica, France",
                default={"west": 8.53, "south": 42.10, "east": 8.72, "north": 42.19},
            ),
            "time": Parameter(
                "time",
                description="One-month window to composite",
                default=["2024-06-01", "2024-07-01"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for the monthly composite",
                default=monthly_composite_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="SENTINEL2_L2A",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum scene-level cloud cover percentage",
                default=90,
            ),
            "gain": Parameter(
                "gain",
                description="Brightness gain for the enhanced natural-color stretch (2.8 in the original script)",
                default=2.8,
            ),
        },
        "po_valley_cropland_italy": {
            "location_name": "Po Valley Cropland, Italy",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for the Po Valley agricultural plain, Italy",
                default={"west": 10.80, "south": 44.95, "east": 11.05, "north": 45.10},
            ),
            "time": Parameter(
                "time",
                description="One-month window to composite",
                default=["2024-07-01", "2024-08-01"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for the monthly composite",
                default=monthly_composite_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="SENTINEL2_L2A",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum scene-level cloud cover percentage",
                default=90,
            ),
            "gain": Parameter(
                "gain",
                description="Brightness gain for the enhanced natural-color stretch (2.8 in the original script)",
                default=2.8,
            ),
        },
        # Brittany is a maritime, frequently cloudy region — a good showcase for
        # monthly compositing, since few single scenes are fully cloud-free.
        "brittany_france": {
            "location_name": "Brittany Coast, France",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for the Brittany coast, France",
                default={"west": -4.00, "south": 48.00, "east": -3.70, "north": 48.20},
            ),
            "time": Parameter(
                "time",
                description="One-month window to composite",
                default=["2024-05-01", "2024-06-01"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for the monthly composite",
                default=monthly_composite_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="SENTINEL2_L2A",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum scene-level cloud cover percentage",
                default=95,
            ),
            "gain": Parameter(
                "gain",
                description="Brightness gain for the enhanced natural-color stretch (2.8 in the original script)",
                default=2.8,
            ),
        },
    }

    return parameter_sets
