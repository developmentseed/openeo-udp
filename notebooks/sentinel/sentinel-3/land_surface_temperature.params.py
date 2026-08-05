# License: CC-BY-SA-4.0
# Origin: Converted from Sentinel Hub evalscript
# Original evalscript: https://custom-scripts.sentinel-hub.com/sentinel-3/land_surface_temperature/
# Source: Sentinel Hub Custom Scripts (CC-BY-SA-4.0)
# Conversion: Development Seed (openEO-UDP project)
"""Parameter definitions for the Sentinel-3 Land Surface Temperature algorithm.

This is a **two-sensor fusion** on a single Sentinel-3 platform:

- **SLSTR** ``S8`` -- the 10.854 um thermal channel, delivered as **brightness
  temperature in Kelvin**. This is the temperature measurement.
- **OLCI** ``B06``, ``B08``, ``B17`` -- delivered as **0-1 reflectance**. B17/B08
  give NDVI, which scales the surface emissivity; B06 only participates in the
  validity test.

The brightness temperature is then corrected for emissivity to give land surface
temperature in degrees Celsius.

Units, and why ``reflectance_scale`` is not used here
----------------------------------------------------
``reflectance_scale`` is an *endpoint*-level attribute describing the Sentinel-2
collections (0-10000 integers on CDSE). Neither Sentinel-3 collection follows it:
SLSTR thermal bands are Kelvin and OLCI is already 0-1 reflectance. The notebook
therefore must **not** divide by it. This costs nothing in accuracy: NDVI is a
normalised ratio and so scale-invariant, and the only other use of the OLCI bands
is a ``> 0`` validity test, which is scale-invariant too.

Daytime acquisitions only
-------------------------
Sentinel-3 crosses the equator at ~10:00 local descending (**daytime**) and again
at night ascending. SLSTR, being thermal, images on both passes; OLCI, being
optical, only images in daylight. On CDSE an unfiltered SLSTR request over a
whole day returns the **night** pass, which would pair night-time thermal with
daytime NDVI and read roughly 15 C too cold. Every parameter set below therefore
relies on the notebook filtering SLSTR to ``orbitDirection == "DESCENDING"``.

Note that OLCI does **not** support that property filter on CDSE (the catalogue
rejects it with "Querying is not supported on property 'sat:orbit_state'"), and
does not need it, so the filter is applied to SLSTR alone.

Choosing the window
-------------------
Each window is one day wide, which resolves to a single daytime overpass -- the
single-image case the original documents as ``option = 0``.

**Cloud must be checked empirically.** The algorithm has no cloud mask, and
Sentinel-3 STAC items carry no ``eo:cloud_cover``, so cloud cannot be pre-filtered
the way it is for Sentinel-2. Cloud tops are far colder than any land surface, so
a contaminated scene shows up as a long cold tail: every date below was screened
by running the algorithm and rejecting any date with pixels below -10 C. The
Po Valley set is a worked example -- its obvious heatwave dates (18, 22 and
24 July 2023) all turned out cloudy, with medians as low as -31 C.
"""

from openeo.api.process import Parameter


