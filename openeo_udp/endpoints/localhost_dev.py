"""Endpoint configuration for Development Seed OpenEO Backend.

This module contains both connection configuration and parameter mapping logic
for the Development Seed OpenEO backend.
"""

from typing import Any, Dict

import openeo
from openeo.api.process import Parameter

# Endpoint configuration
ENDPOINT_CONFIG = {
    "name": "Localhost Development TiTiler OpenEO Backend",
    "url": "http://localhost:8081/",
    "auth_method": "oidc",
    "collection_id": "sentinel-2-l2a",
    "band_format": "{band}",
    "description": "Development and testing endpoint",
    "capabilities": ["load_collection", "apply_dimension", "save_result"],
    "cloud_cover_filter": True,
    "max_area_km2": 5000,
    "enabled": True,
}

# Sentinel-2 band resolution mapping
BAND_RESOLUTIONS = {
    "B01": 60,
    "B02": 10,
    "B03": 10,
    "B04": 10,
    "B05": 20,
    "B06": 20,
    "B07": 20,
    "B08": 10,
    "B8A": 20,
    "B09": 60,
    "B10": 60,
    "B11": 20,
    "B12": 20,
}


def map_parameters(params: Dict[str, Any]) -> Dict[str, Any]:
    """Map parameters for Development Seed endpoint.

    Transforms:
    - Collection IDs: SENTINEL2_L2A -> sentinel-2-l2a
    - Band names: For sentinel-2-l2a collections, appends resolution suffix (B04 -> B04_10m)

    Args:
        params: Original parameter dictionary

    Returns:
        Mapped parameter dictionary
    """
    mapped_params = params.copy()

    # Track the collection to determine if we need to add resolution suffixes
    collection_id = ENDPOINT_CONFIG["collection_id"]

    for param_name, param_value in params.items():
        if isinstance(param_value, Parameter):
            # Map collection parameter to DS format
            if param_name == "collection":
                mapped_params[param_name] = Parameter(
                    param_value.name,
                    description=(
                        param_value.description
                        if hasattr(param_value, "description")
                        else param_value.name
                    ),
                    default=collection_id,
                )

            # Transform band names for sentinel-2-l2a collections
            elif param_name == "bands" and isinstance(param_value.default, list):
                # Add resolution suffix if collection starts with "sentinel-2-l2"
                if collection_id.startswith("sentinel-2-l2"):
                    mapped_bands = []
                    for band in param_value.default:
                        # Extract base band name (handle case variations)
                        band_upper = band.upper()
                        if band_upper in BAND_RESOLUTIONS:
                            resolution = BAND_RESOLUTIONS[band_upper]
                            mapped_bands.append(f"{band}_{resolution}m")
                        else:
                            # Keep original if not in mapping
                            mapped_bands.append(band)

                    mapped_params[param_name] = Parameter(
                        param_value.name,
                        description=(
                            param_value.description
                            if hasattr(param_value, "description")
                            else param_value.name
                        ),
                        default=mapped_bands,
                    )
                else:
                    # No transformation for non-sentinel-2-l2 collections
                    mapped_params[param_name] = Parameter(
                        param_value.name,
                        description=(
                            param_value.description
                            if hasattr(param_value, "description")
                            else param_value.name
                        ),
                        default=param_value.default,
                    )

    return mapped_params


def get_connection():
    """Create connection to Development Seed OpenEO Backend.

    Returns:
        Authenticated OpenEO connection
    """
    connection = openeo.connect(ENDPOINT_CONFIG["url"])

    # Development Seed backend uses OIDC authentication
    connection.authenticate_oidc_authorization_code()

    return connection
