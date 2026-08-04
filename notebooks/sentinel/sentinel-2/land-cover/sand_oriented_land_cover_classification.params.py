# License: CC-BY-SA-4.0
# Origin: Converted from Sentinel Hub evalscript
# Original evalscript: https://custom-scripts.sentinel-hub.com/custom-scripts/data-fusion/sand-oriented_land_cover_classification_s1_s2/
# Source: Sentinel Hub Custom Scripts (CC-BY-SA-4.0)
# Conversion: Development Seed (openEO-UDP project)
"""Parameter definitions for the Sand-Oriented Land Cover Classification algorithm.

This is a **multi-sensor data-fusion** algorithm that needs two acquisitions of the
same scene, both from the same short time window:

- **Sentinel-2 L2A** -- ``B02, B03, B04, B08, B11, B12``. Drives NDVI, MNDWI, BSI
  and the (new) MNDSI sand index used by the classification cascade.
- **Sentinel-1 GRD** -- ``VH, VV``. Bright backscatter in either polarization is
  the built-up test.

Each pixel falls through a seven-way priority cascade -- built-up, shrub/
grassland, dense vegetation, water, bare soil, sand, then a fallback -- so
exactly one class renders each pixel.

Because the algorithm fuses two collections, only the **Sentinel-2** collection/
bands flow through the standard ParameterManager mapping (which also injects
``reflectance_scale`` and the dimension names). The **Sentinel-1**
collection/bands are kept as separate keys and mapped through the same endpoint
mapper inside the notebook, since the automatic mapping only handles the single
``collection``/``bands`` pair.

Choosing the time window
------------------------
The window must contain **one** Sentinel-2 pass and **one** Sentinel-1 pass, and
they should be as close together as possible: the algorithm compares optical
indices against a radar threshold pixel by pixel, so any real change between the
two dates shows up as misclassification.

Note: Sentinel-1 GRD is served as calibrated, ortho-corrected *linear*
backscatter (float, unit 1), which is what the ``0.2`` built-up threshold
assumes. Sentinel-2 reflectance must be divided by ``reflectance_scale`` (10000
on CDSE) before the indices are computed.
"""

from openeo.api.process import Parameter


def get_parameters():
    """Return available parameter sets for the sand-oriented land cover algorithm.

    Returns:
        Dictionary mapping parameter set names to parameter dictionaries.
        Each parameter set includes:
        - location_name: Human-readable location identifier
        - bounding_box: Spatial extent as Parameter object (runtime)
        - time: Window containing one S2 and one S1 pass (runtime)
        - cloud_cover: Maximum scene-level cloud cover for the S2 images
        - collection / bands: Sentinel-2 L2A (mapped automatically)
        - s1_collection / s1_bands: Sentinel-1 GRD (mapped in the notebook)
    """

    # S2L2A drives NDVI (B08/B04), MNDWI (B03/B12), BSI (B02/B04/B08/B11) and the
    # sand index MNDSI (B02/B04).
    s2_bands = ["b02", "b03", "b04", "b08", "b11", "b12"]
    # Both polarizations feed the built-up test.
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
                default=cloud_cover,
            ),
            "collection": Parameter(
                "collection",
                description="Sentinel-2 L2A collection identifier",
                default="sentinel-2-l2a",
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 L2A bands for the NDVI/MNDWI/BSI/MNDSI indices",
                default=s2_bands,
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
        # Cropland plain, expect green, yellow, and red
        "cropland_plain_croatia": {
            "location_name": "Cropland Plain, Istria Coast, Croatia",
            **_shared(
                "Spatial extent for Cropland Plain, Istria Coast, Croatia",
                {"west": 14.09, "south": 45.174, "east": 14.27, "north": 45.25},
                "Window containing a Sentinel-2 and Sentinel-1 pass in July 2026",
                ["2026-07-28", "2026-08-01"],
                30,
            ),
        },
        # Dakar peninsula, expect orange and red color
        "dakar_peninsula_senegal": {
            "location_name": "Dakar Peninsula, Senegal",
            **_shared(
                "Spatial extent for the Dakar Peninsula, Senegal",
                {"west": -17.6048, "south": 14.613, "east": -17.2182, "north": 14.8681},
                "Window containing a Sentinel-2 and Sentinel-1 pass in June 2026",
                ["2026-06-23", "2026-06-26"],
                # Sentinel-1: 2026-06-25
                # Sentinel-2: 2026-06-25
                30,
            ),
        },
        # Aceh, Indonesia, expect green, yellow, red, white, and orange color
        "aceh_indonesia": {
            "location_name": "Aceh, Indonesia",
            **_shared(
                "Spatial extent for Aceh, Indonesia",
                {"west": 98.2588, "south": 4.02, "east": 98.3553, "north": 4.0861},
                "Window containing a Sentinel-2 and Sentinel-1 pass in April 2026",
                ["2026-04-08", "2026-04-13"],
                # Sentinel-2: 2026-04-12
                # Sentinel-1: 2026-04-09
                30,
            ),
        },
    }

    return parameter_sets
