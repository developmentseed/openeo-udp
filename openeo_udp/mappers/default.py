"""
Default parameter mapper for endpoints without specific mapping requirements.

This mapper applies minimal transformations based on endpoint configuration.
"""

from openeo.api.process import Parameter
from typing import Any, Dict


def map_parameters(params: Dict[str, Any], endpoint_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Default parameter mapping based on endpoint configuration.
    
    Args:
        params: Original parameter dictionary
        endpoint_config: Endpoint configuration from endpoints.yaml
        
    Returns:
        Mapped parameter dictionary
    """
    mapped_params = params.copy()
    
    for param_name, param_value in params.items():
        if isinstance(param_value, Parameter):
            # Map collection parameter using endpoint config
            if param_name == 'collection' and 'collection_id' in endpoint_config:
                mapped_params[param_name] = Parameter(
                    param_value.name,
                    description=param_value.description if hasattr(param_value, 'description') else param_value.name,
                    default=endpoint_config['collection_id']
                )
            
            # Map bands parameter using endpoint band format
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