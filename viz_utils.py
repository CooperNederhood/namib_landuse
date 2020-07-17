import typing 

import geopandas as gpd
from shapely.geometry import MultiPolygon, Polygon, MultiLineString, Point, LineString
from shapely.ops import cascaded_union
from shapely.wkt import loads
import pandas as pd
import numpy as np 
import time 

import os 
import matplotlib.pyplot as plt 
import sys 

from pathlib import Path  
from shapely.wkt import loads 

# Bokeh import 
from bokeh.plotting import figure, save
from bokeh.models import GeoJSONDataSource, ColumnDataSource, HoverTool, LinearColorMapper
from bokeh.palettes import RdYlBu11, RdYlGn11, Viridis11
from bokeh.io import output_notebook

def get_polygon_coords(polygon: Polygon, coord_type: str):
    """Calculates coordinates ('x' or 'y') of a Point geometry"""
    if coord_type == 'x':
        return list(polygon.exterior.coords.xy[0])
    elif coord_type == 'y':
        return list(polygon.exterior.coords.xy[1])
    else:
    	raise RuntimeError("Bad input")

