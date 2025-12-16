"""
Configuration and utilities for OpenEO pre-processing
"""

BACKENDS = {
    "CDSE": {
        "url": "https://openeo.dataspace.copernicus.eu/",
        "auth_method": "oidc", # authenticate_oidc()
        "requires_scaling": True,
        "scale_factor": 10000.0,
        "band_scale_factors": {
            "B04": 10000.0,
            "B06": 10000.0,
            "B07": 10000.0,
            "B8A": 10000.0,
            "B12": 10000.0
        }
    },
    "EOPF": {
        "url": "https://api.explorer.eopf.copernicus.eu/openeo",
        "auth_method": "oidc_authorization_code", # authenticate_oidc_authorization_code()
        "requires_scaling": False,
        "scale_factor": 1.0,
        "band_scale_factors": {}
    }
}


def get_backend_config(backend_name="CDSE"):
    """
    Get configuration for specified backend
    
    Args:
        backend_name: Name of the backend (CDSE, EOPF, etc.)
    
    Returns:
        dict: Backend configuration
    """
    return BACKENDS.get(backend_name, BACKENDS["CDSE"])


def connect_to_backend(backend_name="CDSE"):
    """
    Connect and authenticate to a backend
    
    Args:
        backend_name: Name of the backend (CDSE, EOPF, etc.)
    
    Returns:
        conn: Connection to the backend
    """
    import openeo

    if backend_name is None:
        raise ValueError("Backend provider is required. Updates .env file with the backend provider.")

    config = get_backend_config(backend_name)
    
    connection = openeo.connect(url=config["url"])

    auth_method = config["auth_method"]

    try:
        if auth_method == "oidc":
            connection = connection.authenticate_oidc()
        elif auth_method == "oidc_authorization_code":
            connection = connection.authenticate_oidc_authorization_code()
    except Exception as e:
        raise ValueError(f"Authentication method {auth_method} not supported.")
    
    print(f"✓ Connected to {backend_name} backend at {config["url"]}")
    print(f"✓ Authenticated using {auth_method}")

    return connection

def scale_band(band_data, backend="CDSE", band_name=None):
    """
    Scale band data based on backend configuration
    
    Args:
        band_data: Band data to scale
        backend: Backend name (CDSE, EOPF, etc.)
        band_name: Optional specific band name for custom scaling
    """
    config = get_backend_config(backend)
    
    if not config["requires_scaling"]:
        return band_data
    
    if band_name and band_name in config["band_scale_factors"]:
        scale_factor = config["band_scale_factors"][band_name]
    else:
        scale_factor = config["scale_factor"]
    
    return band_data / scale_factor

def scale_bands(bands_dict, backend="CDSE"):
    """
    Scale multiple bands at once

    Args:
        bands_dict: Dictionary of band_name: band_data
        backend: Backend name (CDSE, EOPF, etc.)

    Returns:
        dict: Scaled bands
    """
    config = get_backend_config(backend)
    
    if not config["requires_scaling"]:
        return bands_dict
    
    scaled = {}
    for band_name, band_data in bands_dict.items():
        scaled[band_name] = scale_band(band_data, backend, band_name)
    
    return scaled
