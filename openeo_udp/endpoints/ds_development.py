"""Endpoint configuration for Development Seed OpenEO Backend.

This module contains both connection configuration and parameter mapping logic
for the Development Seed OpenEO backend.
"""

from typing import Any, Dict

import openeo
from openeo.api.process import Parameter

# Endpoint configuration
ENDPOINT_CONFIG = {
    "name": "Development Seed OpenEO Backend",
    "url": "https://openeo.ds.io/",
    "auth_method": "oidc",
    "collection_id": "sentinel-2-l2a",
    "band_format": "{band}",
    "description": "Development and testing endpoint",
    "capabilities": ["load_collection", "apply_dimension", "save_result"],
    "cloud_cover_filter": True,
    "max_area_km2": 5000,
    "enabled": True,
}


def map_parameters(params: Dict[str, Any]) -> Dict[str, Any]:
    """Map parameters for Development Seed endpoint.

    Transforms:
    - Collection IDs: SENTINEL2_L2A -> sentinel-2-l2a
    - Band names: Keep original band names (B02, B03, etc.)

    Args:
        params: Original parameter dictionary

    Returns:
        Mapped parameter dictionary
    """
    mapped_params = params.copy()

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
                    default=ENDPOINT_CONFIG["collection_id"],
                )

            # Keep original band names for DS
            elif param_name == "bands" and isinstance(param_value.default, list):
                mapped_params[param_name] = Parameter(
                    param_value.name,
                    description=(
                        param_value.description
                        if hasattr(param_value, "description")
                        else param_value.name
                    ),
                    default=param_value.default,  # No transformation needed
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
