"""Endpoint configuration management for OpenEO backends.

This module handles loading endpoint configurations and creating connections
to OpenEO backends based on YAML configuration files.
"""

import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional
import openeo


def load_endpoint_config(config_path: Optional[Path] = None) -> Dict[str, Any]:
    """Load endpoint configuration from YAML file.
    
    Args:
        config_path: Path to endpoints.yaml file. If None, uses default location.
        
    Returns:
        Dictionary containing endpoint configurations
        
    Raises:
        FileNotFoundError: If configuration file is not found
        yaml.YAMLError: If configuration file is invalid YAML
    """
    if config_path is None:
        config_path = Path(__file__).parent / "endpoints.yaml"
    
    if not config_path.exists():
        raise FileNotFoundError(f"Endpoint configuration not found: {config_path}")
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def get_available_endpoints(config_path: Optional[Path] = None) -> List[str]:
    """Get list of available endpoint names.
    
    Args:
        config_path: Path to endpoints.yaml file
        
    Returns:
        List of endpoint names
    """
    config = load_endpoint_config(config_path)
    return [
        name for name, endpoint in config["endpoints"].items()
        if endpoint.get("enabled", True)
    ]


def get_endpoint_info(endpoint_name: str, config_path: Optional[Path] = None) -> Dict[str, Any]:
    """Get configuration for a specific endpoint.
    
    Args:
        endpoint_name: Name of the endpoint
        config_path: Path to endpoints.yaml file
        
    Returns:
        Endpoint configuration dictionary
        
    Raises:
        KeyError: If endpoint name is not found
    """
    config = load_endpoint_config(config_path)
    
    if endpoint_name not in config["endpoints"]:
        available = list(config["endpoints"].keys())
        raise KeyError(f"Endpoint '{endpoint_name}' not found. Available: {available}")
    
    return config["endpoints"][endpoint_name]


def get_connection(endpoint_name: Optional[str] = None, config_path: Optional[Path] = None) -> openeo.Connection:
    """Create OpenEO connection to specified endpoint.
    
    Args:
        endpoint_name: Name of endpoint to connect to. If None, uses first available from priority list.
        config_path: Path to endpoints.yaml file
        
    Returns:
        Authenticated OpenEO connection
        
    Raises:
        ValueError: If no endpoints are available
        ConnectionError: If connection fails
    """
    config = load_endpoint_config(config_path)
    
    # Determine which endpoint to use
    if endpoint_name is None:
        # Use default priority
        available_endpoints = get_available_endpoints(config_path)
        priority_list = config.get("default_priority", [])
        
        for priority_endpoint in priority_list:
            if priority_endpoint in available_endpoints:
                endpoint_name = priority_endpoint
                break
        
        if endpoint_name is None:
            if available_endpoints:
                endpoint_name = available_endpoints[0]
            else:
                raise ValueError("No available endpoints found")
    
    endpoint_info = get_endpoint_info(endpoint_name, config_path)
    
    # Create connection
    try:
        connection = openeo.connect(endpoint_info["url"])
        
        # Authenticate based on auth method
        auth_method = endpoint_info.get("auth_method", "oidc")
        
        if auth_method == "oidc_authorization_code":
            connection = connection.authenticate_oidc_authorization_code()
        elif auth_method == "oidc":
            connection = connection.authenticate_oidc()
        elif auth_method == "basic":
            # For local development - no authentication needed
            pass
        else:
            raise ValueError(f"Unknown auth method: {auth_method}")
        
        return connection
        
    except Exception as e:
        raise ConnectionError(f"Failed to connect to {endpoint_name}: {e}")


def get_band_names(endpoint_name: str, bands: List[str], config_path: Optional[Path] = None) -> List[str]:
    """Convert band names to the format expected by the endpoint.
    
    Args:
        endpoint_name: Name of the endpoint
        bands: List of standard band names (e.g., ["B02", "B03", "B04"])
        config_path: Path to endpoints.yaml file
        
    Returns:
        List of band names formatted for the endpoint
    """
    endpoint_info = get_endpoint_info(endpoint_name, config_path)
    band_format = endpoint_info.get("band_format", "{band}")
    
    formatted_bands = []
    for band in bands:
        # Convert to lowercase for reflectance format
        band_lower = band.lower()
        formatted_band = band_format.format(band=band_lower)
        formatted_bands.append(formatted_band)
    
    return formatted_bands


def validate_endpoint_compatibility(endpoint_name: str, required_capabilities: List[str], 
                                  config_path: Optional[Path] = None) -> bool:
    """Check if endpoint supports required capabilities.
    
    Args:
        endpoint_name: Name of the endpoint
        required_capabilities: List of required OpenEO capabilities
        config_path: Path to endpoints.yaml file
        
    Returns:
        True if endpoint supports all required capabilities
    """
    try:
        endpoint_info = get_endpoint_info(endpoint_name, config_path)
        endpoint_capabilities = endpoint_info.get("capabilities", [])
        
        return all(cap in endpoint_capabilities for cap in required_capabilities)
        
    except KeyError:
        return False