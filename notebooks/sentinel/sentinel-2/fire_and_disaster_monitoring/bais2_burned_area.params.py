"""Simple parameter definitions for BAIS2 notebook.

This file defines parameter sets that can be used with the BAIS2 algorithm.
"""


def get_parameters():
    """Return available parameter sets for the BAIS2 algorithm.

    Returns:
        Dictionary mapping parameter set names to parameter dictionaries
    """

    parameter_sets = {
        "gran_canaria": {
            "bounding_box": {
                "west": -15.91,
                "south": 27.73,
                "east": -15.29,
                "north": 28.22,
            },
            "time": ["2019-08-19", "2019-08-30"],
            "bands": ["B04", "B06", "B07", "B8A", "B12"],
            "collection": "SENTINEL2_L2A",
            "cloud_cover": 30,
        },
        "california_wildfire": {
            "bounding_box": {
                "west": -120.5,
                "south": 36.0,
                "east": -119.5,
                "north": 37.0,
            },
            "time": ["2020-09-01", "2020-09-15"],
            "bands": ["B04", "B06", "B07", "B8A", "B12"],
            "collection": "SENTINEL2_L2A",
            "cloud_cover": 20,
        },
        "australia_bushfire": {
            "bounding_box": {
                "west": 149.0,
                "south": -37.0,
                "east": 150.0,
                "north": -36.0,
            },
            "time": ["2019-12-01", "2019-12-15"],
            "bands": ["B04", "B06", "B07", "B8A", "B12"],
            "collection": "SENTINEL2_L2A",
            "cloud_cover": 25,
        },
    }

    return parameter_sets
