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
from bokeh.tile_providers import get_provider, Vendors 

def get_polygon_coords(polygon: Polygon, coord_type: str):
    """Calculates coordinates ('x' or 'y') of a Point geometry"""
    if coord_type == 'x':
        return list(polygon.exterior.coords.xy[0])
    elif coord_type == 'y':
        return list(polygon.exterior.coords.xy[1])
    else:
        raise RuntimeError("Bad input")

def make_explorer(blocks_path: str):
    '''
    Loads a blocks path and creates an explorer for
    viewing blocks based on certain criteria
    '''

    blocks = gpd.read_file(blocks_path).to_crs("EPSG:3857")

    blocks['x'] = blocks['geometry'].apply(lambda p: get_polygon_coords(p, 'x'))
    blocks['y'] = blocks['geometry'].apply(lambda p: get_polygon_coords(p, 'y'))
    blocks['color'] = ['red']*blocks.shape[0]

    blocks_df = blocks.drop(columns=['geometry'])
    blocks_source = ColumnDataSource(data=blocks_df)

    TOOLTIPS = [
        ('OpenArea', '@max_dist'), ('BldgDensity', '@bldg_density')
    ]

    p = figure(background_fill_color="lightgrey", tooltips=TOOLTIPS, plot_width=1200, plot_height=600, sizing_mode='scale_both')

    blocks_source = ColumnDataSource(data=blocks_df)

    # Add patch renderer to figure.
    tile_provider = get_provider(Vendors.ESRI_IMAGERY)
    p.add_tile(tile_provider)
    block_viz = p.patches('x','y', source = blocks_source, 
                       fill_color = 'color',
                       line_color = 'black',
                       line_width = 0.25, 
                       fill_alpha = 0.5)









