# License: CC-BY-SA-4.0
# Origin: Converted from Sentinel Hub evalscript
# Original evalscript: https://custom-scripts.sentinel-hub.com/data-fusion/olci_under_s5/
# Source: Sentinel Hub Custom Scripts (CC-BY-SA-4.0)
# Conversion: Development Seed (openEO-UDP project)
"""Parameter definitions for the OLCI-under-Sentinel-5P data-fusion algorithm.

This is a **cross-mission** fusion, not a same-platform one like the Sentinel-3
Land Surface Temperature notebook:

- **Sentinel-3 OLCI L1B** ``B04``/``B06``/``B08`` -- a 300 m true-colour base map,
  always present, used as-is (0-1 reflectance).
- **Sentinel-5P L2** (TROPOMI) -- a single atmospheric product on a ~7 km grid,
  drawn as a six-stop colour ramp wherever it has data, with OLCI showing through
  where it does not.

Only ``copernicus_dataspace`` serves Sentinel-5P
--------------------------------------------------
CDSE is currently the only endpoint in this repository with a Sentinel-5P
mapping (``SENTINEL5P_L2`` in ``openeo_udp/collections.py``). The
``ds_development``/``eopf_explorer``/``localhost_dev`` endpoints have no S5P
collection at all, so this notebook is CDSE-only.

CDSE also states, in the collection's own STAC description, that
**SENTINEL_5P_L2 only supports loading one band at a time** -- so ``s5p_bands``
below always holds exactly one canonical band name, never a list of several.

The product (and its colour-ramp range) is algorithm-intrinsic, not a runtime knob
-----------------------------------------------------------------------------------
Which atmospheric product is displayed, and the ``(min, max)`` range its colour
ramp is stretched over, are baked into the exported graph via ``s5p_bands``
(picked here) and the ``S5P_PRODUCT_RANGES`` lookup table in the notebook --
mirroring how the original evalscript is repurposed by editing the script text,
not by an evalscript parameter. Only ``bounding_box`` and ``time`` are exposed as
runtime UDP parameters.

Choosing the four parameter sets below
---------------------------------------
- **Mt Etna, cloud top pressure** is the original's own default product, over a
  scene with both a partial cloud deck (showing the colour ramp) and clear land
  (showing the OLCI fallback) -- the clearest single demonstration of the gap-fill
  behaviour this script is built around.
- **Mt Etna, SO2** reuses the *same* bounding box and date as a direct product
  comparison at one location -- exactly the kind of side-by-side the original's
  own "replace all mentions" comment block invites. Etna is one of the most
  persistently SO2-emitting volcanoes on Earth.
- **Po Valley, NO2** is a well-known NO2 hotspot (heavy industry, traffic and
  valley temperature inversions); it renders a strong, well-defined product
  signal rather than a background one.
- **Chiquitania, Bolivia, CO** revisits the same 2019 fire event used by
  ``s2_s1_forest_fire_progression.params.py``, during one of Bolivia's most
  severe wildfire seasons -- carbon monoxide from biomass burning is one of the
  clearest applications of this product.

All four were run end-to-end against CDSE while developing this notebook.
"""

from openeo.api.process import Parameter


def get_parameters():
    """Return available parameter sets for the OLCI-under-S5P algorithm.

    Returns:
        Dictionary mapping parameter set names to parameter dictionaries.
        Each parameter set includes:
        - location_name: Human-readable location identifier
        - bounding_box: Spatial extent as Parameter object (runtime)
        - time: Acquisition window as Parameter object (runtime)
        - collection / bands: Sentinel-3 OLCI L1B true-colour base (mapped
          automatically via quick_connect)
        - s5p_collection / s5p_bands: Sentinel-5P L2, ONE product (mapped in the
          notebook via apply_endpoint_mapping, since it needs the CDSE-only route)
    """

    # OLCI true-colour base: same three bands in every parameter set.
    olci_bands = ["b04", "b06", "b08"]

    def _shared(bbox_description, bbox, time_description, time, s5p_band):
        """Assemble one parameter set; only the AOI, date and S5P product vary."""
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
            "collection": Parameter(
                "collection",
                description="Sentinel-3 OLCI L1B collection identifier (true-colour base map)",
                default="sentinel-3-olci-l1b",
            ),
            "bands": Parameter(
                "bands",
                description="OLCI true-colour bands: B04 (red), B06 (red edge), B08 (NIR)",
                default=olci_bands,
            ),
            "s5p_collection": Parameter(
                "s5p_collection",
                description="Sentinel-5P L2 collection identifier (canonical; CDSE-only)",
                default="sentinel-5p-l2",
            ),
            "s5p_bands": Parameter(
                "s5p_bands",
                description=(
                    "Single Sentinel-5P atmospheric product to overlay -- CDSE's "
                    "SENTINEL_5P_L2 collection only supports one band per request"
                ),
                default=[s5p_band],
            ),
        }

    parameter_sets = {
        # The original evalscript's own default product (CLOUD_TOP_PRESSURE), over
        # a scene with a partial cloud deck offshore and clear volcanic terrain on
        # Etna's flanks -- both branches of the fusion are visible in one frame.
        "etna_sicily_cloud_pressure": {
            "location_name": "Mt Etna, Sicily, Italy (cloud top pressure)",
            **_shared(
                "Spatial extent over Mt Etna and the adjoining Ionian coast",
                {"west": 14.6, "south": 37.6, "east": 15.3, "north": 38.1},
                "Window containing the 24 Jul 2023 daytime overpass",
                ["2023-07-24", "2023-07-25"],
                "cloud_top_pressure",
            ),
        },
        # Same bounding box and date as above -- a direct product swap at one
        # location, echoing the original's "replace all CLOUD_TOP_PRESSURE
        # mentions" comment block. Etna degasses SO2 continuously.
        "etna_sicily_so2": {
            "location_name": "Mt Etna, Sicily, Italy (SO2 degassing)",
            **_shared(
                "Spatial extent over Mt Etna and the adjoining Ionian coast",
                {"west": 14.6, "south": 37.6, "east": 15.3, "north": 38.1},
                "Window containing the 24 Jul 2023 daytime overpass",
                ["2023-07-24", "2023-07-25"],
                "so2",
            ),
        },
        # Po Valley, northern Italy -- one of Europe's most persistent NO2
        # hotspots (industry, traffic, valley inversions). Same date as the LST
        # notebook's Po Valley set.
        "po_valley_no2": {
            "location_name": "Po Valley, Italy (NO2)",
            **_shared(
                "Spatial extent over the central Po plain between Milan and Cremona",
                {"west": 8.8, "south": 44.8, "east": 10.2, "north": 45.6},
                "Window containing the 22 Aug 2023 daytime overpass",
                ["2023-08-22", "2023-08-23"],
                "no2",
            ),
        },
        # Chiquitania, Bolivia -- the same 2019 dry-forest fire complex used by
        # s2_s1_forest_fire_progression.params.py, during the height of Bolivia's
        # worst wildfire season on record. CO is a standard biomass-burning tracer.
        "chiquitania_co": {
            "location_name": "Chiquitania, Bolivia (wildfire CO)",
            **_shared(
                "Spatial extent over the Chiquitania dry-forest fire complex",
                {"west": -60.15, "south": -18.50, "east": -59.95, "north": -18.35},
                "Window containing the 12 Sep 2019 overpass",
                ["2019-09-11", "2019-09-13"],
                "co",
            ),
        },
    }

    return parameter_sets
