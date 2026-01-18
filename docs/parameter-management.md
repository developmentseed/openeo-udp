# OpenEO UDP Parameter Management System

The OpenEO UDP Parameter Management System provides a unified interface for managing algorithm parameters and backend connections across different OpenEO endpoints. This system eliminates the need for manual parameter editing when switching between locations, time periods, or OpenEO backends.

## Overview

The parameter management system consists of three main components:

1. **Parameter Manager**: Core functionality for loading and managing parameter sets
2. **Endpoint Configuration**: Python-based configurations for different OpenEO backends
3. **Interactive Widgets**: User-friendly interface for parameter selection and connection

## Quick Start

```python
from openeo_udp import ParameterManager

# Initialize with your parameter file
param_manager = ParameterManager('algorithm_name.params.py')

# Quick programmatic connection
connection, params = param_manager.quick_connect(
    parameter_set='venice_lagoon',
    endpoint='copernicus_explorer'
)

# Or use interactive widgets in Jupyter
selection_widget = param_manager.interactive_parameter_selection()
connection, params = selection_widget()  # After UI interaction
```

## Parameter Files

### Structure

Parameter files are Python modules that define parameter sets for your algorithm. Each parameter set represents a specific location, time period, and algorithm configuration.

```python
# algorithm_name.params.py
from openeo.api.process import Parameter

def get_parameters():
    return {
        'venice_lagoon': {
            'location_name': 'Venice Lagoon, Italy',
            'bounding_box': Parameter(
                'bounding_box',
                description='Spatial extent for Venice Lagoon',
                default={'west': 12.0, 'south': 45.3, 'east': 12.6, 'north': 45.6}
            ),
            'time': Parameter(
                'time',
                description='Temporal range for data acquisition',
                default=['2023-06-01', '2023-06-30']
            ),
            'bands': Parameter(
                'bands',
                description='Sentinel-2 bands for analysis',
                default=['B02', 'B03', 'B04', 'B05', 'B08', 'B8A', 'B11']
            ),
            'collection': Parameter(
                'collection',
                description='Data collection identifier',
                default='SENTINEL2_L2A'
            ),
            'cloud_cover': Parameter(
                'cloud_cover',
                description='Maximum cloud cover percentage',
                default=30
            ),
        },
        'lake_victoria': {
            # Another parameter set...
        }
    }
```

### Parameter Guidelines

- **Use OpenEO Parameter objects**: All parameters except `location_name` should be `Parameter` objects
- **Include descriptions**: Provide clear descriptions for each parameter
- **Set sensible defaults**: Default values should work out-of-the-box
- **Group related locations**: Organize parameter sets by geographic region or use case

## Endpoint Configuration

The system supports multiple OpenEO backends with automatic parameter mapping to handle different collection IDs and band naming conventions.

### Available Endpoints

| Endpoint | Description | Collection ID | Band Format |
|----------|-------------|---------------|-------------|
| **copernicus_explorer** | EOPF Explorer API | `sentinel-2-l2a` | `reflectance\|{band}` |
| **copernicus_dataspace** | Copernicus Data Space | `SENTINEL2_L2A` | `{band}` |
| **ds_development** | Development Seed | `sentinel-2-l2a` | `{band}` |

### Parameter Mapping

The system automatically transforms parameters for different backends:

```python
# Original parameters
collection: 'SENTINEL2_L2A'
bands: ['B02', 'B03', 'B04']

# Mapped for EOPF Explorer
collection: 'sentinel-2-l2a'
bands: ['reflectance|b02', 'reflectance|b03', 'reflectance|b04']
```

## ParameterManager API

### Initialization

```python
param_manager = ParameterManager('path/to/params.py')
```

### Core Methods

#### Parameter Set Management

```python
# List available parameter sets
sets = param_manager.list_parameter_sets()
# Returns: ['venice_lagoon', 'lake_victoria', ...]

# Switch to a different parameter set
param_manager.use_parameter_set('lake_victoria')

# Get current parameter set
params = param_manager.get_parameter_set()
# Returns: {'location_name': 'Lake Victoria', 'bounding_box': Parameter(...), ...}

# Get specific parameter
bbox = param_manager.get_parameter('bounding_box')
# Returns: Parameter object with default value
```

#### Connection Methods

```python
# Quick programmatic connection
connection, params = param_manager.quick_connect(
    parameter_set='venice_lagoon',  # Optional, uses first if None
    endpoint='copernicus_explorer'  # Optional, uses first if None
)

# Interactive widget creation
widget = param_manager.interactive_parameter_selection()
# Returns: Callable that provides (connection, params) after UI interaction
```

#### Utility Methods

```python
# Print available options
param_manager.print_options("My Algorithm")

# Apply endpoint mapping manually
mapped_params = param_manager.apply_endpoint_mapping(params, 'copernicus_explorer')
```

## Interactive Widgets

The system provides Jupyter-friendly widgets for interactive parameter selection.

### Features

