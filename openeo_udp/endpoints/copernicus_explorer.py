"""Endpoint configuration for EOPF Explorer (Copernicus Explorer).

This module contains both connection configuration and parameter mapping logic
for the EOPF Explorer OpenEO backend.
"""

from typing import Any, Dict

from openeo.api.process import Parameter

# Endpoint configuration
ENDPOINT_CONFIG = {
    "name": "EOPF Explorer API",
    "url": "https://api.explorer.eopf.copernicus.eu/openeo",
    "auth_method": "oidc_authorization_code",
    "collection_id": "sentinel-2-l2a",
    "band_format": "reflectance|{band}",
    "description": "Primary endpoint for interactive development and exploration",
    "capabilities": [
        "load_collection",
        "apply_dimension",
        "save_result",
        "create_service",
    ],
    "cloud_cover_filter": True,
    "max_area_km2": 10000,
    "enabled": True,
}


def map_parameters(params: Dict[str, Any]) -> Dict[str, Any]:
    """Map parameters for EOPF Explorer endpoint.

    Transforms:
    - Collection IDs: SENTINEL2_L2A -> sentinel-2-l2a
    - Band names: B02 -> reflectance|B02

    Args:
        params: Original parameter dictionary

    Returns:
        Mapped parameter dictionary
    """
    mapped_params = params.copy()

    for param_name, param_value in params.items():
        if isinstance(param_value, Parameter):
            # Map collection parameter
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

            # Map bands parameter with reflectance prefix
            elif param_name == "bands" and isinstance(param_value.default, list):
                mapped_bands = [
                    f"reflectance|{band.lower()}" for band in param_value.default
                ]
                mapped_params[param_name] = Parameter(
                    param_value.name,
                    description=(
                        param_value.description
                        if hasattr(param_value, "description")
                        else param_value.name
                    ),
                    default=mapped_bands,
                )

    return mapped_params
