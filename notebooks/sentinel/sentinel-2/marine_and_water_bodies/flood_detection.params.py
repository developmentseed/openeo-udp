# License: CC-BY-SA-4.0
# Origin: Converted from a Sentinel Hub custom script
# Original script: https://custom-scripts.sentinel-hub.com/custom-scripts/data-fusion/s1_flooding_visualisation/
# Source: Sentinel Hub Custom Scripts (CC-BY-SA-4.0)
# Conversion: Development Seed (openEO-UDP project)
"""Parameter TEMPLATE for the Sentinel-1/Sentinel-2 Flood Visualization algorithm.

This is a **data-fusion** algorithm: Sentinel-1 SAR backscatter (VV) is used to
detect flooded/water pixels (smooth water surfaces return very low radar
backscatter), and those pixels are highlighted in blue over a Sentinel-2 true
color background. SAR sees through clouds, so this works even when optical
imagery alone would be blocked by cloud cover during a flood event.

NOTE: This UDP targets the Copernicus Data Space Ecosystem (CDSE), the backend
that serves both Sentinel-1 GRD and Sentinel-2 L2A.

HOW TO USE THIS TEMPLATE
-------------------------
The "thessaly_greece_2023" parameter set below is a worked EXAMPLE. Copy it,
rename the copy to something descriptive (e.g. "danube_floods_2013"), and
replace the values below with real values for your event/area of interest:

- bounding_box: the west/south/east/north extent of your flood area (WGS84
  degrees).
- time: a date window bracketing your Sentinel-1 (and ideally Sentinel-2)
  acquisition(s) during the flood event.
- cloud_cover: adjust based on how cloudy the event typically is (floods are
  often cloudy — a higher tolerance keeps more scenes available).
- water_threshold_db and background_gain: exposed as tunable UDP parameters
  controlling water sensitivity and background brightness — tune per scene
  starting from the defaults below.

``bands``, ``collection``, ``s1_collection`` and ``s1_bands`` are
algorithm-intrinsic (they define which spectral inputs the algorithm reads) and
normally do not need to change per location.
"""

from openeo.api.process import Parameter


