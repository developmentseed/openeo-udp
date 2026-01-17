"""
Parameter sets for Aquatic Plants and Algae (APA) detection algorithm.

This file defines parameter sets for different locations where the APA algorithm
can be applied for detecting aquatic vegetation and algae in water bodies.
"""

from openeo.api.process import Parameter

def get_parameters():
    """
    Return all available parameter sets for APA algorithm.
    
    Returns:
        dict: Dictionary with parameter set names as keys and parameter objects as values
    """
    
    parameter_sets = {
        'venice_lagoon': {
            'location_name': 'Venice Lagoon, Italy',
            'bounding_box': Parameter("bounding_box", default={
                'west': 12.0,
                'south': 45.25,
                'east': 12.6,
                'north': 45.6
            }),
            'time': Parameter("time", default=['2023-06-01', '2023-08-31']),
            'bands': Parameter("bands", default=['B02', 'B03', 'B04', 'B05', 'B08', 'B8A', 'B11']),
            'collection': Parameter("collection", default='SENTINEL2_L2A'),
            'cloud_cover': Parameter("cloud_cover", default=30)
        },
        
        'lake_victoria': {
            'location_name': 'Lake Victoria, Africa',
            'bounding_box': Parameter("bounding_box", default={
                'west': 31.5,
                'south': -3.0,
                'east': 35.0,
                'north': 0.5
            }),
            'time': Parameter("time", default=['2023-06-01', '2023-08-31']),
            'bands': Parameter("bands", default=['B02', 'B03', 'B04', 'B05', 'B08', 'B8A', 'B11']),
            'collection': Parameter("collection", default='SENTINEL2_L2A'),
            'cloud_cover': Parameter("cloud_cover", default=40)
        },
        
        'lake_taihu': {
            'location_name': 'Lake Taihu, China',
            'bounding_box': Parameter("bounding_box", default={
                'west': 119.8,
                'south': 30.9,
                'east': 120.9,
                'north': 31.7
            }),
            'time': Parameter("time", default=['2023-05-01', '2023-09-30']),
            'bands': Parameter("bands", default=['B02', 'B03', 'B04', 'B05', 'B08', 'B8A', 'B11']),
            'collection': Parameter("collection", default='SENTINEL2_L2A'),
            'cloud_cover': Parameter("cloud_cover", default=35)
        },
        
        'lake_pontchartrain': {
            'location_name': 'Lake Pontchartrain, Louisiana, USA',
            'bounding_box': Parameter("bounding_box", default={
                'west': -90.5,
                'south': 29.9,
                'east': -89.6,
                'north': 30.4
            }),
            'time': Parameter("time", default=['2023-04-01', '2023-10-31']),
            'bands': Parameter("bands", default=['B02', 'B03', 'B04', 'B05', 'B08', 'B8A', 'B11']),
            'collection': Parameter("collection", default='SENTINEL2_L2A'),
            'cloud_cover': Parameter("cloud_cover", default=25)
        }
    }
    
    return parameter_sets
