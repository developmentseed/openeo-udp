"""Endpoints package for OpenEO UDP.

This package provides endpoint configurations and parameter mapping functionality
using pure Python modules for maximum flexibility.
"""

from typing import Dict, Any, List
import importlib
from pathlib import Path

__version__ = "0.1.0"


def list_available_endpoints() -> List[str]:
    """List all available endpoint configurations.
    
    Returns:
        List of endpoint names
    """
    endpoints_dir = Path(__file__).parent
    endpoint_files = [f.stem for f in endpoints_dir.glob("*.py") 
                     if f.stem != "__init__"]
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
    except ImportError:
        raise ImportError(f"Endpoint configuration '{endpoint_name}' not found")


def get_endpoint_mapper(endpoint_name: str):
    """Get parameter mapper function for a specific endpoint.
    
    Args:
        endpoint_name: Name of the endpoint
        
    Returns:
        Mapper function or None if not found
    """
    try:
        module = importlib.import_module(f"openeo_udp.endpoints.{endpoint_name}")
        return getattr(module, 'map_parameters', None)
    except ImportError:
        return None


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