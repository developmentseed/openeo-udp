# License: CC-BY-SA-4.0
# Origin: Converted from Sentinel Hub evalscript
# Original evalscript: https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/burned_area/
# Source: Sentinel Hub Custom Scripts (CC-BY-SA-4.0)
# Conversion: Development Seed (openEO-UDP project)
"""Parameter definitions for the Multitemporal Burnt Area Analysis algorithm.

This is a **bi-temporal change-detection** algorithm on Sentinel-2. It compares
the Normalized Burn Ratio (NBR) of a pre-fire and a post-fire acquisition::

    NBR   = (B08 - B12) / (B08 + B12)
    dNBR  = NBR(pre) - NBR(post)

Healthy vegetation is bright in the near infrared (B08) and dark in the SWIR
(B12), so it has a high NBR. Fire destroys that structure and leaves char and
ash, which reverse the relationship, so NBR drops sharply and dNBR rises. The
result is rendered as a natural-colour image of the **post-fire** scene, tinted
by burn severity:

- ``dNBR < 0.27``  -- unburned, plain natural colour
- ``0.27 <= dNBR < 0.66`` -- moderate burn, red and green both raised (yellow tint)
- ``dNBR >= 0.66`` -- severe burn, only red raised (red tint)

Each parameter set therefore carries **two** temporal windows:

- ``time_pre``:  window bracketing the pre-fire acquisition
- ``time_post``: window bracketing the post-fire acquisition

Both windows are one day wide so each resolves to a single acquisition, and every
date below was checked against the CDSE STAC catalogue on two counts:

1. **Low cloud cover** -- a cloudy pixel corrupts NBR on either date and produces
   spurious severity.
2. **Full swath coverage of the AOI** -- this is easy to miss and matters just as
   much. Sentinel-2's relative orbits alternate, and an AOI sitting near the edge
   of one orbit's swath is only partly imaged on those dates. The granule may
   still report 0% cloud, so filtering on cloud alone happily selects a date that
   leaves most of the AOI as no-data. The Corbières set below is exactly that
   trap: its cleanest dates fall on relative orbit 51, which covers only ~15% of
   the AOI, so both its dates are taken from orbit 8 instead.

Prefer a pre/post pair from the **same relative orbit**, which guarantees matched
coverage and near-identical viewing geometry on both dates.

Only the **post-fire** cube needs the full band set, because the natural-colour
rendering is built entirely from the post-fire image; the pre-fire cube supplies
just the NIR/SWIR pair needed for its NBR. Hence the separate ``pre_bands``.

Note: Sentinel-2 reflectance must be divided by ``reflectance_scale`` (10000 on
CDSE) before the indices and the colour stretch are computed.
"""

from openeo.api.process import Parameter


def get_parameters():
    """Return available parameter sets for the multitemporal burnt area algorithm.

    Returns:
        Dictionary mapping parameter set names to parameter dictionaries.
        Each parameter set includes:
        - location_name: Human-readable location identifier
        - bounding_box: Spatial extent as Parameter object (runtime)
        - time_pre: Window bracketing the pre-fire acquisition (runtime)
        - time_post: Window bracketing the post-fire acquisition (runtime)
        - cloud_cover: Maximum scene-level cloud cover for both images (runtime)
        - collection: Sentinel-2 L2A collection identifier
        - bands: Post-fire bands (colour rendering + NBR)
        - pre_bands: Pre-fire bands (NBR only)
    """

    # Post-fire image drives both the natural-colour render and its own NBR.
    post_bands = ["b02", "b03", "b04", "b05", "b08", "b12"]
    # Pre-fire image is only ever used for NBR, so NIR + SWIR suffice.
    pre_bands = ["b08", "b12"]

    def _shared(bbox_description, bbox, pre_description, pre, post_description, post):
        """Assemble one parameter set; only the AOI and the two dates vary."""
        return {
            "bounding_box": Parameter(
                "bounding_box", description=bbox_description, default=bbox
            ),
            "time_pre": Parameter("time_pre", description=pre_description, default=pre),
            "time_post": Parameter(
                "time_post", description=post_description, default=post
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum scene-level cloud cover for the pre- and post-fire images",
                default=40,
            ),
            "collection": Parameter(
                "collection",
                description="Sentinel-2 L2A collection identifier",
                default="sentinel-2-l2a",
            ),
            "bands": Parameter(
                "bands",
                description="Post-fire bands: natural-colour rendering plus NIR/SWIR for NBR",
                default=post_bands,
            ),
            "pre_bands": Parameter(
                "pre_bands",
                description="Pre-fire bands: NIR and SWIR for the baseline NBR only",
                default=pre_bands,
            ),
        }

    parameter_sets = {
        # The original evalscript's own example: the Knysna fires of 7-11 June
        # 2017 on South Africa's Garden Route, which burned roughly 15,000 ha of
        # fynbos, plantation and indigenous forest and destroyed much of the town.
        # Both of the original's dates are cloud-free (0.0% and 8.1%).
        "knysna_south_africa_2017": {
            "location_name": "Knysna, South Africa (June 2017 fires)",
            **_shared(
                "Spatial extent over Knysna and the Garden Route burn scar, South Africa",
                {"west": 22.90, "south": -34.08, "east": 23.25, "north": -33.90},
                "Pre-fire acquisition window (15 May 2017, 0% cloud)",
                ["2017-05-15", "2017-05-16"],
                "Post-fire acquisition window (24 Jun 2017, 8% cloud)",
                ["2017-06-24", "2017-06-25"],
            ),
        },
        # Pedrogao Grande, Portugal: the 17-24 June 2017 fire complex, one of the
        # deadliest in Portuguese history, burning ~45,000 ha of eucalyptus and
        # maritime pine. Pre 4 Jun (1.5% cloud), post 4 Jul (6.1%).
        "pedrogao_grande_portugal_2017": {
            "location_name": "Pedrógão Grande, Portugal (June 2017 fire)",
            **_shared(
                "Spatial extent over the Pedrógão Grande burn scar, central Portugal",
                {"west": -8.35, "south": 39.80, "east": -8.00, "north": 40.05},
                "Pre-fire acquisition window (4 Jun 2017, 1.5% cloud)",
                ["2017-06-04", "2017-06-05"],
                "Post-fire acquisition window (4 Jul 2017, 6.1% cloud)",
                ["2017-07-04", "2017-07-05"],
            ),
        },
        # Corbières, Aude, France: the fire that started 5 Aug 2025 near Lagrasse
        # and burned ~11,000 ha of garrigue and vineyard before being contained on
        # 10 Aug. Both dates are relative orbit 8, which covers this AOI in full;
        # the alternating orbit 51 clips it to ~15% and must be avoided here even
        # though several orbit-51 dates are cloud-free.
        "corbieres_aude_france_2025": {
            "location_name": "Corbières, Aude, France (August 2025 fire)",
            **_shared(
                "Spatial extent over the Corbières burn scar, Aude, France",
                {"west": 2.58, "south": 42.94, "east": 2.95, "north": 43.14},
                "Pre-fire acquisition window (10 Jul 2025, orbit 8, 1.4% cloud, full coverage)",
                ["2025-07-10", "2025-07-11"],
                "Post-fire acquisition window (11 Aug 2025, orbit 8, 0.3% cloud, one day after containment)",
                ["2025-08-11", "2025-08-12"],
            ),
        },
    }

    return parameter_sets
