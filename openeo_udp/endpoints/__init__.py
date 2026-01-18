"""Endpoints package for OpenEO UDP.

This package provides endpoint configurations and parameter mapping functionality
using pure Python modules for maximum flexibility.
"""

import importlib
from pathlib import Path
from typing import Any, Dict, List

__version__ = "0.1.0"


def list_available_endpoints() -> List[str]:
    """List all available endpoint configurations.

    Returns:
        List of endpoint names
    """
    endpoints_dir = Path(__file__).parent
    endpoint_files = [
        f.stem for f in endpoints_dir.glob("*.py") if f.stem != "__init__"
    ]
    return endpoint_files


def get_endpoint_config(endpoint_name: str) -> Dict[str, Any]:
    """Get configuration for a specific endpoint.

    Args:
        endpoint_name: Name of the endpoint

    Returns:
        Endpoint configuration dictionary

    Raises:
        ImportError: If endpoint configuration is not found
    """
    try:
        module = importlib.import_module(f"openeo_udp.endpoints.{endpoint_name}")
        return module.ENDPOINT_CONFIG
    except ImportError as e:
        raise ImportError(f"Endpoint configuration '{endpoint_name}' not found") from e


def get_endpoint_mapper(endpoint_name: str):
    """Get parameter mapper function for a specific endpoint.

    Args:
        endpoint_name: Name of the endpoint

    Returns:
        Mapper function or None if not found
    """
    try:
        module = importlib.import_module(f"openeo_udp.endpoints.{endpoint_name}")
        return getattr(module, "map_parameters", None)
    except ImportError:
        return None


def get_endpoint_connection(endpoint_name: str):
    """Get connection function for specific endpoint.

    Args:
        endpoint_name: Name of the endpoint

    Returns:
        Connection object from endpoint-specific get_connection function

    Raises:
        ImportError: If endpoint module or get_connection function not found
    """
    try:
        module = importlib.import_module(f"openeo_udp.endpoints.{endpoint_name}")
        if not hasattr(module, "get_connection"):
            raise ImportError(
                f"Endpoint '{endpoint_name}' does not have a get_connection function"
            )
        return module.get_connection()
    except ImportError as e:
        raise ImportError(
            f"Failed to get connection for endpoint '{endpoint_name}': {e}"
        ) from e


def get_all_endpoints() -> Dict[str, Dict[str, Any]]:
    """Get all endpoint configurations.

    Returns:
        Dictionary mapping endpoint names to their configurations
    """
    endpoints = {}
    for endpoint_name in list_available_endpoints():
        try:
            endpoints[endpoint_name] = get_endpoint_config(endpoint_name)
        except ImportError:
            continue
    return endpoints
