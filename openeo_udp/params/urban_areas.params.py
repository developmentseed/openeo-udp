# License: CC-BY-SA-4.0
# Origin: Converted from Sentinel Hub evalscript
# Original evalscript: https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-1/urban_areas/
# Source: Sentinel Hub Custom Scripts (CC-BY-SA-4.0)
# Conversion: Development Seed (openEO-UDP project)
"""Parameter definitions for the Urban Areas visualization algorithm.

This file defines parameter sets for detecting and visualizing urban areas
using Sentinel-1 GRD VH and VV backscatter.  VV maps to the green channel,
VH to the blue channel, and strongly reflecting VH values (VH × 5.5 > 0.5)
are added to the red channel so that different building materials appear in
distinctive colors.

Note: Sentinel-1 GRD backscatter is already in linear float units (0–1 range).
The ``reflectance_scale`` injected by the endpoint mapper is not used in this
algorithm.
"""

from openeo.api.process import Parameter


def get_parameters():
    """Return available parameter sets for the urban areas algorithm.

    Returns:
        Dictionary mapping parameter set names to parameter dictionaries.
        Each parameter set includes:
        - location_name: Human-readable location identifier
        - bounding_box: Spatial extent as Parameter object (runtime)
        - time: Temporal range as Parameter object (runtime)
        - bands: Required Sentinel-1 polarizations as Parameter object
        - collection: Data collection identifier as Parameter object
    """

    urban_bands = ["vh", "vv"]

    parameter_sets = {
        "bologna_italy": {
            "location_name": "Bologna, Italy",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for Bologna, Italy",
                default={"west": 11.20, "south": 44.45, "east": 11.48, "north": 44.56},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                default=["2019-05-26", "2019-06-01"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-1 GRD polarization bands",
                default=urban_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Sentinel-1 GRD collection identifier",
                default="sentinel-1-grd",
            ),
        },
        "paris_france": {
            "location_name": "Paris, France",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for central Paris, France",
                default={"west": 2.20, "south": 48.75, "east": 2.55, "north": 48.95},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                default=["2024-09-01", "2024-09-12"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-1 GRD polarization bands",
                default=urban_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Sentinel-1 GRD collection identifier",
                default="sentinel-1-grd",
            ),
        },
        "dubai_uae": {
            "location_name": "Dubai, UAE",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for Dubai, UAE",
                default={"west": 55.15, "south": 25.05, "east": 55.45, "north": 25.30},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                default=["2024-10-01", "2024-10-12"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-1 GRD polarization bands",
                default=urban_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Sentinel-1 GRD collection identifier",
                default="sentinel-1-grd",
            ),
        },
    }

    return parameter_sets
