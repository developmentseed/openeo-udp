# OpenEO UDP Parameter Management System

The OpenEO UDP Parameter Management System provides a unified interface for managing algorithm parameters and backend connections across different OpenEO endpoints. This system eliminates the need for manual parameter editing when switching between locations, time periods, or OpenEO backends, and lets a single notebook produce both a synchronous preview **and** a reusable UDP export from the same parameterised graph.

> 💡 **Reference Implementation**: The [NDCI cyanobacteria notebook](../notebooks/sentinel/sentinel-2/marine_and_water_bodies/ndci_cyanobacteria.ipynb) is the canonical, up-to-date example. The [APA notebook](../notebooks/sentinel/sentinel-2/marine_and_water_bodies/apa_aquatic_plants_algae.ipynb) demonstrates the interactive-widget flow but still uses inline `.default` values for every parameter.

## Overview

The parameter management system consists of four main components:

1. **Parameter Manager**: Core functionality for loading parameter sets, resolving parameter references, and reconstructing DataCubes.
2. **Endpoint Configuration**: Python-based configurations for different OpenEO backends, including backend-specific attributes (band naming, collection ID, reflectance scale, dimension names).
3. **Interactive Widgets**: User-friendly interface for parameter selection and connection.
4. **Parameter Resolver**: Substitutes `{"from_parameter": "name"}` nodes in a flat graph with concrete defaults so the graph can be executed synchronously while remaining exportable as a UDP.

## Usage Patterns

The parameter management system supports two main usage patterns:

### 1. Interactive Widgets (Recommended for Notebooks)

Best for Jupyter notebooks where users want to select parameters interactively:

```python
# Create interactive widgets
selection_widget = param_manager.interactive_parameter_selection()
# User selects options via dropdown menus
connection, current_params = selection_widget()
```

**Benefits:**
- User-friendly interface with dropdown menus
- No need to remember parameter set names or endpoint IDs
- Handles authentication flows properly within widgets
- Perfect for exploratory analysis

### 2. Programmatic Approach (Ideal for Scripts)

Best for automation, scripts, or when you know exactly which parameters to use:

```python
# Direct connection with known parameters
connection, current_params = param_manager.quick_connect(
    parameter_set='venice_lagoon',
    endpoint='eopf_explorer'
)
```

**Benefits:**
- No user interaction required
- Perfect for automated workflows
- Reproducible parameter selection
- Ideal for batch processing

### When to Use Each Approach

**Use Interactive Widgets when:**
- Working in Jupyter notebooks
- Exploring different parameter combinations
- Creating tutorials or demos
- Users are not familiar with available parameter sets
- You want a user-friendly interface

**Use Programmatic Approach when:**
- Running automated scripts
- Processing multiple locations in batch
- Working in production environments
- You know the exact parameters needed
- Building APIs or services

## Intrinsic vs Runtime Parameters

When building a graph that will also be exported as a UDP, split parameters into two categories:

