"""Parameter definitions for Cyanobacteria Chlorophyll-a (NDCI) Detection.

This file defines parameter sets that can be used with the NDCI algorithm
for detecting cyanobacteria chlorophyll-a concentrations in water bodies
using Sentinel-2 imagery.
"""

from openeo.api.process import Parameter


def get_parameters():
    """Return available parameter sets for the NDCI algorithm.

    Returns:
        Dictionary mapping parameter set names to parameter dictionaries.
        Each parameter set includes:
        - location_name: Human-readable location identifier
        - bounding_box: Spatial extent as Parameter object
        - time: Temporal range as Parameter object
        - bands: Required Sentinel-2 bands as Parameter object
        - collection: Data collection identifier as Parameter object
        - cloud_cover: Maximum cloud cover percentage as Parameter object
    """

    # Bands required for the NDCI algorithm:
    # B02 (Blue), B03 (Green), B04 (Red), B05 (Red Edge 1),
    # B07 (Red Edge 3), B08 (NIR), B8A (Narrow NIR),
    # B11 (SWIR 1), B12 (SWIR 2)
    ndci_bands = ["B02", "B03", "B04", "B05", "B07", "B08", "B8A", "B11", "B12"]

    parameter_sets = {
        "peniche_bay": {
            "location_name": "Peniche Bay, Portugal",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for Peniche Bay",
                default={"west": -9.42, "south": 39.30, "east": -9.32, "north": 39.38},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                default=["2025-12-01", "2026-03-01"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for NDCI calculation",
                default=ndci_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="SENTINEL2_L2A",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum cloud cover percentage",
                default=20,
            ),
        },
        "roper_river": {
            "location_name": "Roper River, Australia",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for Roper River",
                default={"west": 132.35, "south": -14.55, "east": 132.55, "north": -14.40},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                default=["2024-06-01", "2024-09-30"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for NDCI calculation",
                default=ndci_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="SENTINEL2_L2A",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum cloud cover percentage",
                default=20,
            ),
        },
        "lake_taihu": {
            "location_name": "Lake Taihu, China",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for Lake Taihu",
                default={"west": 119.90, "south": 30.90, "east": 120.60, "north": 31.55},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                default=["2023-07-01", "2023-09-30"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for NDCI calculation",
                default=ndci_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="SENTINEL2_L2A",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum cloud cover percentage",
                default=30,
            ),
        },
        "lake_erie": {
            "location_name": "Lake Erie, USA/Canada",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for western Lake Erie",
                default={"west": -83.50, "south": 41.50, "east": -82.60, "north": 41.95},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                default=["2023-07-15", "2023-09-15"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for NDCI calculation",
                default=ndci_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="SENTINEL2_L2A",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum cloud cover percentage",
                default=25,
            ),
        },
        "lake_pontchartrain": {
            "location_name": "Lake Pontchartrain, USA",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for Lake Pontchartrain",
                default={"west": -90.45, "south": 30.03, "east": -89.65, "north": 30.40},
            ),
            "time": Parameter(
                "time",
                description="Temporal range for data acquisition",
                default=["2023-06-01", "2023-08-31"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for NDCI calculation",
                default=ndci_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="SENTINEL2_L2A",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum cloud cover percentage",
                default=30,
            ),
        },
    }

    return parameter_sets
