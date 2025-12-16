# openEO User-Defined Processes

This repository contains Jupyter notebooks that creates openEO User-Defined Processes (UDPs), initially from Sentinel Hub evalscripts. Each notebook documents the purpose of the UDP, validates the results, and exports the final process graph for integration with the openEO ecosystem.

## Project Context

This work is part of the [APEx (Application Propagation Environments)](https://apex.esa.int/) project for the European Space Agency. The goal is to convert the extensive library of [Sentinel Hub custom evalscripts](https://custom-scripts.sentinel-hub.com/) into interoperable openEO process graphs that can run on any openEO-compliant backend while maintaining synchronous visualization capabilities.

For more information about the project:

- [APEx Algorithm Catalogue](https://algorithm-catalogue.apex.esa.int/)

## Repository Structure

The repository is organized by category and sensor type following the structure of the original evalscripts:

```console
notebooks/
├── sentinel/
│   ├── sentinel-2/
│   │   ├── remote_sensing_indices/
│   │   │   ├── ndvi_enhanced.ipynb
│   │   │   └── ...
│   │   ├── marine_and_water_bodies/
│   │   │   ├── ndci_cyanobacteria.ipynb
│   │   │   └── ...
│   │   ├── cloud_detection/
│   │   │   ├── cohen_braaten_yang_cloud_detection.ipynb
│   │   │   └── ...
│   │   └── fire/
│   │       ├── bais2_burned_area.ipynb
│   │       └── ...
│   ├── sentinel-1/
│   └── ...
├── multi-sensor/
│   └── ...
└── README.md (this file)
```

## Notebook Structure

Each conversion notebook follows a consistent structure to ensure clarity and reproducibility. Using the [NDCI cyanobacteria detection example](notebooks/sentinel/sentinel-2/marine_and_water_bodies/ndci_cyanobacteria.ipynb) as a reference, a typical notebook contains:

### Introduction and Context

The notebook begins with a clear explanation of what the algorithm does, its scientific basis, and its practical applications. For instance, the NDCI notebook explains how the Normalized Difference Chlorophyll Index uses Sentinel-2's red and red-edge bands to estimate chlorophyll-a concentrations in water bodies, which is particularly valuable for detecting cyanobacteria blooms.

### Scientific Background

This section provides the mathematical foundation and methodology behind the algorithm. The NDCI notebook describes the spectral signatures of chlorophyll, the specific wavelengths used (Band 5 at 705 nm and Band 4 at 665 nm), and the empirically-derived calibration model that converts NDVI values to chlorophyll-a concentrations.

### Environment Setup

The notebook then establishes the technical environment by importing necessary libraries, connecting to the openEO backend, and configuring any required parameters. This includes libraries for data processing (openEO), visualization (matplotlib), and any specialized processing functions.

### Data Loading and Exploration

This section demonstrates how to load the initial dataset, define the spatial extent, select appropriate bands, and perform initial exploration of the data. The NDCI example shows how to extract multiple Sentinel-2 bands needed for both the main index and supporting calculations.

### Intermediate Calculations

If the algorithm requires preparatory steps, these are documented separately with their own explanations. The NDCI notebook includes the Floating Algae Index (FAI) calculation as an intermediate step for detecting surface algal blooms before computing the main chlorophyll index.

### Main Algorithm Implementation

This is the core of the notebook, where the primary algorithm is implemented using openEO processes. The implementation is broken down into understandable steps with clear variable names and comments explaining the logic. For NDCI, this includes water body identification, the NDCI calculation itself, and the conversion to chlorophyll-a concentrations.

### Visualization and Color Mapping

Many algorithms require custom visualization schemes to make their results interpretable. The NDCI notebook demonstrates how to create discrete color scales representing different water quality classifications, from oligotrophic (clear water) through eutrophic to bloom conditions.

### Process Graph Export

A critical section where the final openEO process graph is captured in a variable that can be serialized to JSON format. This export becomes the formal UDP definition that can be registered with openEO backends and consumed by various clients.

### Validation and Results

The notebook executes the process graph and displays results for visual validation. This often includes comparisons with natural color imagery to help verify that the algorithm is working correctly. The NDCI example shows both the chlorophyll-a map and a side-by-side comparison with true color imagery.

### Documentation and Attribution

Each notebook concludes with proper attribution to the original evalscript authors, citations for the scientific methodology, references to relevant publications, and acknowledgment of data sources used in the conversion.

## Getting Started

### Prerequisites

To run these notebooks, you need:

- Python 3.11 or later
- [uv](https://docs.astral.sh/uv/) for fast and reliable dependency management
- Access to an openEO backend (we recommend https://openeo.ds.io/ for testing)
- Basic understanding of remote sensing concepts and Python programming

### Environment Setup

This project uses [uv](https://docs.astral.sh/uv/) for fast and reliable dependency management.

1. **Install uv** if you haven't already:

   ```bash
   # On macOS and Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # On Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **Clone the repository and set up the environment**:

   ```bash
   git clone https://github.com/developmentseed/openeo-udp.git
   cd openeo-udp

   # Create virtual environment and install all dependencies
   uv sync
   ```

3. **Install as Jupyter kernel** (recommended for running notebooks):
   ```bash
   # Install the environment as a Jupyter kernel
   uv run python -m ipykernel install --user --name openeo-udp --display-name "openEO UDP"
   ```

The environment includes the openEO Python client library, visualization tools like matplotlib and Pillow, Jupyter, and all other dependencies needed to run the notebooks.

### Running a Notebook

Start Jupyter and open any notebook. For example, the [NDCI cyanobacteria notebook](notebooks/sentinel/sentinel-2/marine_and_water_bodies/ndci_cyanobacteria.ipynb):

```bash
# Start Jupyter using uv
uv run jupyter lab

# Or start Jupyter Notebook
uv run jupyter notebook
```

When creating or opening a notebook:

1. Make sure the "openEO UDP" kernel is selected (if you installed it as a kernel)
2. Open the [NDCI cyanobacteria notebook](notebooks/sentinel/sentinel-2/marine_and_water_bodies/ndci_cyanobacteria.ipynb)
3. Execute the cells sequentially to see the conversion process, validate results, and export the UDP definition

Most notebooks are designed to run completely from top to bottom without modification, though you may want to adjust spatial extents or temporal ranges to explore different areas.

## Using the Exported UDPs

Once a notebook has been executed and validated, the resulting UDP can be used in several ways:

### Direct Integration with openEO Backends

The exported JSON process graph can be registered as a UDP on openEO backends that support user-defined processes. This makes the algorithm available through standard openEO clients in Python, R, and JavaScript.

### APEx Algorithm Catalogue

Validated UDPs are published to the APEx Algorithm Catalogue, making them discoverable and accessible to the broader Earth observation community through a standardized interface.

### Synchronous Visualization Services

The converted algorithms can be consumed through web map tile services (XYZ endpoints) for real-time visualization in web mapping applications, maintaining the interactive nature of the original evalscripts.

## Contributing

We welcome contributions from the community! Whether you are converting additional evalscripts, improving existing conversions, or fixing bugs, your help makes this resource more valuable for everyone.

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on how to contribute to this project, including the conversion process, coding standards, testing requirements, and pull request procedures.

The [NDCI cyanobacteria notebook](notebooks/sentinel/sentinel-2/marine_and_water_bodies/ndci_cyanobacteria.ipynb) serves as a comprehensive reference implementation demonstrating best practices for conversion, documentation, and validation.

## Original Evalscripts

All algorithms in this repository are converted from Sentinel Hub's community-contributed evalscripts. The original scripts can be found at:

- [Sentinel Hub Custom Scripts Repository](https://custom-scripts.sentinel-hub.com/)
- [Custom Scripts GitHub](https://github.com/sentinel-hub/custom-scripts)

Each notebook includes specific attribution to the original script authors and links to the source evalscripts.

## Related Resources

### openEO Ecosystem

- [openEO API Specification](https://openeo.org/)
- [openEO Processes Documentation](https://processes.openeo.org/)
- [openEO Python Client](https://github.com/Open-EO/openeo-python-client)

### Sentinel Hub Documentation

- [Evalscript Documentation](https://docs.sentinel-hub.com/api/latest/evalscript/)
- [Custom Script Tutorial](https://docs.sentinel-hub.com/api/latest/evalscript/)

### Project Infrastructure

- [openEO by TiTiler](https://github.com/sentinel-hub/titiler-openeo)
- [Demo Instance](https://openeo.ds.io/)

## License

This project is licensed under the Apache License 2.0, consistent with the openEO ecosystem and Sentinel Hub custom scripts.

## Acknowledgments

This work is funded by the European Space Agency through the APEx project. We are grateful to:

- The Sentinel Hub team at Sinergise for creating the original evalscript infrastructure
- The openEO community for developing the interoperable processing standards
- All the scientists and developers who contributed the original evalscripts
- VITO, EODC, and other openEO backend providers for their collaboration

## Contact and Support

For questions, issues, or suggestions:

- Open an issue in this repository
- Contact the Development Seed team through the project issue tracker

---

**Note**: This repository is under active development as part of the evalscript conversion project. Some notebooks may be in draft form, and new conversions are added regularly as the project progresses.
