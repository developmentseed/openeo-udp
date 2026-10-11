# License: MIT
# Origin: Original implementation (Development Seed, openEO-UDP project),
#   inspired by the CNES/CESBIO Let-it-snow (LIS) algorithm.
# Scientific source: Gascoin et al. (2019), ESSD 11, 493-514,
#   https://doi.org/10.5194/essd-11-493-2019
# LIS code (Apache-2.0): https://gitlab.orfeo-toolbox.org/remote_modules/let-it-snow
"""Parameter definitions for the LIS-like snow cover workshop notebook.

Each parameter set describes one small Pyrenees area (about 15 x 20 km, one
Sentinel-2 MGRS tile) with a winter-to-spring season for the synchronous steps
and a hydrological year for the snow-cover-duration step.

The LIS thresholds are the defaults of Gascoin et al. (2019), Table 1, p. 499,
which are also the defaults in ``doc/lis_default_configuration.json`` of the
LIS repository. NDSI thresholds are unitless; red thresholds are 0-1 surface
reflectance (LIS stores them as reflectance x 1000).

Note:
    Collections and bands are canonical ids (``sentinel-2-l2a``, ``b03``,
    ``cop-dem-glo-30``, ``dem``). The endpoint mapper rewrites the main
    ``collection``/``bands`` pair. The notebook maps the second (DEM) pair
    itself with ``ParameterManager.apply_endpoint_mapping``.
"""

import json
from pathlib import Path

from openeo.api.process import Parameter

_HERE = Path(__file__).parent


def _watersheds(name):
    """Load the simplified BD TOPAGE watershed outlines stored next to this file.

    Source: BD TOPAGE (IGN/OFB), "Bassins versants topographiques", served by
    the Sandre WFS https://services.sandre.eaufrance.fr/geo/topage (layer
    ``sa:BassinVersantTopographique_FXX``), Licence Ouverte Etalab 2.0.
    Geometries simplified with a 0.0005 degree tolerance.
    """
    with open(_HERE / f"lis_snow_cover_watersheds_{name}.geojson") as f:
        return json.load(f)


