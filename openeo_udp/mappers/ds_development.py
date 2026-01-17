"""
Parameter mapper for Development Seed OpenEO Backend.

This mapper transforms parameter values to match the DS backend requirements:
- Collection IDs: SENTINEL2_L2A -> sentinel-2-l2a
- Band names: Keep original band names (B02, B03, etc.)
"""

from openeo.api.process import Parameter
from typing import Any, Dict


def map_parameters(params: Dict[str, Any], endpoint_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map parameters for Development Seed endpoint.
    
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
            if param_name == 'collection' and param_value.default == 'SENTINEL2_L2A':
                mapped_params[param_name] = Parameter(
                    param_value.name,
                    description=param_value.description if hasattr(param_value, 'description') else param_value.name,
                    default=endpoint_config.get('collection_id', 'sentinel-2-l2a')
                )
            
            # Map bands parameter - no transformation needed for DS
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