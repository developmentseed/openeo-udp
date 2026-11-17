# openeo-portable

Parameter and backend management for portable openEO notebooks and User-Defined Processes (UDPs).

`openeo-portable` lets you write an openEO workflow once and run it on several openEO backends and study areas, without editing the code. It provides:

- **Parameter sets.** Each algorithm has a `.params.py` file with named sets of locations, dates and settings (for example `venice_lagoon`). The parameter files for the [openeo-udp notebooks](https://github.com/developmentseed/openeo-udp) ship with the package.
- **Endpoint mapping.** Collection IDs, band names and dimension names differ between backends. The package rewrites them for the backend you connect to, so the same process graph works on each one.
- **Interactive selection.** Dropdown widgets in Jupyter for choosing a parameter set and a backend.
- **Parameter resolution.** Turns `Parameter` references into concrete values, so a graph that will later be exported as a UDP can also run synchronously.

## Installation

```bash
pip install openeo-portable
```

To run the openeo-udp notebooks, install the `notebooks` extra as well. It adds matplotlib, NumPy, Pillow and rioxarray:

```bash
pip install "openeo-portable[notebooks]"
```

Requires Python 3.11 or later.

## Quick start

```python
from openeo_portable import ParameterManager

# Load a parameter file that ships with the package
param_manager = ParameterManager("apa_aquatic_plants_algae.params.py")

# Show the parameter sets and endpoints you can choose from
param_manager.print_options("Aquatic plants and algae")

# Option 1: choose with dropdown widgets (in Jupyter)
selection_widget = param_manager.interactive_parameter_selection()
connection, current_params = selection_widget()

# Option 2: choose in code (in scripts)
connection, current_params = param_manager.quick_connect(
    param_set="venice_lagoon",
    endpoint="eopf_explorer",
)
```

`current_params` holds the parameters mapped for the chosen backend. Use them to build a parameterised graph, then resolve it before running it synchronously:

```python
cube = connection.load_collection(
    current_params["collection"].default,
    bands=current_params["bands"].default,
    spatial_extent=current_params["bounding_box"],
    temporal_extent=current_params["time"],
    properties={"eo:cloud_cover": lambda x: x <= current_params["cloud_cover"]},
)

# The synchronous /result endpoint rejects unresolved parameter references
param_manager.resolve(cube, current_params).download("preview.nc")
```

The endpoint mapping also adds three backend values to `current_params`: `reflectance_scale`, `bands_dimension` and `time_dimension`. Read them from `current_params` instead of hard-coding them, so the graph stays backend-agnostic.

## Supported endpoints

| Endpoint | Backend |
| --- | --- |
| `eopf_explorer` | EOPF Sentinel Zarr Samples Explorer |
| `copernicus_dataspace` | Copernicus Data Space Ecosystem |
| `ds_development` | Development Seed development instance |
| `localhost_dev` | A local openEO backend for development |

```python
from openeo_portable.endpoints import list_available_endpoints

list_available_endpoints()
```

## Parameter files

Parameter files for the openeo-udp algorithms ship in `openeo_portable.params`. A bare file name such as `ParameterManager("urban_areas.params.py")` loads the packaged file. To list them:

```python
from openeo_portable import list_parameter_files

list_parameter_files()
```

### Using your own parameter file

You can override a packaged parameter file without changing the package. Put a file with the same name in your working directory, and `ParameterManager` loads it instead of the packaged one. The easiest start is a copy of the packaged file:

```python
import shutil
from importlib.resources import files

shutil.copy(files("openeo_portable.params") / "urban_areas.params.py", "urban_areas.params.py")
```

Edit the copy, for example to add a parameter set for your own area and dates. `print_options()` shows which file was loaded and warns when a local file overrides the packaged one. Delete or rename the local file to go back to the packaged version.

You can also give your file a different name and pass its path, for example `ParameterManager("my_urban_areas.params.py")`.

## Documentation

- [Parameter management guide](https://github.com/developmentseed/openeo-udp/blob/main/docs/parameter-management.md): parameter file format, endpoint mapping, the full `ParameterManager` API, and how to add a new endpoint.
- [openeo-udp notebooks](https://github.com/developmentseed/openeo-udp): the notebooks that use this package to build UDPs for the [APEx Algorithm Catalogue](https://algorithm-catalogue.apex.esa.int/).
- [Contributing](https://github.com/developmentseed/openeo-udp/blob/main/CONTRIBUTING.md)

## License

`MIT AND CC-BY-SA-4.0`:

- The package code is MIT ([LICENSE](https://github.com/developmentseed/openeo-udp/blob/main/LICENSE)).
- The parameter files in `openeo_portable/params/` are converted from [Sentinel Hub custom scripts](https://custom-scripts.sentinel-hub.com/) and are [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/). Each file's header links to its original evalscript.

See [LICENSING.md](https://github.com/developmentseed/openeo-udp/blob/main/LICENSING.md) for details.

## Acknowledgments

Developed by [Development Seed](https://developmentseed.org/) as part of the [APEx](https://apex.esa.int/) project, funded by the European Space Agency.
