# Contributing to openEO UDP Conversion

Thank you for your interest in contributing to the Sentinel Hub evalscript to openEO conversion project! This guide will help you understand our conversion process and standards so your contributions can be integrated smoothly.

## Understanding the Conversion Process

Converting a Sentinel Hub evalscript to an openEO User-Defined Process involves more than simple translation. You need to understand both what the algorithm does scientifically and how to express that logic using openEO's process graph structure.

### The Nature of Evalscripts

Evalscripts are JavaScript functions that process satellite imagery pixel-by-pixel or in small neighborhoods. They typically define a `setup()` function that declares which bands are needed, an `evaluatePixel()` function that performs calculations on those bands, and often helper functions for color mapping or complex logic. The scripts are designed for synchronous, real-time visualization where users expect immediate visual feedback.

### openEO's Process Graph Approach

openEO represents algorithms as directed acyclic graphs where each node is a standardized process with defined inputs and outputs. Instead of procedural code that executes line-by-line, you construct a graph describing the data flow and transformations. This abstraction enables the same algorithm to run on different backends, but requires thinking about the computation differently than imperative programming.

## Conversion Workflow

### Phase 1: Script Analysis and Understanding

Before writing any code, thoroughly analyze the original evalscript:

- **Read the script documentation** to understand:
  - Its purpose and the scientific principle it implements
  - Typical applications
  - Any known limitations
  - Example: For NDCI, understand it's designed to detect cyanobacteria blooms by estimating chlorophyll-a concentrations using specific spectral bands

- **Identify all required inputs** including:
  - Satellite bands
  - Metadata like acquisition angles or timestamps
  - User-configurable parameters such as thresholds or scaling factors

