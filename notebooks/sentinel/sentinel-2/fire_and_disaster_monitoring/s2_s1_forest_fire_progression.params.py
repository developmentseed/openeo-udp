# License: CC-BY-SA-4.0
# Origin: Converted from Sentinel Hub evalscript
# Original evalscript: https://custom-scripts.sentinel-hub.com/custom-scripts/data-fusion/s2_s1_forest_fire_progression/
# Source: Sentinel Hub Custom Scripts (CC-BY-SA-4.0)
# Conversion: Development Seed (openEO-UDP project)
"""Parameter definitions for the S2/S1 Forest Fire Progression algorithm.

This is a **multi-sensor, multi-temporal data-fusion** algorithm. It combines:

- Sentinel-2 optical bands from a first date (t1) to map vegetation / burned area
  via spectral indices, and
- Sentinel-1 SAR backscatter from t1 and a second date (t2) to track how the fire
  progressed under cloud cover (SAR sees through clouds).

The companion notebook therefore needs three acquisitions: S2 at t1, S1 at t1 and
S1 at t2. Because the algorithm fuses two collections, the **S2** collection/bands
flow through the standard ParameterManager mapping (so ``reflectance_scale`` and
the dimension names are injected), while the **S1** collection/bands are kept as
separate keys and mapped via the endpoint mapper in the notebook (the standard
mapping only auto-maps the single ``collection``/``bands`` pair).

The default parameter sets reproduce the original example: the September 2019 fires
that ravaged the Chiquitano dry forest on the Bolivia/Paraguay border, using
Sentinel data from 7 September (t1) and 12 September (t2) 2019.

NOTE: This UDP targets the Copernicus Data Space Ecosystem (CDSE), the backend
that serves both Sentinel-1 GRD and Sentinel-2 L2A.
"""

from openeo.api.process import Parameter


