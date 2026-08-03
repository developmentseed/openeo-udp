# License: CC-BY-SA-4.0
# Origin: Converted from Sentinel Hub evalscript
# Original evalscript: https://custom-scripts.sentinel-hub.com/custom-scripts/data-fusion/ship_detection_s1_s2/
# Source: Sentinel Hub Custom Scripts (CC-BY-SA-4.0)
# Conversion: Development Seed (openEO-UDP project)
"""Parameter definitions for the Ship Detection (S1/S2 data-fusion) algorithm.

This is a **multi-sensor data-fusion** algorithm. It combines:

- Sentinel-2 (L1C) optical bands to compute NDWI and isolate water pixels, and
- Sentinel-1 GRD (VV, VH) backscatter to flag anomalously bright radar returns
  over water (ships act as corner reflectors against a normally-dark sea surface).

Because the original evalscript uses ``mosaicking: "ORBIT"`` for both
datasources (picking a single representative pass per sensor rather than a
temporal composite), the companion notebook reduces each sensor's short
``time`` window to a single slice with the ``first`` reducer instead of
averaging across days -- averaging would smear out the transient radar
signature a moving vessel produces.

The **Sentinel-2** collection/bands flow through the standard ParameterManager
mapping (so ``reflectance_scale`` and the dimension names are injected), while
the **Sentinel-1** collection/bands are kept as separate keys and mapped via
the endpoint mapper in the notebook (the standard mapping only auto-maps the
single ``collection``/``bands`` pair).

NOTE: This UDP targets the Copernicus Data Space Ecosystem (CDSE), the backend
that serves both Sentinel-1 GRD and Sentinel-2 L1C.
"""

from openeo.api.process import Parameter


def get_parameters():
    """Return available parameter sets for the ship detection algorithm.

    Returns:
        Dictionary mapping parameter set names to parameter dictionaries.
        Each parameter set includes:
        - location_name: Human-readable location identifier
        - bounding_box: Spatial extent as Parameter object (runtime)
        - time: Window bracketing one S1 pass and one S2 pass (runtime)
        - bands: Sentinel-2 bands for NDWI + true color (mapped to native names)
        - collection: Sentinel-2 collection id (mapped to native id)
        - cloud_cover: Maximum scene-level cloud cover for the S2 image
        - s1_collection: Sentinel-1 GRD collection id (canonical, mapped per endpoint)
        - s1_bands: Sentinel-1 polarizations needed (VV, VH)
    """

    # Sentinel-2 bands (canonical lowercase, mapped per endpoint): B02 (Blue),
    # B03 (Green), B04 (Red), B08 (NIR).
    s2_bands = ["b02", "b03", "b04", "b08"]

    parameter_sets = {
        # Zhenjiang, Jiangsu: a major port on the Yangtze River -- the world's
        # busiest inland waterway -- where the Yangtze meets the Beijing-
        # Hangzhou Grand Canal, so barge and cargo-vessel traffic is dense.
        "zhenjiang_yangtze_river": {
            "location_name": "Zhenjiang, Yangtze River",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent over the Yangtze River channel at Zhenjiang, Jiangsu",
                schema={"type": "object", "subtype": "bounding-box"},
                default={
                    "west": 119.3704,
                    "south": 32.1843,
                    "east": 119.5843,
                    "north": 32.2999,
                },
            ),
            "time": Parameter(
                "time",
                description=(
                    "Window bracketing one Sentinel-1 and one Sentinel-2 pass. "
                    "Widened because Sentinel-1 GRD is outside ESA's "
                    "systematic background-mission mask over inland China, "
                    "so acquisitions over this reach of the Yangtze are "
                    "sporadic rather than the nominal 6-day revisit"
                ),
                schema={"type": "array", "subtype": "temporal-interval"},
                default=["2026-03-27", "2026-03-30"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for NDWI and the true-color composite",
                default=s2_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Sentinel-2 data collection identifier",
                default="sentinel-2-l1c",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum scene-level cloud cover for the S2 image (raised for Yangtze plum-rain/monsoon season)",
                schema={"type": "number"},
                default=30,
            ),
            "s1_collection": Parameter(
                "s1_collection",
                description="Sentinel-1 GRD collection identifier (canonical; mapped per endpoint)",
                default="sentinel-1-grd",
            ),
            "s1_bands": Parameter(
                "s1_bands",
                description="Sentinel-1 polarizations needed (VV, VH)",
                default=["vv", "vh"],
            ),
        },
        # Singapore Strait: the world's busiest port and transshipment hub,
        # with dense anchorage traffic east and west of the port.
        "singapore_strait": {
            "location_name": "Singapore Strait anchorage",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent over the Singapore Strait anchorages and approach lanes",
                schema={"type": "object", "subtype": "bounding-box"},
                default={"west": 103.62, "south": 1.15, "east": 103.90, "north": 1.32},
            ),
            "time": Parameter(
                "time",
                description="Window bracketing one Sentinel-1 and one Sentinel-2 pass",
                schema={"type": "array", "subtype": "temporal-interval"},
                default=["2026-03-20", "2026-03-25"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for NDWI and the true-color composite",
                default=s2_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Sentinel-2 data collection identifier",
                default="sentinel-2-l1c",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum scene-level cloud cover for the S2 image (tropical, so a looser threshold)",
                schema={"type": "number"},
                default=50,
            ),
            "s1_collection": Parameter(
                "s1_collection",
                description="Sentinel-1 GRD collection identifier (canonical; mapped per endpoint)",
                default="sentinel-1-grd",
            ),
            "s1_bands": Parameter(
                "s1_bands",
                description="Sentinel-1 polarizations needed (VV, VH)",
                default=["vv", "vh"],
            ),
        },
        # Sunda Strait, Indonesia: the shipping/ferry chokepoint between Java
        # and Sumatra (near the Merak-Bakauheni crossing) -- dense inter-
        # island ferry and cargo traffic funnels through this narrow strait.
        "sunda_strait_indonesia": {
            "location_name": "Sunda Strait, Indonesia",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent over the Sunda Strait near the Merak-Bakauheni crossing, Java/Sumatra",
                schema={"type": "object", "subtype": "bounding-box"},
                default={
                    "west": 105.9149,
                    "south": -5.9683,
                    "east": 106.0210,
                    "north": -5.8729,
                },
            ),
            "time": Parameter(
                "time",
                description="Window bracketing one Sentinel-1 and one Sentinel-2 pass",
                schema={"type": "array", "subtype": "temporal-interval"},
                default=["2026-03-13", "2026-03-16"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for NDWI and the true-color composite",
                default=s2_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Sentinel-2 data collection identifier",
                default="sentinel-2-l1c",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum scene-level cloud cover for the S2 image (tropical, so a looser threshold)",
                schema={"type": "number"},
                default=20,
            ),
            "s1_collection": Parameter(
                "s1_collection",
                description="Sentinel-1 GRD collection identifier (canonical; mapped per endpoint)",
                default="sentinel-1-grd",
            ),
            "s1_bands": Parameter(
                "s1_bands",
                description="Sentinel-1 polarizations needed (VV, VH)",
                default=["vv", "vh"],
            ),
        },
    }

    return parameter_sets