- **Dropdown menus**: Select parameter sets and endpoints
- **Real-time connection**: Connect to backends with progress feedback
- **Parameter display**: View current parameter values
- **Error handling**: Clear error messages and troubleshooting tips

### Usage Pattern

```python
# Create widget interface
selection_widget = param_manager.interactive_parameter_selection()

# Use widgets to select parameters and connect
# Then access results:
connection, current_params = selection_widget()

# Extract specific parameters
bounding_box = current_params['bounding_box']
time_range = current_params['time']
bands = current_params['bands']
collection = current_params['collection']
```

## Adding New Endpoints

To add support for a new OpenEO backend:

1. **Create endpoint module** in `openeo_udp/endpoints/`:

```python
# openeo_udp/endpoints/new_backend.py
from openeo.api.process import Parameter
from typing import Any, Dict

ENDPOINT_CONFIG = {
    "name": "New Backend",
    "url": "https://openeo.example.com",
    "auth_method": "oidc",
    "collection_id": "sentinel-2-l2a",
    "band_format": "{band}",
    "description": "Custom backend description",
    "capabilities": ["load_collection", "apply_dimension"]
}

def map_parameters(params: Dict[str, Any]) -> Dict[str, Any]:
    """Map parameters for this endpoint."""
    mapped_params = params.copy()

    for param_name, param_value in params.items():
        if isinstance(param_value, Parameter):
            if param_name == "collection":
                mapped_params[param_name] = Parameter(
                    param_value.name,
                    description=param_value.description,
                    default=ENDPOINT_CONFIG["collection_id"]
                )
            elif param_name == "bands" and isinstance(param_value.default, list):
                # Apply custom band mapping logic here
                pass

    return mapped_params
```

2. **Update endpoint registry** in `openeo_udp/endpoints/__init__.py`:

```python
from .new_backend import ENDPOINT_CONFIG as new_backend_config, map_parameters as new_backend_mapper

# Add to ENDPOINT_CONFIGS dictionary
```

## Best Practices

### Parameter File Organization

1. **Consistent naming**: Use descriptive, consistent names for parameter sets
2. **Geographic grouping**: Group related locations together
3. **Validation**: Include parameter validation in your parameter files
4. **Documentation**: Add comments explaining unusual parameter choices

### Error Handling

```python
try:
    connection, params = param_manager.quick_connect('invalid_set', 'invalid_endpoint')
except ValueError as e:
    print(f"Parameter error: {e}")
except ConnectionError as e:
    print(f"Connection failed: {e}")
```

### Performance Tips

1. **Reuse connections**: Cache connections when processing multiple parameter sets
2. **Minimize UI calls**: Use `quick_connect` for batch processing
3. **Parameter validation**: Validate parameters before attempting connections

## Troubleshooting

### Common Issues

**Parameter set not found**
```
ValueError: Parameter set 'typo_name' not found. Available: ['venice_lagoon', 'lake_victoria']
```
- Check parameter set name spelling
- Verify parameter file is correctly formatted

**Connection timeout**
```
ConnectionError: Unable to connect to backend
```
- Check internet connection
- Verify endpoint URL is accessible
- Try different authentication method

**Parameter mapping errors**
```
KeyError: 'collection' parameter not found
```
- Ensure all required parameters are defined
- Check parameter file structure

### Debug Mode

Enable verbose output for troubleshooting:

```python
# Use interactive widgets for detailed connection feedback
selection_widget = param_manager.interactive_parameter_selection()

# Or check endpoint configurations
from openeo_udp.endpoints import get_all_endpoints
print(get_all_endpoints())
```

## Migration from Manual Parameters

If you have existing notebooks with hardcoded parameters:

1. **Extract parameters** into a parameter file
2. **Replace hardcoded values** with parameter manager calls
3. **Add endpoint flexibility** using the mapping system
4. **Test with multiple endpoints** to ensure compatibility

### Migration Example

**Before:**
```python
# Hardcoded parameters
bbox = {'west': 12.0, 'south': 45.3, 'east': 12.6, 'north': 45.6}
time_range = ['2023-06-01', '2023-06-30']
connection = openeo.connect('https://openeo.example.com')
```

**After:**
```python
# Using parameter manager
param_manager = ParameterManager('algorithm.params.py')
connection, params = param_manager.quick_connect('venice_lagoon', 'copernicus_explorer')
bbox = params['bounding_box'].default
time_range = params['time'].default
```

## Examples and Templates

See the following notebooks for complete examples:

- [APA Aquatic Plants Detection](../notebooks/sentinel/sentinel-2/marine_and_water_bodies/apa_aquatic_plants_algae.ipynb)
- [NDCI Cyanobacteria Detection](../notebooks/sentinel/sentinel-2/marine_and_water_bodies/ndci_cyanobacteria.ipynb)

## Contributing

When adding new algorithms or improving existing ones:

1. **Follow parameter file conventions**
2. **Test with multiple endpoints**
3. **Include diverse parameter sets** (different locations, time periods)
4. **Document any special requirements**

For more details, see [CONTRIBUTING.md](../CONTRIBUTING.md).
