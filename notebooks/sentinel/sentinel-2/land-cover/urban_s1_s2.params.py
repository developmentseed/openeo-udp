# License: CC-BY-SA-4.0
# Origin: Converted from Sentinel Hub evalscript
# Original evalscript: https://custom-scripts.sentinel-hub.com/custom-scripts/data-fusion/urban_s1_s2/
# Source: Sentinel Hub Custom Scripts (CC-BY-SA-4.0)
# Conversion: Development Seed (openEO-UDP project)
"""Parameter definitions for the Urban Detection (S1/S2 fusion) algorithm.

This is a **multi-sensor data-fusion** algorithm that needs *three* acquisitions
of the same scene, all from the same short time window:

- **Sentinel-2 L1C** (top of atmosphere) -- ``B02, B03, B04, B08, B11``. Drives
  the NDVI and NDMI masks and supplies the darkened true-colour fallback.
- **Sentinel-1 GRD** -- ``VH, VV``. Bright backscatter in either polarization is
  the built-up test.
- **Sentinel-2 L2A** (bottom of atmosphere) -- ``B02, B03, B04``. Supplies the
  true-colour rendering for the vegetation and water branches.

Each pixel falls through a four-way priority cascade -- vegetation, then water,
then built-up, then a catch-all -- so exactly one branch renders each pixel.

Because the algorithm fuses three collections, only the **L1C** collection/bands
flow through the standard ParameterManager mapping (which also injects
``reflectance_scale`` and the dimension names). The **L2A** and **Sentinel-1**
collection/bands are kept as separate keys and mapped through the same endpoint
mapper inside the notebook, since the automatic mapping only handles the single
``collection``/``bands`` pair.

Choosing the time window
------------------------
The window must contain **one** Sentinel-2 pass and **one** Sentinel-1 pass, and
they should be as close together as possible: the algorithm compares an optical
mask against a radar threshold pixel by pixel, so any real change between the two
dates shows up as misclassification. Every window below was checked against the
CDSE STAC catalogue; the Cairo set is the best case, with both sensors acquiring
on the same day.

Note: Sentinel-1 GRD is served as calibrated, ortho-corrected *linear*
backscatter (float, unit 1), which is what the ``0.2`` threshold and the
``5.5``/``8`` display gains assume. Sentinel-2 reflectance must be divided by
``reflectance_scale`` (10000 on CDSE) before the indices are computed.
"""

from openeo.api.process import Parameter


def get_parameters():
    """Return available parameter sets for the urban S1/S2 fusion algorithm.

    Returns:
        Dictionary mapping parameter set names to parameter dictionaries.
        Each parameter set includes:
        - location_name: Human-readable location identifier
        - bounding_box: Spatial extent as Parameter object (runtime)
        - time: Window containing one S2 and one S1 pass (runtime)
        - cloud_cover: Maximum scene-level cloud cover for the S2 images (runtime)
        - collection / bands: Sentinel-2 L1C (mapped automatically)
        - l2a_collection / l2a_bands: Sentinel-2 L2A (mapped in the notebook)
        - s1_collection / s1_bands: Sentinel-1 GRD (mapped in the notebook)
    """

    # L1C drives NDVI (B08/B04), NDMI (B08/B11) and the true-colour fallback.
    l1c_bands = ["b02", "b03", "b04", "b08", "b11"]
    # L2A supplies true colour for the vegetation and water branches only.
    l2a_bands = ["b02", "b03", "b04"]
    # Both polarizations feed the built-up test; VH also drives its red/blue.
    s1_bands = ["vh", "vv"]

    def _shared(bbox_description, bbox, time_description, time, cloud_cover):
        """Assemble one parameter set; only the AOI/TOI actually vary."""
        return {
            "bounding_box": Parameter(
                "bounding_box",
                description=bbox_description,
                schema={"type": "object", "subtype": "bounding-box"},
                default=bbox,
            ),
            "time": Parameter(
                "time",
                description=time_description,
                schema={"type": "array", "subtype": "temporal-interval"},
                default=time,
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum scene-level cloud cover for the Sentinel-2 images",
                schema={"type": "number"},
                default=cloud_cover,
            ),
            "collection": Parameter(
                "collection",
                description="Sentinel-2 L1C collection identifier",
                default="sentinel-2-l1c",
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 L1C bands for the NDVI/NDMI masks and the fallback true colour",
                default=l1c_bands,
            ),
            "l2a_collection": Parameter(
                "l2a_collection",
                description="Sentinel-2 L2A collection identifier (canonical; mapped per endpoint)",
                default="sentinel-2-l2a",
            ),
            "l2a_bands": Parameter(
                "l2a_bands",
                description="Sentinel-2 L2A true-colour bands for the vegetation and water branches",
                default=l2a_bands,
            ),
            "s1_collection": Parameter(
                "s1_collection",
                description="Sentinel-1 GRD collection identifier (canonical; mapped per endpoint)",
                default="sentinel-1-grd",
            ),
            "s1_bands": Parameter(
                "s1_bands",
                description="Sentinel-1 polarizations used for the built-up test",
                default=s1_bands,
            ),
        }

    parameter_sets = {
        # Best case: Sentinel-2 (0% cloud) and Sentinel-1 both acquired on
        # 12 June 2023, so optical and radar are genuinely simultaneous. Cairo
        # also exercises all four branches in one frame -- the Nile (water),
        # irrigated Delta farmland (vegetation), dense continuous built-up, and
        # bare desert on the Giza side (fallback).
        "cairo_egypt": {
            "location_name": "Cairo, Egypt",
            **_shared(
                "Spatial extent over central Cairo and Giza, spanning the Nile and the desert margin",
                {"west": 31.15, "south": 29.98, "east": 31.35, "north": 30.12},
                "Window containing the 12 Jun 2023 Sentinel-2 and Sentinel-1 passes (same day)",
                ["2023-06-12", "2023-06-13"],
                40,
            ),
        },
        # Bologna: Sentinel-2 on 7 Jul 2023 (2.4% cloud), Sentinel-1 on 9 Jul
        # (relative orbit 95, descending) -- two days apart. A compact European
        # city surrounded by intensively farmed Po valley cropland.
        "bologna_italy": {
            "location_name": "Bologna, Italy",
            **_shared(
                "Spatial extent over Bologna and the surrounding Po valley farmland",
                {"west": 11.20, "south": 44.45, "east": 11.48, "north": 44.56},
                "Window containing the 7 Jul 2023 Sentinel-2 and 9 Jul 2023 Sentinel-1 passes",
                ["2023-07-07", "2023-07-10"],
                40,
            ),
        },
        # Paris: Sentinel-2 on 7 Sep 2023 (0% cloud), Sentinel-1 on 8 Sep
        # (relative orbit 110, descending) -- one day apart. A dense historic
        # core with the Seine, large parks and a sharp urban/suburban gradient.
        "paris_france": {
            "location_name": "Paris, France",
            **_shared(
                "Spatial extent over central Paris, the Seine and the inner suburbs",
                {"west": 2.20, "south": 48.78, "east": 2.50, "north": 48.95},
                "Window containing the 7 Sep 2023 Sentinel-2 and 8 Sep 2023 Sentinel-1 passes",
                ["2023-09-07", "2023-09-09"],
                40,
            ),
        },
    }

    return parameter_sets
