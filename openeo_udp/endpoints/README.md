# Python-Only Endpoint Configuration

This directory contains endpoint configurations using pure Python modules for maximum flexibility and developer-friendliness.

## Structure

Each endpoint is configured in a separate Python file:
- `copernicus_explorer.py` - EOPF Explorer API configuration
- `copernicus_dataspace.py` - Copernicus Data Space configuration  
- `ds_development.py` - Development Seed OpenEO Backend configuration

## Adding New Endpoints

To add a new endpoint, create a new Python file with:

```python
"""Endpoint configuration for Your Backend."""

from openeo.api.process import Parameter
from typing import Any, Dict

# Endpoint configuration
ENDPOINT_CONFIG = {
    "name": "Your Backend Name",
    "url": "https://your-backend-url/",
    "auth_method": "oidc",  # or "basic", "oidc_authorization_code"
    "collection_id": "your-collection-id",
    "band_format": "{band}",  # or "prefix|{band}"
    "description": "Your backend description",
    "capabilities": ["load_collection", "apply_dimension", "save_result"],
    "cloud_cover_filter": True,
    "max_area_km2": 10000,
    "enabled": True
}

def map_parameters(params: Dict[str, Any]) -> Dict[str, Any]:
    \"\"\"Map parameters for your endpoint.\"\"\"
    # Add your custom mapping logic here
    return params
```

## Advantages of Python-Only Configuration

- **🐍 Developer-Friendly**: Native Python syntax and capabilities
- **🔧 Flexible Mapping**: Full programming power for parameter transformations
- **📦 Self-Contained**: No external dependencies or file formats
- **🚀 Dynamic**: Runtime parameter calculation and conditional logic
- **🧪 Testable**: Easy unit testing of configuration logic