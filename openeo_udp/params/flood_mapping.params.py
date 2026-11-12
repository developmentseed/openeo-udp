# License: CC-BY-SA-4.0
# Origin: Converted from Sentinel Hub evalscript
# Original evalscript: https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-1/flood_mapping/
# Source: Sentinel Hub Custom Scripts (CC-BY-SA-4.0)
# Conversion: Development Seed (openEO-UDP project)
"""Parameter definitions for the Sentinel-1 Flood Mapping algorithm.

This is a **bi-temporal change-detection** algorithm on Sentinel-1 GRD VV
backscatter. It compares one acquisition from *before* a flood with one from
*during* the flood and renders the pair as an RGB composite::

    R = 1.5 x VV(before)
    G = 1.5 x VV(during)
    B = 1.5 x VV(during)

Open water reflects the radar pulse away from the sensor (specular reflection),
so newly inundated land turns dark in the "during" image while it was bright in
the "before" image -- those pixels come out **red**. Permanent water is dark in
both and stays black; unchanged land is grey; built-up areas whose double-bounce
response *increases* during a flood come out **cyan**.

Each parameter set therefore carries **two** temporal windows rather than one:

- ``time_before``: window bracketing the pre-flood acquisition
- ``time_during``: window bracketing the flood acquisition

Both windows are intentionally one day wide so that each resolves to a *single*
Sentinel-1 pass. The two dates in every set below were checked against the CDSE
STAC catalogue and belong to the **same relative orbit and pass direction**, so
the incidence-angle geometry is identical and the backscatter difference is due
to the surface, not to the viewing geometry. Pairing two different relative
orbits produces large spurious differences over terrain and must be avoided.

Note: Sentinel-1 GRD is served as calibrated, ortho-corrected linear backscatter
(float, unit 1), which is the same convention the original evalscript assumes.
The ``reflectance_scale`` injected by the endpoint mapper applies to optical
reflectance only and is **not** used by this algorithm.
"""

from openeo.api.process import Parameter


def get_parameters():
    """Return available parameter sets for the flood mapping algorithm.

    Returns:
        Dictionary mapping parameter set names to parameter dictionaries.
        Each parameter set includes:
        - location_name: Human-readable location identifier
        - bounding_box: Spatial extent as Parameter object (runtime)
        - time_before: Window bracketing the pre-flood acquisition (runtime)
        - time_during: Window bracketing the flood acquisition (runtime)
        - flood_threshold: Backscatter drop above which a pixel counts as
          flooded, used by the optional binary-mask variant (runtime)
        - bands: Required Sentinel-1 polarization as Parameter object
        - collection: Data collection identifier as Parameter object
    """

    # The algorithm reads a single co-polarized channel; VV is the most
    # sensitive to the smooth-surface (specular) signature of standing water.
    flood_bands = ["vv"]

    # Original evalscript default: 0.05 on the 1.5x-scaled difference. The
    # script page also documents 0.08 as the less sensitive alternative.
    default_threshold = 0.05

    parameter_sets = {
        # The original evalscript's default example: the March 2019 Golestan
        # floods in northern Iran. Heavy rain from 17 March burst the Gorgan
        # river banks and inundated the plain around Aq Qala (Aghghala).
        # Both dates are relative orbit 137, descending.
        "aq_qala_iran_2019": {
            "location_name": "Aq Qala, Golestan, Iran (March 2019 flood)",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent over the Gorgan river floodplain around Aq Qala, Iran",
                default={"west": 54.30, "south": 36.90, "east": 54.65, "north": 37.20},
            ),
            "time_before": Parameter(
                "time_before",
                description="Pre-flood acquisition window (11 Mar 2019, orbit 137 descending)",
                default=["2019-03-11", "2019-03-12"],
            ),
            "time_during": Parameter(
                "time_during",
                description="Flood acquisition window (23 Mar 2019, orbit 137 descending)",
                default=["2019-03-23", "2019-03-24"],
            ),
            "flood_threshold": Parameter(
                "flood_threshold",
                description="Backscatter drop (on the 1.5x-scaled VV difference) above which a pixel is classed as flooded",
                default=default_threshold,
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-1 GRD polarization band",
                default=flood_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Sentinel-1 GRD collection identifier",
                default="sentinel-1-grd",
            ),
        },
        # The 29 October 2024 DANA over the Valencia region, Spain: a
        # cut-off low dropped ~490 mm in eight hours over the Poyo and Magro
        # basins and flooded the Horta Sud plain south of Valencia city.
        # Both dates are relative orbit 103, ascending, bracketing the event.
        "valencia_spain_2024": {
            "location_name": "Valencia, Spain (October 2024 DANA flood)",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent over the Horta Sud plain and Albufera lagoon, Valencia, Spain",
                default={"west": -0.50, "south": 39.15, "east": -0.25, "north": 39.42},
            ),
            "time_before": Parameter(
                "time_before",
                description="Pre-flood acquisition window (19 Oct 2024, orbit 103 ascending)",
                default=["2024-10-19", "2024-10-20"],
            ),
            "time_during": Parameter(
                "time_during",
                description="Flood acquisition window (31 Oct 2024, two days after the DANA, orbit 103 ascending)",
                default=["2024-10-31", "2024-11-01"],
            ),
            "flood_threshold": Parameter(
                "flood_threshold",
                description="Backscatter drop (on the 1.5x-scaled VV difference) above which a pixel is classed as flooded",
                default=default_threshold,
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-1 GRD polarization band",
                default=flood_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Sentinel-1 GRD collection identifier",
                default="sentinel-1-grd",
            ),
        },
        # The original evalscript's second commented example: the January 2019
        # Uruguay river flood at Uruguaiana, Rio Grande do Sul, Brazil. The
        # script's own dates (6 Jan / 14 Jan) fall on two *different* relative
        # orbits, so the "during" date is moved to the next pass of the same
        # orbit as the "before" date: both are relative orbit 170, descending.
        "uruguaiana_brazil_2019": {
            "location_name": "Uruguaiana, Rio Grande do Sul, Brazil (January 2019 flood)",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent over the Uruguay river floodplain at Uruguaiana, Brazil",
                default={
                    "west": -57.15,
                    "south": -29.90,
                    "east": -56.95,
                    "north": -29.70,
                },
            ),
            "time_before": Parameter(
                "time_before",
                description="Pre-flood acquisition window (6 Jan 2019, orbit 170 descending)",
                default=["2019-01-06", "2019-01-07"],
            ),
            "time_during": Parameter(
                "time_during",
                description="Flood acquisition window (18 Jan 2019, orbit 170 descending)",
                default=["2019-01-18", "2019-01-19"],
            ),
            "flood_threshold": Parameter(
                "flood_threshold",
                description="Backscatter drop (on the 1.5x-scaled VV difference) above which a pixel is classed as flooded",
                default=default_threshold,
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-1 GRD polarization band",
                default=flood_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Sentinel-1 GRD collection identifier",
                default="sentinel-1-grd",
            ),
        },
    }

    return parameter_sets