def get_parameters():
    """Return available parameter sets for the flood visualization algorithm.

    Returns:
        Dictionary mapping parameter set names to parameter dictionaries.
        Each parameter set includes:
        - location_name: Human-readable location identifier
        - bounding_box: Spatial extent as Parameter object (runtime)
        - time: Date window bracketing the flood-event acquisition (runtime)
        - bands: Sentinel-2 bands for the true-color background (mapped to native names)
        - collection: Sentinel-2 collection id (mapped to native id)
        - cloud_cover: Maximum scene-level cloud cover for the S2 background image (runtime)
        - s1_collection: Sentinel-1 GRD collection id (canonical, mapped per endpoint)
        - s1_bands: Sentinel-1 polarization(s) needed for water detection (VV)
        - water_threshold_db: VV backscatter threshold in dB for water detection (runtime)
        - background_gain: Brightness gain applied to the S2 background (runtime)
    """

    # Sentinel-2 bands for the true-color background (canonical lowercase,
    # mapped per endpoint): B04 (Red), B03 (Green), B02 (Blue).
    s2_bands = ["b08"]

    parameter_sets = {
        # Thessaly plain, Greece — catastrophic flooding from Storm Daniel
        # (early September 2023), which inundated much of the region's
        # agricultural lowlands around Karditsa/Larissa.
        "thessaly_greece_2023": {
            "location_name": "Thessaly, Greece (2023 Storm Daniel floods)",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent over the flooded area",
                schema={"type": "object", "subtype": "bounding-box"},
                default={
                    "west": 21.70563513130361,
                    "south": 39.26831808742622,
                    "east": 22.396135163414897,
                    "north": 39.590242870406456,
                },
            ),
            "time": Parameter(
                "time",
                description="Window bracketing the flood-event acquisition(s)",
                schema={"type": "array", "subtype": "temporal-interval"},
                default=["2023-09-06", "2023-09-11"],
            ),
            # Optional bi-temporal reference windows (not used by the single-date
            # algorithm above, but handy for before/after comparison of the same
            # event): a pre-flood baseline and a post-flood recession check.
            "time_pre": Parameter(
                "time_pre",
                description="Pre-flood baseline window",
                schema={"type": "array", "subtype": "temporal-interval"},
                default=["2023-08-01", "2023-08-07"],
            ),
            "time_post": Parameter(
                "time_post",
                description="Post-flood window (recession check)",
                schema={"type": "array", "subtype": "temporal-interval"},
                default=["2023-10-09", "2023-10-16"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands for the true-color background",
                schema={"type": "array", "subtype": "band-names"},
                default=s2_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Sentinel-2 data collection identifier",
                schema={"type": "string", "subtype": "collection-id"},
                default="sentinel-2-l2a",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum scene-level cloud cover for the S2 background image",
                schema={"type": "number"},
                default=30,
            ),
            "s1_collection": Parameter(
                "s1_collection",
                description="Sentinel-1 GRD collection identifier (canonical; mapped per endpoint)",
                schema={"type": "string", "subtype": "collection-id"},
                default="sentinel-1-grd",
            ),
            "s1_bands": Parameter(
                "s1_bands",
                description="Sentinel-1 polarization(s) needed for water detection",
                schema={"type": "array", "subtype": "band-names"},
                default=["vv"],
            ),
            "water_threshold_db": Parameter(
                "water_threshold_db",
                description=(
                    "VV backscatter threshold in dB (used as -water_threshold_db) at "
                    "or below which a pixel is classified as flooded/water. Lower this "
                    "to detect MORE water, raise it to detect LESS water."
                ),
                schema={"type": "number"},
                default=15,
            ),
            "background_gain": Parameter(
                "background_gain",
                description=(
                    "Brightness gain applied to the Sentinel-2 true-color background "
                    "for non-flooded pixels. Increase for a brighter background, "
                    "decrease if the background is over-exposed."
                ),
                schema={"type": "number"},
                default=2.5,
            ),
        },
        # River Severn floodplain near Gloucester/Tewkesbury, UK — widespread
        # winter flooding during the UK's wet 2023-24 season.
        "severn_river_uk_2024": {
            "location_name": "Severn River, UK",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent over the flooded area",
                schema={"type": "object", "subtype": "bounding-box"},
                default={
                    "west": -2.2731684,
                    "south": 51.91011116157637,
                    "east": -2.1745268614154156,
                    "north": 51.9961253,
                },
            ),
            "time": Parameter(
                "time",
                description="Window bracketing the flood-event acquisition(s)",
                schema={"type": "array", "subtype": "temporal-interval"},
                default=["2024-01-26", "2024-02-29"],
            ),
            # Optional bi-temporal reference windows (not used by the single-date
            # algorithm above, but handy for before/after comparison of the same
            # event): a pre-flood baseline and a post-flood recession check.
            "time_pre": Parameter(
                "time_pre",
                description="Pre-flood baseline window",
                schema={"type": "array", "subtype": "temporal-interval"},
                default=["2023-11-14", "2023-11-19"],
            ),
            "time_post": Parameter(
                "time_post",
                description="Post-flood window (recession check)",
                schema={"type": "array", "subtype": "temporal-interval"},
                default=["2024-04-12", "2024-04-21"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands for the true-color background",
                schema={"type": "array", "subtype": "band-names"},
                default=s2_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Sentinel-2 data collection identifier",
                schema={"type": "string", "subtype": "collection-id"},
                default="sentinel-2-l2a",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum scene-level cloud cover for the S2 background image",
                schema={"type": "number"},
                default=30,
            ),
            "s1_collection": Parameter(
                "s1_collection",
                description="Sentinel-1 GRD collection identifier (canonical; mapped per endpoint)",
                schema={"type": "string", "subtype": "collection-id"},
                default="sentinel-1-grd",
            ),
            "s1_bands": Parameter(
                "s1_bands",
                description="Sentinel-1 polarization(s) needed for water detection",
                schema={"type": "array", "subtype": "band-names"},
                default=["vv"],
            ),
            "water_threshold_db": Parameter(
                "water_threshold_db",
                description=(
                    "VV backscatter threshold in dB (used as -water_threshold_db) at "
                    "or below which a pixel is classified as flooded/water. Lower this "
                    "to detect MORE water, raise it to detect LESS water."
                ),
                schema={"type": "number"},
                default=15,
            ),
            "background_gain": Parameter(
                "background_gain",
                description=(
                    "Brightness gain applied to the Sentinel-2 true-color background "
                    "for non-flooded pixels. Increase for a brighter background, "
                    "decrease if the background is over-exposed."
                ),
                schema={"type": "number"},
                default=2.5,
            ),
        },
    }

    return parameter_sets