def get_parameters():
    """Return available parameter sets for the forest fire progression algorithm.

    Returns:
        Dictionary mapping parameter set names to parameter dictionaries.
        Each parameter set includes:
        - location_name: Human-readable location identifier
        - bounding_box: Spatial extent as Parameter object (runtime)
        - time_t1: Window bracketing the first acquisition (pre/early fire)
        - time_t2: Window bracketing the second acquisition (later fire stage)
        - bands: Sentinel-2 bands for the optical indices (mapped to native names)
        - collection: Sentinel-2 collection id (mapped to native id)
        - cloud_cover: Maximum scene-level cloud cover for the S2 (t1) image
        - s1_collection: Sentinel-1 GRD collection id (canonical, mapped per endpoint)
        - s1_bands_t1: Sentinel-1 polarizations needed at t1 (VH)
        - s1_bands_t2: Sentinel-1 polarizations needed at t2 (VV, VH)
    """

    # Sentinel-2 bands for the optical part (canonical lowercase, mapped per
    # endpoint): B03 (Green), B04 (Red), B08 (NIR), B11 (SWIR1), B12 (SWIR2).
    s2_bands = ["b03", "b04", "b08", "b11", "b12"]

    parameter_sets = {
        # Bolivian Chiquitania (Roboré / San José de Chiquitos area), the heart of
        # the 2019 Chiquitano dry-forest fires.
        "chiquitania_bolivia_2019": {
            "location_name": "Chiquitania, Bolivia (2019 fires)",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent over the Bolivian Chiquitania fire region",
                default={
                    "west": -60.15,
                    "south": -18.50,
                    "east": -59.95,
                    "north": -18.35,
                },
            ),
            "time_t1": Parameter(
                "time_t1",
                description="Window bracketing the first acquisition (7 Sep 2019)",
                default=["2019-09-06", "2019-09-08"],
            ),
            "time_t2": Parameter(
                "time_t2",
                description="Window bracketing the second acquisition (12 Sep 2019)",
                default=["2019-09-11", "2019-09-13"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for the optical indices",
                default=s2_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Sentinel-2 data collection identifier",
                default="sentinel-2-l2a",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum scene-level cloud cover for the S2 (t1) image",
                default=50,
            ),
            "s1_collection": Parameter(
                "s1_collection",
                description="Sentinel-1 GRD collection identifier (canonical; mapped per endpoint)",
                default="sentinel-1-grd",
            ),
            "s1_bands_t1": Parameter(
                "s1_bands_t1",
                description="Sentinel-1 polarizations needed at t1",
                default=["vh"],
            ),
            "s1_bands_t2": Parameter(
                "s1_bands_t2",
                description="Sentinel-1 polarizations needed at t2",
                default=["vv", "vh"],
            ),
        },
        # Paraguayan Chaco side of the same trans-border 2019 fire complex.
        "chaco_paraguay_border_2019": {
            "location_name": "Chaco, Paraguay/Bolivia border (2019 fires)",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent over the Paraguayan Chaco fire region",
                default={
                    "west": -60.30,
                    "south": -19.60,
                    "east": -60.10,
                    "north": -19.45,
                },
            ),
            "time_t1": Parameter(
                "time_t1",
                description="Window bracketing the first acquisition (7 Sep 2019)",
                default=["2019-09-06", "2019-09-08"],
            ),
            "time_t2": Parameter(
                "time_t2",
                description="Window bracketing the second acquisition (12 Sep 2019)",
                default=["2019-09-11", "2019-09-13"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for the optical indices",
                default=s2_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Sentinel-2 data collection identifier",
                default="sentinel-2-l2a",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum scene-level cloud cover for the S2 (t1) image",
                default=50,
            ),
            "s1_collection": Parameter(
                "s1_collection",
                description="Sentinel-1 GRD collection identifier (canonical; mapped per endpoint)",
                default="sentinel-1-grd",
            ),
            "s1_bands_t1": Parameter(
                "s1_bands_t1",
                description="Sentinel-1 polarizations needed at t1",
                default=["vh"],
            ),
            "s1_bands_t2": Parameter(
                "s1_bands_t2",
                description="Sentinel-1 polarizations needed at t2",
                default=["vv", "vh"],
            ),
        },
        # Corbières massif, Aude, France — the August 2025 fire. It started on
        # 5 Aug 2025 ~16:15 on the D212 between Lagrasse and Ribaute (origin
        # 43.061 N, 2.758 E), spread south-east under 70 km/h Tramontane winds,
        # reached ~16,000 ha within 24 h and ~17,000 ha by 7 Aug, was "fixé" on
        # 8 Aug and "maîtrisé" on 10 Aug (final burn 11,133 ha across 16 communes).
        # t1 is a PRE-fire baseline (29 Jul–4 Aug, before the 5 Aug start) and t2 is
        # post-fire (8–15 Aug, once fully burned), so the SAR VH drop cleanly marks
        # the scar — a textbook case for the "newly burned" (red) class.
        "aude_corbieres_france_2025": {
            "location_name": "Corbières, Aude, France (2025 fire)",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent over the Corbières burn scar (Lagrasse/Ribaute origin SE to Durban-Corbières), Aude, France",
                default={
                    "west": 2.58,
                    "south": 42.94,
                    "east": 2.95,
                    "north": 43.14,
                },
            ),
            "time_t1": Parameter(
                "time_t1",
                description="Pre-fire baseline window (before the 5 Aug 2025 start)",
                default=["2025-07-29", "2025-08-04"],
            ),
            "time_t2": Parameter(
                "time_t2",
                description="Post-fire window (8-15 Aug 2025, once fully burned)",
                default=["2025-08-08", "2025-08-15"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for the optical indices",
                default=s2_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Sentinel-2 data collection identifier",
                default="sentinel-2-l2a",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum scene-level cloud cover for the S2 (t1) image",
                default=40,
            ),
            "s1_collection": Parameter(
                "s1_collection",
                description="Sentinel-1 GRD collection identifier (canonical; mapped per endpoint)",
                default="sentinel-1-grd",
            ),
            "s1_bands_t1": Parameter(
                "s1_bands_t1",
                description="Sentinel-1 polarizations needed at t1",
                default=["vh"],
            ),
            "s1_bands_t2": Parameter(
                "s1_bands_t2",
                description="Sentinel-1 polarizations needed at t2",
                default=["vv", "vh"],
            ),
        },
    }

    return parameter_sets