def get_parameters():
    """Return available parameter sets for the Sentinel-3 LST algorithm.

    Returns:
        Dictionary mapping parameter set names to parameter dictionaries.
        Each parameter set includes:
        - location_name: Human-readable location identifier
        - bounding_box: Spatial extent as Parameter object (runtime)
        - time: Window containing one daytime overpass (runtime)
        - collection / bands: Sentinel-3 SLSTR thermal (mapped automatically)
        - olci_collection / olci_bands: Sentinel-3 OLCI (mapped in the notebook)
    """

    # S8 is the 10.854 um thermal channel the LST retrieval is built on.
    slstr_bands = ["s8"]
    # B06 is only used by the validity test; B08/B17 give NDVI.
    olci_bands = ["b06", "b08", "b17"]

    def _shared(bbox_description, bbox, time_description, time, animation_time):
        """Assemble one parameter set; only the AOI and the dates vary."""
        return {
            "bounding_box": Parameter(
                "bounding_box", description=bbox_description, default=bbox
            ),
            "time": Parameter("time", description=time_description, default=time),
            "animation_time": Parameter(
                "animation_time",
                description=(
                    "Date range for the daily animation; one frame is rendered per day "
                    "in [start, end)"
                ),
                default=animation_time,
            ),
            "collection": Parameter(
                "collection",
                description="Sentinel-3 SLSTR collection identifier",
                default="sentinel-3-slstr",
            ),
            "bands": Parameter(
                "bands",
                description="SLSTR thermal band (brightness temperature, Kelvin)",
                default=slstr_bands,
            ),
            "olci_collection": Parameter(
                "olci_collection",
                description="Sentinel-3 OLCI L1B collection identifier (canonical; mapped per endpoint)",
                default="sentinel-3-olci-l1b",
            ),
            "olci_bands": Parameter(
                "olci_bands",
                description="OLCI bands for NDVI (B17/B08) and the validity test (B06)",
                default=olci_bands,
            ),
        }

    parameter_sets = {
        # Sicily during the July 2023 European heatwave -- the showcase the
        # original evalscript is presented with, as a day-by-day animation over
        # the whole month. 24 July was the peak: Palermo and the north coast were
        # burning, and Etna's dark lava fields push the scene maximum past 55 C.
        # Verified clean (100% valid, no cold tail); note that 21, 23 and 25 July
        # are cloud-affected, which the animation shows rather than hides.
        "sicily_italy_2023": {
            "location_name": "Sicily, Italy (July 2023 heatwave)",
            **_shared(
                "Spatial extent covering the whole island of Sicily",
                {"west": 12.35, "south": 36.60, "east": 15.70, "north": 38.35},
                "Window containing the 24 Jul 2023 daytime overpass (heatwave peak)",
                ["2023-07-24", "2023-07-25"],
                ["2023-07-01", "2023-08-01"],
            ),
        },
        # Guadiana valley, Extremadura, Spain. A dry summer landscape with
        # irrigated river valleys and reservoirs, so one frame spans cool water,
        # cool irrigated crops and very hot bare soil -- the full emissivity
        # cascade in a single scene. Verified clean: 100% valid, median 36 C,
        # minimum 12 C over the reservoirs.
        "guadiana_spain_2023": {
            "location_name": "Guadiana valley, Extremadura, Spain",
            **_shared(
                "Spatial extent over the Guadiana valley and surrounding dehesa, Extremadura",
                {"west": -6.6, "south": 38.6, "east": -5.8, "north": 39.2},
                "Window containing the 15 Jul 2023 daytime overpass",
                ["2023-07-15", "2023-07-16"],
                ["2023-07-01", "2023-08-01"],
            ),
        },
        # Nile Delta, Egypt. The sharpest LST contrast available anywhere: dense
        # irrigated delta against bare desert, with the boundary drawn by water
        # rather than terrain. Verified clean: 100% valid, median 38 C, max 47 C.
        "nile_delta_egypt_2023": {
            "location_name": "Nile Delta, Egypt",
            **_shared(
                "Spatial extent over the southern Nile Delta and the adjoining desert margin",
                {"west": 30.2, "south": 29.8, "east": 31.6, "north": 30.9},
                "Window containing the 15 Jul 2023 daytime overpass",
                ["2023-07-15", "2023-07-16"],
                ["2023-07-01", "2023-08-01"],
            ),
        },
        # Po Valley, northern Italy. A densely farmed and heavily urbanised plain
        # ringed by mountains, useful for seeing urban and irrigated signals side
        # by side. 22 Aug 2023 was chosen after the obvious July heatwave dates
        # proved cloudy; verified clean: 100% valid, median 32 C, max 39 C.
        "po_valley_italy_2023": {
            "location_name": "Po Valley, Italy",
            **_shared(
                "Spatial extent over the central Po plain between Milan and Cremona",
                {"west": 8.8, "south": 44.8, "east": 10.2, "north": 45.6},
                "Window containing the 22 Aug 2023 daytime overpass",
                ["2023-08-22", "2023-08-23"],
                ["2023-08-01", "2023-09-01"],
            ),
        },
    }

    return parameter_sets