- **Intrinsic** — fixed by the algorithm itself. These should be passed to `load_collection` as `.default` values so they become literals in the graph. Examples: `collection`, `bands`, and the endpoint-derived keys `reflectance_scale`, `bands_dimension`, `time_dimension` (see [Endpoint Configuration](#endpoint-configuration)).
- **Runtime** — the knobs a UDP consumer is expected to swap per invocation. Pass these as the `Parameter` object itself (without `.default`) so the graph contains `{"from_parameter": "name"}` references. Typical runtime parameters: `bounding_box`, `time`, `cloud_cover`.

```python
s2cube = connection.load_collection(
    current_params["collection"].default,       # intrinsic → literal
    bands=current_params["bands"].default,      # intrinsic → literal
    spatial_extent=current_params["bounding_box"],  # runtime → from_parameter
    temporal_extent=current_params["time"],         # runtime → from_parameter
    properties={
        "eo:cloud_cover": lambda x: x <= current_params["cloud_cover"],  # runtime
    },
)
```

## Parameter Resolution

A parameterised graph cannot be executed synchronously: Copernicus Data Space (and openEO's `POST /result` endpoint in general) rejects graphs that still contain unresolved `{"from_parameter": ...}` nodes. Only the UDP registration and secondary-services APIs accept parameter definitions.

`ParameterManager` provides two helpers to bridge this gap:

```python
# Low-level: walk a flat graph and replace from_parameter refs with defaults
resolved_graph = param_manager.resolve_parameters(
    chl_a_image.flat_graph(), current_params
)

# High-level: returns a new DataCube/SaveResult bound to the same connection
resolved_cube = param_manager.resolve(chl_a_image, current_params)
resolved_cube.download("output.png")
```

The same source `chl_a_image` can then be exported as a UDP with its parameter references preserved:

```python
udp = {
    "process_graph": chl_a_image.flat_graph(),
    "parameters": [
        current_params["time"].to_dict(),
        current_params["bounding_box"].to_dict(),
        current_params["cloud_cover"].to_dict(),
    ],
    "id": "my_algorithm",
    ...
}
```

## Interactive Workflow Example

```python
# Step 1: Initialize parameter manager with algorithm-specific parameter file
param_manager = ParameterManager('apa_aquatic_plants_algae.params.py')

# Step 2: Display available options to user
param_manager.print_options("APA algorithm")
# This shows all parameter sets and available endpoints without triggering authentication

# Step 3: Create interactive widgets for user selection
selection_widget = param_manager.interactive_parameter_selection()
# This creates dropdown menus for endpoint and parameter set selection

# Step 4: Get connection and parameters after user interaction
connection, current_params = selection_widget()

# Step 5: Use parameters in your OpenEO workflow — intrinsic inline, runtime as refs
s2cube = connection.load_collection(
    current_params["collection"].default,
    temporal_extent=current_params["time"],
    spatial_extent=current_params["bounding_box"],
    bands=current_params["bands"].default,
    properties={
        "eo:cloud_cover": lambda x: x <= current_params["cloud_cover"],
    },
)

# ... build the rest of the graph ...

# Step 6: Resolve parameters before synchronous execution
resolved = param_manager.resolve(final_cube, current_params)
resolved.download("result.png")
```

## Quick Start

```python
from openeo_udp import ParameterManager

# Initialize with your parameter file
param_manager = ParameterManager('algorithm_name.params.py')

# Display available options
param_manager.print_options("Algorithm name")

# Option 1: Interactive approach (recommended for Jupyter notebooks)
selection_widget = param_manager.interactive_parameter_selection()
connection, current_params = selection_widget()  # After UI interaction

# Option 2: Programmatic approach (useful for scripts and automation)
connection, current_params = param_manager.quick_connect(
    parameter_set='venice_lagoon',
    endpoint='eopf_explorer'
)

# Build a parameterised graph (runtime params stay as Parameter refs)
s2cube = connection.load_collection(
    current_params["collection"].default,
    temporal_extent=current_params["time"],
    spatial_extent=current_params["bounding_box"],
    bands=current_params["bands"].default,
)

# Resolve before synchronous download
param_manager.resolve(s2cube, current_params).download("out.nc")
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

- **Use OpenEO Parameter objects**: All parameters except `location_name` should be `Parameter` objects.
- **Include descriptions**: Provide clear descriptions for each parameter.
- **Set sensible defaults**: Default values should work out-of-the-box.
- **Group related locations**: Organize parameter sets by geographic region or use case.
- **Decide intrinsic vs runtime at the call site, not in the param file**: All `Parameter` objects define a *potential* runtime knob. The notebook decides per-use whether to expose it (pass the `Parameter` itself) or to freeze it as a literal (pass `.default`). See [Intrinsic vs Runtime Parameters](#intrinsic-vs-runtime-parameters).

## Endpoint Configuration

The system supports multiple OpenEO backends with automatic parameter mapping to handle different collection IDs and band naming conventions.

### Available Endpoints

| Endpoint | Collection ID | Band Format | `reflectance_scale` | `bands_dimension` | `time_dimension` |
| --- | --- | --- | --- | --- | --- |
| **eopf_explorer** | `sentinel-2-l2a` | `reflectance\|{band}` | `1.0` | `bands` | `time` |
| **copernicus_dataspace** | `SENTINEL2_L2A` | `{band}` | `10000.0` | `bands` | `t` |
| **ds_development** | `sentinel-2-l2a` | `{band}` (+ resolution suffix) | `10000.0` | `bands` | `t` |
| **localhost_dev** | `sentinel-2-l2a` | `{band}` (+ resolution suffix) | `10000.0` | `bands` | `t` |

### Parameter Mapping

The system automatically transforms parameters for different backends. Beyond the collection-ID and band-name rewrites, each endpoint's `map_parameters` also injects three scalar values into `current_params` that the notebook can read directly:

| Key | Purpose | Consumer in the notebook |
| --- | --- | --- |
| `reflectance_scale` | Divisor to convert raw band values to 0–1 reflectance (1.0 if already reflectance, 10000.0 for integer L2A) | `data[i] / current_params["reflectance_scale"]` inside UDPs |
| `bands_dimension` | Name of the band/spectral dimension on this backend | `apply_dimension(dimension=current_params["bands_dimension"], ...)` |
| `time_dimension` | Name of the time dimension on this backend (`"t"` or `"time"`) | `reduce_dimension(dimension=current_params["time_dimension"], ...)` |

These are plain floats/strings, not `Parameter` objects, because they are intrinsic to the backend and should be baked into the graph as literals.

```python
# Original parameters
collection: 'SENTINEL2_L2A'
bands: ['B02', 'B03', 'B04']

# Mapped for EOPF Explorer
collection: 'sentinel-2-l2a'
bands: ['reflectance|b02', 'reflectance|b03', 'reflectance|b04']
reflectance_scale: 1.0
bands_dimension: 'bands'
time_dimension: 'time'
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
    endpoint='eopf_explorer'  # Optional, uses first if None
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
mapped_params = param_manager.apply_endpoint_mapping(params, 'eopf_explorer')
```

#### Resolution Methods

```python
# Low-level: walk a flat graph and replace from_parameter refs whose name
# appears in current_params with that parameter's .default. References whose
# name is not in current_params (typically callback-scoped placeholders like
# "data", "value", "x") are preserved unchanged.
resolved_graph = param_manager.resolve_parameters(
    datacube.flat_graph(),
    current_params,   # optional, defaults to the current parameter set
)

# High-level: return a new DataCube/SaveResult with all refs resolved, bound
# to the same connection as the input. Use this before any synchronous call
# (.download(), .execute()) while keeping the original `datacube` parameterised
# for UDP export.
resolved_cube = param_manager.resolve(datacube, current_params)
resolved_cube.download("output.png")
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
    # Backend-specific intrinsic attributes; see the Endpoint Configuration
    # table above for the meaning of each key.
    "reflectance_scale": 10000.0,   # 1.0 if bands are already 0-1 reflectance
    "bands_dimension": "bands",     # name of the band dimension on this backend
    "time_dimension": "t",          # "t" or "time" depending on the backend
    "description": "Custom backend description",
    "capabilities": ["load_collection", "apply_dimension"],
    "enabled": True,
}


def map_parameters(params: Dict[str, Any]) -> Dict[str, Any]:
    """Map parameters for this endpoint."""
    mapped_params = params.copy()

    # Propagate the intrinsic backend attributes so the notebook can read them
    # from current_params as plain scalars.
    mapped_params["reflectance_scale"] = ENDPOINT_CONFIG["reflectance_scale"]
    mapped_params["bands_dimension"] = ENDPOINT_CONFIG["bands_dimension"]
    mapped_params["time_dimension"] = ENDPOINT_CONFIG["time_dimension"]

    for param_name, param_value in params.items():
        if isinstance(param_value, Parameter):
            if param_name == "collection":
                mapped_params[param_name] = Parameter(
                    param_value.name,
                    description=param_value.description,
                    default=ENDPOINT_CONFIG["collection_id"],
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
# Using parameter manager with runtime parameters kept as refs
param_manager = ParameterManager('algorithm.params.py')
connection, params = param_manager.quick_connect('venice_lagoon', 'eopf_explorer')

s2cube = connection.load_collection(
    params['collection'].default,
    bands=params['bands'].default,
    spatial_extent=params['bounding_box'],   # Parameter ref, not .default
    temporal_extent=params['time'],
)

# Resolve before sync execution; the unresolved graph is still usable for UDP export.
param_manager.resolve(s2cube, params).download('out.nc')
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
