#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''type description here'''

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from geopy.distance import geodesic
from shapely import LineString

def find_midpoint(line):
    """
    Calculate the geographic midpoint of a LineString based on its length.
    
    This function computes the midpoint of a LineString by finding the point along the line
    that is half of the line's total length. This is particularly useful for finding a central
    point in a set of geographical coordinates represented as a LineString.

    Args:
    line (LineString): A Shapely LineString object consisting of two or more points.

    Returns:
    Point: A Shapely Point object representing the geographic midpoint of the LineString.
    """
    # Calculate the total length of the LineString.
    total_length = line.length
    
    # Find the length from the start to the midpoint.
    half_length = total_length / 2
    
    # Interpolate to find the midpoint based on the half_length.
    midpoint = line.interpolate(half_length)
    
    return midpoint

def compute_midpoints(df_dam):
    """
    Compute the geographical midpoint for each dam based on multiple latitude and longitude entries.
    
    Args:
    df_dam (pd.DataFrame): DataFrame containing dam names and their corresponding latitude and longitude.
    
    Returns:
    pd.DataFrame: A DataFrame with columns for dam name, longitude, and latitude of the midpoint.
    """
    # Initialize an empty DataFrame for the midpoints.
    df_center = pd.DataFrame(columns=['name', 'longitude', 'latitude'])

    # Process each dam's data grouped by the dam's name.
    for name, group in df_dam.groupby('Name'):
        # Extract coordinates into a list of tuples.
        coordinates_list = group[['Latitude', 'Longitude']].values.tolist()
        # Create a LineString from these coordinates.
        line = LineString(coordinates_list)
        
        # Optional: Calculate the total length of the LineString.
        # total_length = sum(geodesic(coordinates_list[i], coordinates_list[i+1]).meters for i in range(len(coordinates_list) - 1))
        
        # Find the midpoint of the LineString.
        midpoint = find_midpoint(line)
        
        # Prepare a new row for the results DataFrame.
        temp_df = pd.DataFrame([{'name': name, 'longitude': midpoint.y, 'latitude': midpoint.x}])
        
        # Append the new row to the results DataFrame.
        df_center = pd.concat([df_center, temp_df], ignore_index=True)

    return df_center