- **Map the computational structure** by tracing the data flow from input bands through calculations to final output. Note:
  - Conditional logic (if statements that might require the `if` process)
  - Mathematical operations (which map to openEO's mathematical processes)
  - Temporal or spatial aggregations (requiring processes like `aggregate_temporal` or `reduce_dimension`)
  - Color mapping schemes (which may need custom color blend implementations)

- **Determine the processing pattern** to understand whether:
  - The algorithm can be computed tile-by-tile for web map tiling (suitable for synchronous visualization)
  - It requires broader temporal or spatial context (necessitating the synchronous processing endpoint)

### Phase 2: Environment Setup and Data Loading

- **Create a new Jupyter notebook** in the appropriate category directory
  - Start with a clear title and introduction section
  - Explain what the algorithm does, why it's useful, and what the expected outputs look like

- **Import the necessary libraries** including:
  - The openEO Python client
  - Visualization tools
  - Any specialized processing libraries
  - Establish a connection to the openEO backend, handling authentication appropriately

- **Define your test area** by selecting a spatial extent where the algorithm should produce meaningful results:
  - Water quality algorithms (like NDCI): choose areas with known water bodies
  - Vegetation indices: select regions with diverse vegetation types
  - Fire detection: ideally use areas with documented fire events

- **Load your initial dataset** using `load_collection`:
  - Request all necessary bands
  - Ensure appropriate temporal coverage
  - Use Cloud-Optimized GeoTIFF sources when available for best performance

### Phase 3: Algorithm Implementation

Implement the algorithm incrementally, building up from simple components to the complete process:

- **Start with basic band extraction**:
  - Ensure you can access all required spectral bands correctly
  - Test that band values are in the expected range and format

- **Implement intermediate calculations separately** if the algorithm has multiple stages:
  - Example: For NDCI, implement and validate the Floating Algae Index (FAI) calculation before proceeding to the main chlorophyll index
  - This modular approach makes debugging easier and creates reusable components

- **Build the main algorithm** using appropriate openEO processes:
  - Mathematical operations translate straightforwardly (addition, subtraction, multiplication, division)
  - Spectral indices often use the `normalized_difference` process
  - Conditional logic uses the `if` process
  - Array operations use `array_apply`, `array_element`, and related processes

- **Implement visualizations carefully**, as this often requires the most adaptation from evalscripts:
  - Simple color mappings can use openEO's color blend capabilities
  - Complex classifications may require building custom color lookup logic using nested `if` processes
  - Document your visualization choices clearly since color scales significantly affect how users interpret results

### Phase 4: Testing and Validation

Validate your converted algorithm against the original evalscript:

- **Compare visual outputs**:
  - Run the same scene through both the original evalscript (in Sentinel Hub) and your openEO conversion
  - They should produce visually similar results, though minor differences in interpolation or color mapping are acceptable

- **Test with multiple scenes** representing different conditions:
  - Vegetation index: test on forests, grasslands, agricultural areas, and bare soil
  - Water algorithm: test on clear water, turbid water, and coastal areas
  - This reveals whether your conversion generalizes properly or only works for specific conditions

- **Verify edge cases** including:
  - Areas with no data
  - Cloud-affected pixels
  - Extreme index values
  - Scenes at the boundaries of your spatial or temporal extent
  - Note: The original evalscript may handle these gracefully through JavaScript's error handling, so ensure your openEO version doesn't fail on such inputs

- **Document any differences honestly**:
  - If your conversion produces slightly different results than the original, explain why
  - This might be due to different data sources, preprocessing differences, or necessary adaptations to the openEO framework

### Phase 5: Documentation and Export

Write comprehensive documentation within the notebook:

- **The introduction** should:
  - Explain the algorithm's purpose in terms accessible to users who aren't remote sensing experts
  - Provide enough technical detail for those who are
  - Describe typical use cases and what users can learn from the output

- **Document the scientific methodology** by explaining:
  - The spectral indices used
  - The physical principles behind them (e.g., why near-infrared light reflects strongly from healthy vegetation)
  - Any calibration or validation studies that support the approach
  - Appropriate citations to peer-reviewed literature

- **Describe the implementation choices** you made:
  - Particularly where the openEO version differs from the original evalscript
  - Why you chose certain processes over alternatives
  - How you adapted conditional logic
  - Any limitations users should be aware of

- **Provide clear attribution**:
  - Credit the original evalscript author
  - Link to the source script
  - Acknowledge any modifications you made during conversion
  - Thank relevant institutions or funding sources

- **Export the final process graph** (TBD for automation):
  - Capture the built graph in a variable that can be serialized to JSON
  - Include a cell that demonstrates this export and saves the JSON to an appropriate location

## Coding Standards

### Process Graph Construction

Build process graphs that are clear and maintainable:

- Use meaningful variable names that describe what each step does. Rather than generic names like `cube1` and `cube2`, use `masked_water` and `vegetation_index` so the logic flow is self-documenting.
- Break complex operations into intermediate steps with their own variables. Don't chain dozens of operations into one massive expression. Each meaningful transformation should be a separate step that can be understood and debugged independently.
- Add comments explaining non-obvious logic, particularly for complex conditional structures or mathematical operations that implement specific scientific formulas. The comment should explain the "why," not just the "what."
- Include assertions or validation checks where appropriate to catch common errors early. For example, verify that spectral bands contain values in the expected range before performing index calculations.

### Visualization Implementation

Visualization code requires special attention:

- Document your color scales thoroughly by explaining what each color represents, the thresholds you chose and why, and providing a legend that users can reference when interpreting results.
- Test color scales across the full range of possible output values, ensuring that extreme values render appropriately and that transitions between colors occur at meaningful thresholds rather than arbitrary boundaries.
- Consider colorblind-friendly palettes when possible, avoiding color combinations that become indistinguishable for users with common forms of color vision deficiency.

### Performance Considerations

Write efficient process graphs:

- Minimize unnecessary operations by removing redundant calculations, combining operations where possible, and avoiding repeated data loading or processing of the same temporal slices.
- Use appropriate data types, ensuring you're not requesting unnecessarily high precision or resolution for intermediate calculations. Final outputs should have appropriate precision, but intermediate steps can often use lower precision for better performance.
- Leverage Cloud-Optimized formats by preferring COG or Zarr data sources over traditional formats when both are available, as this dramatically improves response times for synchronous processing.

## Testing Requirements

Every contribution must include appropriate testing:

### Visual Validation

Include in your notebook:

- Side-by-side comparisons of your openEO output with the original evalscript output, executed on the same scene. Show multiple examples representing different environmental conditions.
- Clear labeling that helps users understand what they're looking at, including dates, locations, algorithm parameters, and any relevant metadata.
- Discussion of any differences observed, explaining whether they're acceptable variations or potential issues that need investigation.

### Numerical Validation

Where possible, validate numerical accuracy:

- For algorithms that compute specific physical quantities (like chlorophyll-a concentration in NDCI), compare output values against expected ranges from the literature or reference measurements
- Test mathematical operations produce correct results by validating intermediate steps against manual calculations for sample pixels
- Verify that statistical aggregations (means, medians, quantiles) produce sensible results when compared to summary statistics from the original evalscript

### Edge Case Testing

Document how your conversion handles challenging situations:

- Missing data (no data values, masked pixels)
- Invalid values (negative indices where only positive values are physically meaningful)
- Extreme values (saturated pixels, very dark shadows)
- Temporal gaps in data availability
- Areas at the edge of satellite swath coverage

## Submission Process

When you're ready to contribute your conversion:

### Preparing Your Contribution

- **Ensure your notebook runs completely** from top to bottom without errors in a fresh Python environment
  - Clear all output, then execute all cells to verify reproducibility

- **Verify that all required files are included**:
  - Exported JSON process graphs
  - Example output images for documentation
  - Any supporting data files needed for testing

- **Check that your contribution follows the repository structure**:
  - Place files in appropriate directories
  - Follow naming conventions consistent with existing notebooks

### Creating a Pull Request

- **Fork the repository and create a new branch** for your contribution
  - Use a descriptive name like `convert-ndwi-script` or `add-burned-area-detection`

- **Commit your changes** with clear, descriptive commit messages
  - Explain what you did and why
  - Each commit should represent a logical unit of work

- **Open a pull request** with a comprehensive description including:
  - The original evalscript you converted and its author
  - What the algorithm does and what it's used for
  - Any challenges you encountered during conversion
  - Notable differences from the original, if any
  - Example outputs demonstrating successful conversion
  - Links to relevant documentation or scientific papers

### Review Process

- **A maintainer will review your contribution**, checking that it:
  - Follows our standards
  - Produces valid results
  - Includes appropriate documentation
  - Integrates well with existing conversions

- **You may receive feedback** requesting changes such as:
  - Improving documentation
  - Adjusting implementation details
  - Adding additional test cases
  - Clarifying attribution

- **Once approved**, your contribution will be merged and made available to the community
  - You'll be credited in the repository contributors list and in the specific notebook you created

## Getting Help

If you encounter difficulties during conversion:

- **Check existing notebooks** for similar algorithms that might provide patterns you can follow
  - The NDCI cyanobacteria notebook is a comprehensive example covering many common patterns

- **Consult the openEO processes documentation** to understand what processes are available and how to use them correctly

- **Ask questions** in the project Slack channel or GitHub discussions
  - The community is helpful and happy to assist with technical challenges, conceptual questions about openEO, or advice on conversion strategies

- **Open a draft pull request early** if you want feedback before completing your conversion
  - Maintainers can provide guidance while you're still working

## Advanced Topics

### Creating New openEO Processes

Sometimes an evalscript uses capabilities that don't exist in standard openEO processes. When this happens:

- **First check if you can achieve the same result** by combining existing processes in creative ways
  - Many seemingly complex operations can be constructed from simpler building blocks

- **If a new process is truly needed**:
  - Document the requirement in the notebook
  - Show why existing processes are insufficient
  - Explain what the new process would need to do

- **Follow the process proposal pipeline** for openEO:
  - Create a formal process specification
  - Provide a reference implementation
  - Submit it to the openEO community for review
  - Your work on this project could contribute to expanding openEO's capabilities

### Multi-Sensor Fusion

Some evalscripts combine data from multiple satellites (such as overlaying Sentinel-1 SAR data on Sentinel-2 optical imagery). These conversions require:

- Understanding the `merge_cubes` process and its requirements for spatial and temporal alignment
- Handling different spatial resolutions appropriately, either by resampling to a common grid or documenting requirements for pre-aligned data
- Managing temporal mismatches when satellites don't acquire data simultaneously, which may require temporal aggregation or nearest-neighbor selection

### Temporal Processing

Evalscripts that work with time series or temporal composites require different approaches:

- The `aggregate_temporal` process handles temporal averaging, median composites, or other statistical aggregations across time
- The `reduce_dimension` process along the temporal axis can implement custom temporal logic that doesn't fit standard aggregation functions
- Multi-temporal change detection typically requires loading multiple temporal slices, aligning them carefully, and computing differences or ratios between time periods

## Conclusion

Converting evalscripts to openEO UDPs makes valuable algorithms accessible across the entire openEO ecosystem while maintaining their utility for real-time exploration and analysis. Your contributions help build a library of interoperable Earth observation processes that benefit researchers, operational users, and educators worldwide.

Thank you for contributing to this important work. Your efforts make Earth observation more open, accessible, and interoperable for everyone.

---

For questions about these guidelines or the contribution process, please contact the project maintainers through GitHub issues.
