# License: CC-BY-SA-4.0
# Origin: Converted from Sentinel Hub evalscript
# Original evalscript: https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/vegetation_condition_index/
# Source: Sentinel Hub Custom Scripts (CC-BY-SA-4.0)
# Conversion: Development Seed (openEO-UDP project)
"""Parameter definitions for the Vegetation Condition Index (VCI) algorithm.

This file defines parameter sets for detecting vegetation stress from a
multi-year stack of Sentinel-2 NDVI observations. VCI expresses the most
recent (observed) NDVI, taken from the ``time`` window, relative to the
historical minimum and maximum NDVI within the same calendar window across
the previous ``nb_past_years`` years.

The ``time`` parameter defines the *observed calendar window* (a ``±N``-day
range around an anchor date); the companion notebook derives each historical
window from ``time`` and ``nb_past_years``.
"""

from openeo.api.process import Parameter


def get_parameters():
    """Return available parameter sets for the VCI algorithm.

    Returns:
        Dictionary mapping parameter set names to parameter dictionaries.
        Each parameter set includes:
        - location_name: Human-readable location identifier
        - bounding_box: Spatial extent as Parameter object
        - time: Observed calendar window (current year) as Parameter object
        - bands: Required Sentinel-2 bands as Parameter object
        - collection: Data collection identifier as Parameter object
        - nb_past_years: Number of past years to include in the historical
          NDVI stack, using the same calendar window as ``time``
        - cloud_masking_method: 'threshold' (NGDR/bRatio) or 'scl-dilation'
          (to_scl_dilation_mask)
    """

    # Bands required by VCI: B02/B03/B04 (true color, threshold cloud mask),
    # B08 (NIR, for NDVI with B04).
    vci_bands = ["b02", "b03", "b04", "b08"]

    parameter_sets = {
        "dodge_city_kansas_usa": {
            "location_name": "Dodge City, Kansas, United States",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for vegetated cropland near Dodge City, Kansas, United States",
                schema={"type": "object", "subtype": "bounding-box"},
                default={"west": -100.41, "south": 37.91, "east": -100.01, "north": 38.06},
            ),
            "time": Parameter(
                "time",
                description="Observed calendar window (5 days around 2020-05-30) for the current year",
                schema={"type": "array", "subtype": "temporal-interval"},
                default=["2020-05-25", "2020-06-04"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for VCI",
                default=vci_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="sentinel-2-l2a",
            ),
            "nb_past_years": Parameter(
                "nb_past_years",
                description="Number of past years to include in the historical NDVI stack, using the same calendar window as `time`",
                schema={"type": "integer"},
                default=2,
            ),
            "cloud_masking_method": Parameter(
                "cloud_masking_method",
                description="Cloud masking method: 'threshold' (NGDR/bRatio) or 'scl-dilation' (to_scl_dilation_mask)",
                schema={"type": "string", "enum": ["threshold", "scl-dilation"]},
                default="threshold",
            ),
        },
        "canterbury_plains_new_zealand": {
            "location_name": "Canterbury Plains, New Zealand",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for arable farmland on the Canterbury Plains, New Zealand",
                schema={"type": "object", "subtype": "bounding-box"},
                default={"west": 172.0, "south": -43.75, "east": 172.3, "north": -43.55},
            ),
            "time": Parameter(
                "time",
                description="Observed calendar window (±5 days around 2021-12-01) for the current year",
                schema={"type": "array", "subtype": "temporal-interval"},
                default=["2021-11-26", "2021-12-06"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for VCI",
                default=vci_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="sentinel-2-l2a",
            ),
            "nb_past_years": Parameter(
                "nb_past_years",
                description="Number of past years to include in the historical NDVI stack, using the same calendar window as `time`",
                schema={"type": "integer"},
                default=2,
            ),
            "cloud_masking_method": Parameter(
                "cloud_masking_method",
                description="Cloud masking method: 'threshold' (NGDR/bRatio) or 'scl-dilation' (to_scl_dilation_mask)",
                schema={"type": "string", "enum": ["threshold", "scl-dilation"]},
                default="scl-dilation",
            ),
        },
    }

    return parameter_sets
