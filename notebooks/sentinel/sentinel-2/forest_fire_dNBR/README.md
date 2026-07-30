
# Burned area detection and burned vegetation classification using openEO: dNBR and server-side machine learning

This notebook estimates the CO2 emissions of a forest fire, running openEO processes on the Copernicus Data Space Ecosystem (CDSE) backend. The burned area is first detected from the difference in Normalized Burn Ratio (dNBR) between a pre- and post-fire image, then the vegetation within that area is classified per-pixel using a Random Forest model trained locally and applied server-side through a User-Defined Function (UDF). The resulting vegetation map is combined with species-specific factors to estimate CO2 emissions, using a formula provided by the Intergovernmental Panel on Climate Change (IPCC) [1].

This work was developed based on the methodology Anton Donle developed: https://github.com/toschka123/ForestFireImpact

## Requirements

- Access to the [CDSE backend](https://openeo.dataspace.copernicus.eu).
- The GeoJSON file containing labels derived from the National Forest Inventory (`input_data/nfi_labels.geojson`).
- Refer environment set up in openEO UDP repository readme section [`### Environment Setup`](../../../../README.md#environment-setup).
- Run the `dnbr_vegetation_classification_udf.ipynb` notebook.
- Set the spatial and temporal coverage in `dnbr_vegetation_classification_udf.params.py` to change locations and time period.

This folder contains the following structure:

```
forest_fire_dNBR/
├── input_data/
│   └── nfi_labels.geojson
├── dnbr_vegetation_classification_udf.ipynb
└── dnbr_vegetation_classification_udf.params.py
```

## Data

- Sentinel-2 images accessed through openEO (CDSE): bands 4, 8 and 12 in time frame 01.01.2024 – 31.12.2024.
- Vegetation labels derived from National Forest Inventory [2] in GeoJSON format.

## Methodology

The steps performed in the notebook are:

### 1. Fire Area Detection

In the first step the fire area is detected using dNBR.

For this, the notebook loads pre- and post-fire satellite images as cubes. It uses a relatively short time period and reduces it to only use the last image taken in that period. The cube contains the bands 8 and 12. The resolution is resampled to 20 meters. The NBR is calculated with the formula:

$$NBR = \frac{B08 - B12}{B08 + B12}$$

The dNBR is calculated by subtracting the NBR of the two cubes via `merge_cubes`:

$$dNBR = NBR_{pre} - NBR_{post}$$

Healthy vegetation strongly reflects near-infrared light (B08) and absorbs short-wave infrared light (B12), giving a high NBR, while burned or stressed vegetation reflects less in the near-infrared and more in the short-wave infrared, giving a low or negative NBR. The larger the dNBR, the greater the drop in vegetation health between the pre- and post-fire images, indicating more severe fire damage. 

To create a binary mask that indicates whether a pixel was burned or not, a threshold of 0.3 is applied. Connected component labeling is applied to extract only the main area of the fire. This is used to generate a mask of the main fire area.

### 2. Machine Learning

In the second step the vegetation type is classified for each pixel in the fire area, using labels derived from the National Forest Inventory. The Portuguese NFI provides labels in a grid with 500m distance between the points (516 points in study area).

To train the classifier, a feature cube is built covering the full calendar year of 2024, reduced to monthly means, using bands 4, 8 and 12. The NDVI is also calculated and added to the cube as an additional feature, using the following formula:

$$NDVI = \frac{B04 - B08}{B04 + B08}$$

The function `aggregate_spatial` then samples this feature cube at the locations of the NFI labels, resulting in a cube that only contains pixels with a corresponding label. A simple random forest classifier is trained on this labeled data and tested on a held out split, achieving an overall accuracy of 0.74 and a macro F1 score of 0.67.

To avoid having to download all bands and monthly means for the area of interest (AOI), a UDF is registered to run in CDSE backend. The UDF takes cubes as input and outputs cubes, with additional information passed in the form of a dictionary via context.

Before it is shipped to the backend, the classifier is retrained locally on the full label set, then serialized with pickle and base64-encoded so it can be passed to the UDF as part of its JSON-serializable `context`. This keeps the UDF itself exclusively responsible for prediction. The alternative — training the Random Forest classifier and running prediction inside the same UDF — would mean retraining the model for every chunk the backend processes, which becomes resource-intensive as the raster or number of chunks grows.

On the backend, the UDF reshapes each chunk of the feature cube into per-pixel feature vectors, unpickles the classifier from `context`, and predicts a vegetation class for every pixel. Applied via `reduce_dimension`, it collapses the cube's band dimension into a single predicted-class band, so the full-resolution classification runs server-side and only the resulting raster needs to be downloaded.

The predicted classes are then visualized for all pixels within the fire mask, and counted to estimate how many hectares each vegetation species occupied.

In this notebook the UDF loads a pre-trained classifier (```clf```) and is defined as follows:

```
model_b64  =  base64.b64encode(pickle.dumps(clf)).decode("utf-8")
udf_code  =  textwrap.dedent("""
	import base64
	import pickle
	import numpy as np
	import xarray as xr
	
	def apply_datacube(cube: xr.DataArray, context: dict) -> xr.DataArray:
		clf = pickle.loads(base64.b64decode(context["model"]))
		label_names = context["label_names"]
		class_to_int = {cls: float(i) for i, cls in enumerate(label_names)}
		arr = cube.values
		n_t, n_bands, height, width = arr.shape
		X_pred = arr.reshape(n_t * n_bands, -1).T
		valid = ~np.isnan(X_pred).any(axis=1)
		preds_str = np.full(height * width, "NoData", dtype=object)
		preds_str[valid] = clf.predict(X_pred[valid])
		preds_float = np.array([class_to_int.get(p, -1.0) for p in preds_str])
		return xr.DataArray(
			preds_float.reshape(1, height, width),
			dims=cube.dims[1:],
			)
""")

context  = {	
	"model": model_b64,
	"label_names": label_names,
	}

udf  =  UDF(code=udf_code, runtime="Python", context=context)
```
An alternative approach is giving the train and test data as input in the context and train the machine learning classifier in the UDF as follows:
```
udf_code  =  textwrap.dedent("""
	import numpy as np
	import xarray as xr
	from sklearn.ensemble import RandomForestClassifier
	
	def apply_datacube(cube: xr.DataArray, context: dict) -> xr.DataArray:
		X_train = np.array(context["X_train"])
		y_train = np.array(context["y_train"])
		label_names = context["label_names"] # sorted list; index == class ID
		class_to_int = {cls: float(i) for i, cls in enumerate(label_names)}
		clf = RandomForestClassifier(n_estimators=100, random_state=42)
		clf.fit(X_train, y_train)
		arr = cube.values
		n_bands, height, width = arr.shape
		X_pred = arr.reshape(n_bands, -1).T # (pixels, n_bands)
		valid = ~np.isnan(X_pred).any(axis=1)
		preds_str = np.full(height * width, "NoData", dtype=object)
		preds_str[valid] = clf.predict(X_pred[valid])
		preds_float = np.array([class_to_int.get(p, -1.0) for p in preds_str])
		return xr.DataArray(
			preds_float.reshape(1, height, width),
			dims=cube.dims,
			)
""")

context  = {
	"X_train": X_train.tolist(),
	"y_train": y_train_str,
	"label_names": label_names,
	}
	
udf  = UDF(code=udf_code, runtime="Python", context=context)
```
The advantage with training the model in the UDF is that all calculations can be performed on the server-side, but the resulting disadvantage is that it needs to retrain for every batch, so it ends up repeating calculations unnecessarily. Loading a model into the UDF avoids this, but is limited by the size of the context, so only simpler models with a maximum size of ~2mb can be used. 

### 3. CO2 emissions

Each vegetation type is multiplied by species-specific factors to estimate the CO2 emissions caused by the fire. The factors are:

- **Fuel Density** — how much biomass is available per hectare.
- **Combustion Factor** — how much of the available biomass typically burns.
- **Emission Factor** — how much CO2 is released per unit of burned biomass.

The values were extracted from a report by the IPCC [1] and research carried out in Portugal [3].

## Limitations

- The UDF call is limited to 2MB, which significantly constrains the size of the Random Forest classifier passed in via `context`, so it needs to stay small and simple.
- The labels are derived from the NFI, with 500m distance. They are sparse and there are only 516 labeled points, which negatively impacts the performance of the classifier. Under-represented classes such as Eucalyptus have particularly few training samples, so they are classified less reliably than well-represented classes like Shrubland. 
## References

[1] Eggleston, H.S., Buendia, L., Miwa, K., Ngara, T., Tanabe, K. (eds.): 2006 IPCC Guidelines for National Greenhouse Gas Inventories. Institute for Global Environmental Strategies (IGES), Japan (2006).

[2] Uva, J.S., Onofre, R., Moreira, J., Faias, S.P., Barreiro, S., Santos, E., Capelo, J., Corte-Real, L., Martins, J., Ribeiro, J.R., Cancela, J., Rainha, M., Amaral, N., Santos, C., Perpétua, J., Pinho, J., Araújo, J.M., Reis, L., Canaveira, P., Paulino, J., Pina, A., Binev, Y., Coelho, P.: Forestry Inventory 2015. ICNF – Instituto da Conservação da Natureza e das Florestas (2021). https://doi.org/10.15468/33hvm4

[3] Alegria, C.: Aboveground biomass mapping and fire potential severity assessment: a case study for eucalypts and shrubland areas in the central inland region of Portugal. Forests 14(9), 1795 (2023). https://doi.org/10.3390/f14091795
