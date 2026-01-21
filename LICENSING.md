# Licensing

This repository uses a mixed-licensing approach.

## Default license (repo-level)

Unless stated otherwise in a file header, all original work in this repository is
licensed under the **MIT License** (see `LICENSE`).

## Converted Sentinel Hub evalscripts

Files that are converted from Sentinel Hub Custom Scripts **must retain the
original license**. The Sentinel Hub Custom Scripts are published under
**CC-BY-SA-4.0**, so converted files are also **CC-BY-SA-4.0**.

To keep this clear and non-viral, every converted file must include an explicit
header that states:

- The origin (converted from Sentinel Hub)
- The license that applies to that file (CC-BY-SA-4.0)
- A link to the original evalscript

This makes it clear that CC-BY-SA-4.0 applies only to those converted files, not
to the rest of the repository.

## Required header template

Use the following template at the top of each converted file.

### Jupyter notebook (first markdown cell)

```
## License

This notebook is a conversion of a Sentinel Hub evalscript and is licensed under
**CC-BY-SA-4.0**.

Original evalscript: <link>
Source: Sentinel Hub Custom Scripts (CC-BY-SA-4.0)
Conversion: Development Seed (openEO-UDP project)
```

### Code file (file header comment)

```
# License: CC-BY-SA-4.0
# Origin: Converted from Sentinel Hub evalscript
# Original evalscript: <link>
# Source: Sentinel Hub Custom Scripts (CC-BY-SA-4.0)
# Conversion: Development Seed (openEO-UDP project)
```

## Current CC-BY-SA-4.0 files

- `notebooks/sentinel/sentinel-2/fire_and_disaster_monitoring/bais2_burned_area.ipynb`
- `notebooks/sentinel/sentinel-2/marine_and_water_bodies/ndci_cyanobacteria.ipynb`