def _common(location, bbox, watersheds, snowline_dates, snowline_elevation):
    """Build one parameter set. Only the location-specific values change."""
    return {
        "location_name": location,
        "bounding_box": Parameter(
            "bounding_box",
            description=f"Spatial extent ({location})",
            schema={"type": "object", "subtype": "bounding-box"},
            default=bbox,
        ),
        "time": Parameter(
            "time",
            description=(
                "Temporal range of the Sentinel-2 acquisitions. The snow cover "
                "fraction is computed over this range."
            ),
            schema={"type": "array", "subtype": "temporal-interval"},
            default=["2023-01-01", "2023-05-31"],
        ),
        "hydrological_year": Parameter(
            "hydrological_year",
            description=(
                "Hydrological year (1 September to 31 August) for the "
                "snow-cover-duration synthesis (end date excluded)."
            ),
            schema={"type": "array", "subtype": "temporal-interval"},
            default=["2022-09-01", "2023-09-01"],
        ),
        "collection": Parameter(
            "collection",
            description="Sentinel-2 L2A surface reflectance collection",
            default="sentinel-2-l2a",
        ),
        "bands": Parameter(
            "bands",
            description=(
                "Bands used by LIS: green (b03), red (b04), SWIR (b11) and the "
                "Sen2Cor scene classification (scl). Order matters: the "
                "callbacks index the bands in this order."
            ),
            default=["b03", "b04", "b11", "scl"],
        ),
        "cloud_cover": Parameter(
            "cloud_cover",
            description=(
                "Maximum scene-level cloud cover (%). Clouds are also masked "
                "per pixel with SCL, so this only skips the worst scenes."
            ),
            schema={"type": "number", "minimum": 0, "maximum": 100},
            default=50,
        ),
        "target_resolution": Parameter(
            "target_resolution",
            description="Working resolution in metres (LIS works at 20 m, the B11 grid)",
            schema={"type": "number"},
            default=20,
        ),
        # LIS pass 1 (Gascoin et al. 2019, Table 1 and Eq. 2).
        "ndsi_pass1": Parameter(
            "ndsi_pass1",
            description="LIS pass 1 NDSI threshold n1: snow if NDSI > n1 and red > r1",
            schema={"type": "number", "minimum": -1, "maximum": 1},
            default=0.4,
        ),
        "red_pass1": Parameter(
            "red_pass1",
            description="LIS pass 1 red reflectance threshold r1 (0-1 reflectance)",
            schema={"type": "number", "minimum": 0, "maximum": 1},
            default=0.2,
        ),
        # LIS pass 2, applied only above the snowline elevation zs.
        "ndsi_pass2": Parameter(
            "ndsi_pass2",
            description="LIS pass 2 NDSI threshold n2, applied above the snowline elevation",
            schema={"type": "number", "minimum": -1, "maximum": 1},
            default=0.15,
        ),
        "red_pass2": Parameter(
            "red_pass2",
            description="LIS pass 2 red reflectance threshold r2 (0-1 reflectance)",
            schema={"type": "number", "minimum": 0, "maximum": 1},
            default=0.04,
        ),
        "snowline_elevation": Parameter(
            "snowline_elevation",
            description=(
                "Snowline elevation zs in metres. Pass 2 (n2, r2) applies only "
                "to pixels above zs. LIS computes zs per image; this "
                "simplified version takes one value per run. Set it above the "
                "highest summit (for example 9000) to switch pass 2 off."
            ),
            schema={"type": "number"},
            default=snowline_elevation,
        ),
        # Step 4: the DEM, a second collection mapped by the notebook.
        "dem_collection": Parameter(
            "dem_collection",
            description="Digital elevation model collection (canonical id)",
            default="cop-dem-glo-30",
        ),
        "dem_bands": Parameter(
            "dem_bands",
            description="Elevation band of the DEM collection (canonical id)",
            default=["dem"],
        ),
        "snowline_dates": Parameter(
            "snowline_dates",
            description=(
                "Clear-sky acquisition dates used in step 4 to plot the snow "
                "fraction against elevation (one synchronous request per date)"
            ),
            default=snowline_dates,
        ),
        # Step 6: watershed polygons for aggregate_spatial.
        "watersheds": Parameter(
            "watersheds",
            description="Watershed polygons (GeoJSON FeatureCollection), BD TOPAGE",
            schema={"type": "object", "subtype": "geojson"},
            default=watersheds,
        ),
    }


def get_parameters():
    """Return the available parameter sets for the LIS snow cover notebook.

    Returns:
        Dictionary mapping parameter set names to parameter dictionaries.
    """
    return {
        # Néouvielle massif, Hautes-Pyrénées (MGRS tile 30TYN).
        "neouvielle_pyrenees_france": _common(
            location="Néouvielle massif, Hautes-Pyrénées, France",
            bbox={"west": 0.05, "south": 42.78, "east": 0.30, "north": 42.92},
            watersheds=_watersheds("neouvielle"),
            # Clear dates of relative orbit 51, which covers the whole area.
            snowline_dates=["2023-01-20", "2023-03-06", "2023-04-10"],
            # Median of the LIS snowlines of the three dates (890, 1090, 1690 m).
            snowline_elevation=1100,
        ),
        # Canigou massif, Pyrénées-Orientales (MGRS tile 31TDH).
        "canigou_pyrenees_france": _common(
            location="Canigou massif, Pyrénées-Orientales, France",
            bbox={"west": 2.38, "south": 42.47, "east": 2.55, "north": 42.57},
            watersheds=_watersheds("canigou"),
            # Clear dates (tile cloud cover < 15 %) of relative orbit 8, which
            # covers the whole area. Orbit 51 covers only part of the tile.
            snowline_dates=["2023-02-11", "2023-03-28", "2023-04-17"],
            # Median of the LIS snowlines of the three dates (526, 1926, 2226 m).
            snowline_elevation=1900,
        ),
    }
