"""Endpoint configuration for Copernicus Data Space.

This module contains both connection configuration and parameter mapping logic
for the Copernicus Data Space OpenEO backend.
"""

from typing import Any, Dict

import openeo
from openeo.api.process import Parameter

# Endpoint configuration
ENDPOINT_CONFIG = {
    "name": "Copernicus Data Space - Production API",
    "url": "https://openeo.dataspace.copernicus.eu/",
    "auth_method": "oidc",
    "collection_id": "SENTINEL2_L2A",
    "band_format": "{band}",
    "description": "Production endpoint for larger scale processing",
    "capabilities": [
        "load_collection",
        "apply_dimension",
        "save_result",
        "batch_processing",
    ],
    "cloud_cover_filter": True,
    "max_area_km2": 50000,
    "enabled": True,
}


def map_parameters(params: Dict[str, Any]) -> Dict[str, Any]:
    """Map parameters for Copernicus Data Space endpoint.

    Transforms:
    - Collection IDs: Uses SENTINEL2_L2A (original format)
    - Band names: Keep original band names (B02, B03, etc.)

    Args:
        params: Original parameter dictionary

    Returns:
        Mapped parameter dictionary
    """
    mapped_params = params.copy()

    for param_name, param_value in params.items():
        if isinstance(param_value, Parameter):
            # Map collection parameter to CDSE format
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

            # Keep original band names for CDSE
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
    """Create connection to Copernicus Data Space endpoint.

    Returns:
        Authenticated OpenEO connection
    """
    connection = openeo.connect(ENDPOINT_CONFIG["url"])

    # Copernicus Data Space uses OIDC authentication
    connection.authenticate_oidc()

    return connection
