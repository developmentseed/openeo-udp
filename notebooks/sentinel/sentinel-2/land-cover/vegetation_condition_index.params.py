# License: CC-BY-SA-4.0
# Origin: Converted from Sentinel Hub evalscript
# Original evalscript: https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/vegetation_condition_index/
# Source: Sentinel Hub Custom Scripts (CC-BY-SA-4.0)
# Conversion: Development Seed (openEO-UDP project)
"""Parameter definitions for the Vegetation Condition Index (VCI) algorithm.

This file defines parameter sets for detecting vegetation stress from a
multi-year stack of Sentinel-2 NDVI observations. For each year in
``[year_from, year_to]``, scenes within a ``±tolerance_days`` calendar window
around ``anchor_date`` are cloud-masked and merged into one time stack; VCI
expresses the most recent (observed) NDVI relative to the historical minimum
and maximum NDVI within that same calendar window across prior years.

Note:
    ``anchor_date``, ``year_from``, ``year_to`` and ``tolerance_days`` are
    build-time knobs: the companion notebook uses them (in Python) to shape
    the process graph itself (how many ``load_collection`` calls are merged),
    so changing them produces a different graph rather than a different
    ``from_parameter`` value at execution time. ``time`` is derived from those
    same four values (year_from's window start through year_to's window end)
    so there is a single source of truth; it is kept for interface parity
    with other notebooks (e.g. ``openeo_udp/run_batch_job.py`` expects a
    ``time`` key) even though the notebook itself does not read it back.
"""

from datetime import datetime, timedelta

from openeo.api.process import Parameter


def _overall_time_range(
    anchor_date: str, year_from: int, year_to: int, tolerance_days: int
) -> list[str]:
    """Derive [window_start, window_end] spanning year_from through year_to.

    Mirrors the per-year windowing done in the notebook's cube_scene_stack
    helper, using the same (month, day) anchor for the earliest and latest
    years in the range.
    """
    anchor = datetime.strptime(anchor_date, "%Y-%m-%d")
    month, day = anchor.month, anchor.day

    def _anchor_for_year(year: int) -> datetime:
        try:
            return datetime(year, month, day)
        except ValueError:
            # e.g. Feb 29 in a non-leap year
            return datetime(year, month, 28)

    window_start = _anchor_for_year(year_from) - timedelta(days=tolerance_days)
    window_end = _anchor_for_year(year_to) + timedelta(days=tolerance_days)
    return [window_start.strftime("%Y-%m-%d"), window_end.strftime("%Y-%m-%d")]


def get_parameters():
    """Return available parameter sets for the VCI algorithm.

    Returns:
        Dictionary mapping parameter set names to parameter dictionaries.
        Each parameter set includes:
        - location_name: Human-readable location identifier
        - bounding_box: Spatial extent as Parameter object (runtime)
        - time: Overall multi-year temporal extent derived from anchor_date /
          year_from / year_to / tolerance_days, as Parameter object
        - bands: Required Sentinel-2 bands as Parameter object
        - collection: Data collection identifier as Parameter object
        - anchor_date: Calendar date (month/day) the ±tolerance_days window
          is centered on, for every year in [year_from, year_to]
        - year_from: Earliest year included in the historical NDVI stack
        - year_to: Most recent (observed) year in the NDVI stack
        - tolerance_days: Days before/after anchor_date to include, per year
        - cloud_masking_method: 'threshold' (NGDR/bRatio) or 'scl-dilation'
          (to_scl_dilation_mask)
    """

    # Bands required by VCI: B02/B03/B04 (true color, threshold cloud mask),
    # B08 (NIR, for NDVI with B04).
    vci_bands = ["b02", "b03", "b04", "b08"]

    dodge_city_anchor_date = "2020-05-30"
    dodge_city_year_from = 2018
    dodge_city_year_to = 2020
    dodge_city_tolerance_days = 5

    canterbury_anchor_date = "2021-12-01"
    canterbury_year_from = 2019
    canterbury_year_to = 2021
    canterbury_tolerance_days = 5

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
                description="Overall temporal extent spanning the historical stack, derived from anchor_date/year_from/year_to/tolerance_days",
                schema={"type": "array", "subtype": "temporal-interval"},
                default=_overall_time_range(
                    dodge_city_anchor_date,
                    dodge_city_year_from,
                    dodge_city_year_to,
                    dodge_city_tolerance_days,
                ),
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
            "anchor_date": Parameter(
                "anchor_date",
                description="Observed calendar date (month/day) the ±tolerance_days window is centered on, for every year in [year_from, year_to]",
                schema={"type": "string", "format": "date"},
                default=dodge_city_anchor_date,
            ),
            "year_from": Parameter(
                "year_from",
                description="Earliest year included in the historical NDVI stack",
                schema={"type": "integer"},
                default=dodge_city_year_from,
            ),
            "year_to": Parameter(
                "year_to",
                description="Most recent (observed) year in the NDVI stack",
                schema={"type": "integer"},
                default=dodge_city_year_to,
            ),
            "tolerance_days": Parameter(
                "tolerance_days",
                description="Number of days before/after anchor_date to include, per year",
                schema={"type": "integer"},
                default=dodge_city_tolerance_days,
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
                description="Overall temporal extent spanning the historical stack, derived from anchor_date/year_from/year_to/tolerance_days",
                schema={"type": "array", "subtype": "temporal-interval"},
                default=_overall_time_range(
                    canterbury_anchor_date,
                    canterbury_year_from,
                    canterbury_year_to,
                    canterbury_tolerance_days,
                ),
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
            "anchor_date": Parameter(
                "anchor_date",
                description="Observed calendar date (month/day) the ±tolerance_days window is centered on, for every year in [year_from, year_to]",
                schema={"type": "string", "format": "date"},
                default=canterbury_anchor_date,
            ),
            "year_from": Parameter(
                "year_from",
                description="Earliest year included in the historical NDVI stack",
                schema={"type": "integer"},
                default=canterbury_year_from,
            ),
            "year_to": Parameter(
                "year_to",
                description="Most recent (observed) year in the NDVI stack",
                schema={"type": "integer"},
                default=canterbury_year_to,
            ),
            "tolerance_days": Parameter(
                "tolerance_days",
                description="Number of days before/after anchor_date to include, per year",
                schema={"type": "integer"},
                default=canterbury_tolerance_days,
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