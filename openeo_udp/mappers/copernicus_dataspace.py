"""
Parameter mapper for Copernicus Data Space endpoint.

This mapper transforms parameter values to match the Copernicus Data Space backend requirements:
- Collection IDs: Keep SENTINEL2_L2A as is
- Band names: Keep original band names (B02, B03, etc.)
"""

from openeo.api.process import Parameter
from typing import Any, Dict


def map_parameters(params: Dict[str, Any], endpoint_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map parameters for Copernicus Data Space endpoint.
    
    Args:
        params: Original parameter dictionary
        endpoint_config: Endpoint configuration from endpoints.yaml
        
    Returns:
        Mapped parameter dictionary
    """
    mapped_params = params.copy()
    
    for param_name, param_value in params.items():
        if isinstance(param_value, Parameter):
            # Map collection parameter
            if param_name == 'collection':
                mapped_params[param_name] = Parameter(
                    param_value.name,
                    description=param_value.description if hasattr(param_value, 'description') else param_value.name,
                    default=endpoint_config.get('collection_id', param_value.default)
                )
            
            # Map bands parameter - no transformation needed for CDSE
            elif param_name == 'bands' and isinstance(param_value.default, list):
                band_format = endpoint_config.get('band_format', '{band}')
                if '{band}' in band_format:
                    mapped_bands = [
                        band_format.format(band=band) 
                        for band in param_value.default
                    ]
                else:
                    mapped_bands = param_value.default
                    
                mapped_params[param_name] = Parameter(
                    param_value.name,
                    description=param_value.description if hasattr(param_value, 'description') else param_value.name,
                    default=mapped_bands
                )
                
    return mapped_params