# License: CC-BY-SA-4.0
# Origin: Converted from Sentinel Hub evalscript
# Original evalscript: https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/ndvi_anomaly_detection/
# Source: Sentinel Hub Custom Scripts (CC-BY-SA-4.0)
# Conversion: Development Seed (openEO-UDP project)
"""Parameter definitions for NDVI Anomaly Detection.

This file defines parameter sets that can be used with the NDVI anomaly
algorithm, which compares the current month's NDVI against the same-month
average over the previous N years to highlight vegetation gain or loss
(e.g. drought stress or crop loss) from Sentinel-2 imagery.

The ``time`` parameter defines the *target month of the current year*; the
companion notebook derives the multi-year look-back window from ``time`` and
``nb_past_years``.
"""

from openeo.api.process import Parameter


def get_parameters():
    """Return available parameter sets for the NDVI anomaly algorithm.

    Returns:
        Dictionary mapping parameter set names to parameter dictionaries.
        Each parameter set includes:
        - location_name: Human-readable location identifier
        - bounding_box: Spatial extent as Parameter object
        - time: Target month (current year) as Parameter object
        - bands: Required Sentinel-2 bands as Parameter object
        - collection: Data collection identifier as Parameter object
        - cloud_cover: Maximum cloud cover percentage as Parameter object
        - nb_past_years: Number of past years to use as baseline
        - anomaly_clamp: Symmetric clamp on the anomaly (|current - past|)
        - ndvi_min: NDVI values at or below this are treated as invalid

    Note:
        NDVI is computed with ``normalized_difference`` (B08, B04), which is
        invariant to the band reflectance scale, so no ``reflectance_scale``
        parameter is required here (unlike the LAI/Cab biophysical algorithms).
    """

    # Bands required for the NDVI anomaly algorithm:
    # B04 (Red), B08 (NIR) for NDVI; SCL (Scene Classification Layer) for masking.
    ndvi_anomaly_bands = [
        "B04",
        "B08",
        "SCL",
    ]

    parameter_sets = {
        "cropland_plain_croatia": {
            "location_name": "Cropland Plain, Istria Coast, Croatia",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for Cropland Plain, Croatia",
                default={"west": 14.09, "south": 45.174, "east": 14.27, "north": 45.25},
            ),
            "time": Parameter(
                "time",
                description="Target month (current year) for the NDVI anomaly",
                default=["2024-06-01", "2024-07-01"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for NDVI anomaly detection",
                default=ndvi_anomaly_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="SENTINEL2_L2A",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum cloud cover percentage",
                default=60,
            ),
            "nb_past_years": Parameter(
                "nb_past_years",
                description="Number of past years to average as the NDVI baseline",
                default=3,
            ),
            "anomaly_clamp": Parameter(
                "anomaly_clamp",
                description="Symmetric clamp applied to the NDVI anomaly (pixelEvalMaxValue in the original script)",
                default=0.7,
            ),
            "ndvi_min": Parameter(
                "ndvi_min",
                description="NDVI values at or below this threshold are treated as invalid",
                default=-1.0,
            ),
        },
        "po_valley_cropland_italy": {
            "location_name": "Po Valley Cropland, Italy",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for the Po Valley agricultural plain, Italy",
                default={"west": 10.80, "south": 44.95, "east": 11.05, "north": 45.10},
            ),
            "time": Parameter(
                "time",
                description="Target month (current year) for the NDVI anomaly",
                default=["2022-07-01", "2022-08-01"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for NDVI anomaly detection",
                default=ndvi_anomaly_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="SENTINEL2_L2A",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum cloud cover percentage",
                default=60,
            ),
            "nb_past_years": Parameter(
                "nb_past_years",
                description="Number of past years to average as the NDVI baseline",
                default=3,
            ),
            "anomaly_clamp": Parameter(
                "anomaly_clamp",
                description="Symmetric clamp applied to the NDVI anomaly (pixelEvalMaxValue in the original script)",
                default=0.7,
            ),
            "ndvi_min": Parameter(
                "ndvi_min",
                description="NDVI values at or below this threshold are treated as invalid",
                default=-1.0,
            ),
        },
        # 2018 summer drought south of Leipzig, Germany — the representative
        # example from the original Sentinel Hub script (peak in August, end in
        # October). Requires the full Sentinel-2 archive (use the CDSE endpoint;
        # the titiler/EOPF catalog does not cover 2018).
        "leipzig_drought_2018_germany": {
            "location_name": "South of Leipzig, Germany (2018 drought, August peak)",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for the agricultural region south of Leipzig, Germany",
                default={"west": 12.20, "south": 51.10, "east": 12.50, "north": 51.28},
            ),
            "time": Parameter(
                "time",
                description="Target month (current year) for the NDVI anomaly",
                default=["2018-08-01", "2018-09-01"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for NDVI anomaly detection",
                default=ndvi_anomaly_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="SENTINEL2_L2A",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum cloud cover percentage",
                default=60,
            ),
            "nb_past_years": Parameter(
                "nb_past_years",
                description="Number of past years to average as the NDVI baseline",
                default=3,
            ),
            "anomaly_clamp": Parameter(
                "anomaly_clamp",
                description="Symmetric clamp applied to the NDVI anomaly (pixelEvalMaxValue in the original script)",
                default=0.7,
            ),
            "ndvi_min": Parameter(
                "ndvi_min",
                description="NDVI values at or below this threshold are treated as invalid",
                default=-1.0,
            ),
        },
        "leipzig_drought_2018_october_germany": {
            "location_name": "South of Leipzig, Germany (2018 drought, October end)",
            "bounding_box": Parameter(
                "bounding_box",
                description="Spatial extent for the agricultural region south of Leipzig, Germany",
                default={"west": 12.20, "south": 51.10, "east": 12.50, "north": 51.28},
            ),
            "time": Parameter(
                "time",
                description="Target month (current year) for the NDVI anomaly",
                default=["2018-10-01", "2018-11-01"],
            ),
            "bands": Parameter(
                "bands",
                description="Sentinel-2 bands required for NDVI anomaly detection",
                default=ndvi_anomaly_bands,
            ),
            "collection": Parameter(
                "collection",
                description="Data collection identifier",
                default="SENTINEL2_L2A",
            ),
            "cloud_cover": Parameter(
                "cloud_cover",
                description="Maximum cloud cover percentage",
                default=70,
            ),
            "nb_past_years": Parameter(
                "nb_past_years",
                description="Number of past years to average as the NDVI baseline",
                default=3,
            ),
            "anomaly_clamp": Parameter(
                "anomaly_clamp",
                description="Symmetric clamp applied to the NDVI anomaly (pixelEvalMaxValue in the original script)",
                default=0.7,
            ),
            "ndvi_min": Parameter(
                "ndvi_min",
                description="NDVI values at or below this threshold are treated as invalid",
                default=-1.0,
            ),
        },
    }

    return parameter_sets
