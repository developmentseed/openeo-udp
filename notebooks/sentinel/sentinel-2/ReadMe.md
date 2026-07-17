# Burned area detection and burned vegetation classification using openEO: dNBR and server-side machine learning

  

This notebook accesses the CDSE backend through openEO. The burned area is detected by making use of the difference in Normalized Burn Ratio (dNBR) between a pre- and post-fire image. Secondly, the burned vegetation is classified using machine learning. The algorithm is trained locally and run on the server side through a UDF. Lastly the resulting vegetation map is used as a basis for calculating the CO2 emissions caused by the fire with a formula provided by the Intergovernmental Panel on Climate Change (IPCC).

  

This notebook requires the CDSE backend and the GeoJson that contains labels derived from the National Forest Inventory. This folder contains the `dNBR_ML_UDF_Portugal.ipynb` notebook, its parameter file, and the `nfi_labels.geojson` file.

  

This work was developed as part of my internship with Development Seed. Based on the methodology I (Anton Donle) developed in my master's thesis: https://github.com/toschka123/ForestFireImpact

  

## Requirements / installation

  

Same as the root README, but this notebook uses additional packages. Regenerate the lockfile before syncing:

  

```bash

rm uv.lock

uv sync

```
Once the environment is set up, open and run `dNBR_ML_UDF_Portugal.ipynb`
  

## Data

  

Sentinel-2 images accessed through openEO (CDSE): bands 4, 8 and 12 in time frame 01.01.2024 – 31.12.2024.

  

Labels derived from National Forest Inventory as GeoJson.

  

## Details / Documentation

  

The steps performed in the notebook are:

  

### 1. Fire Area Detection

  

In the first step the fire area is detected by using the dNBR.

  

For this the notebook loads the pre- and post-fire satellite image as a cube. For this it uses a relatively short time period and reduces it to only use the last image taken in that period. The cube contains only the bands 8 and 12. The resolution is resampled to 20 m. The NBR is calculated with the formula:

  

NBR = (B08 - B12) / (B08 + B12)

  

The dNBR is calculated by subtracting between the two cubes via `merge_cubes`:

  

dNBR = NBR_pre – NBR_post

  

The larger the dNBR, the more the vegetation was damaged due to the fire. To create a binary mask that indicates whether a pixel was burned or not, a threshold of 0.3 is applied. Connected component labeling is applied to extract only the main area of the fire. This is used to generate a mask of the main fire area.

  

### 2. Machine Learning

  

In the second step the vegetation type is classified for each pixel in the fire area. As labels, a file derived from the National Forest Inventory is used. The Portuguese NFI provides labels in a grid with 500m distance between the points (500 points in study area).

  

A cube that is used as the feature space is loaded. The temporal range is the whole calendar year of 2024. The temporal range is reduced to the monthly mean. The bands that are used are 4, 8 and 12. Furthermore, the NDVI is calculated and added to the cube. The NDVI is calculated with the following formula:

  

NDVI = (B04 – B08) / (B04 + B08)

  

For training the algorithm, the function `aggregate_spatial` is used. It samples the cube at the locations of the labels, resulting in a cube that only contains pixels with a corresponding label. A simple random forest classifier is trained and tested on a held out split of the data. It achieves an overall accuracy of 0.74 and a macro F1 score of 0.67.

  

To avoid having to download all bands and monthly means for the AOI, a User Defined Function (UDF) is registered. A UDF takes cubes as input and outputs cubes. Additional information can be given in the form of a dictionary via context.

  

The Random Forest classifier is serialized with pickle and encoded as a string using base64. The UDF takes the classifier as an input via context and translates it back into a classifier object.

  

The UDF takes as input the cube containing the full feature space and outputs the prediction of the Random Forest classifier over the study area. Hence, it reduces the dimensionality of the cube and is applied via `reduce_dimension`.

  

The predicted classes are visualized for all pixels that fall within the mask of the fire area. Counting them allows us to estimate how many hectares each vegetation species occupied.

  

### 3. CO2 emissions

  

Each vegetation type is multiplied by species specific factors to estimate the CO2 emissions caused by the fire. Those factors are Fuel Density (How much biomass is available per hectare), Combustion Factor (how much of the available biomass typically burns) and the Emission Factor (how much CO2 is released per unit of burned biomass). The values were extracted from a report by the IPCC and research carried out in Portugal.

  

## Limitations

  

The call of the UDF is limited to 2MB. This limits the models that are fed in significantly. The models need to stay small and simple.

  

The labels are derived from the NFI, with 500m distance. They are sparse and only around 500 labeled points, which negatively impacts the performance of the classifier.

  


