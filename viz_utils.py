import typing 
from typing import List 

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
from bokeh.models import GeoJSONDataSource, RangeSlider, CustomJS
from bokeh.io import output_notebook
from bokeh.tile_providers import get_provider, Vendors 
from bokeh.layouts import row, column

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
    p_width = 1200
    p_height = 600

    blocks['x'] = blocks['geometry'].apply(lambda p: get_polygon_coords(p, 'x'))
    blocks['y'] = blocks['geometry'].apply(lambda p: get_polygon_coords(p, 'y'))
    blocks['color'] = ['red']*blocks.shape[0]

    blocks_df = blocks.drop(columns=['geometry'])
    blocks_source = ColumnDataSource(data=blocks_df)

    TOOLTIPS = [
        ('OpenArea', '@max_dist'), ('BldgDensity', '@bldg_density'), ('BlockID', '@id')
    ]
    p = figure(background_fill_color="lightgrey", tooltips=TOOLTIPS, plot_width=p_width, plot_height=p_height,
               match_aspect=True)

    p_map = figure(background_fill_color="lightgrey", tooltips=TOOLTIPS, plot_width=p_width, plot_height=p_height,
                   x_range=p.x_range, y_range=p.y_range)

    # p = figure(background_fill_color="lightgrey", tooltips=TOOLTIPS, plot_width=p_width, plot_height=p_height,
    #          x_axis_type="mercator", y_axis_type="mercator", match_aspect=True)

    # p_map = figure(background_fill_color="lightgrey", tooltips=TOOLTIPS, plot_width=p_width, plot_height=p_height,
    #              x_axis_type="mercator", y_axis_type="mercator", x_range=p.x_range, y_range=p.y_range)
    blocks_source = ColumnDataSource(data=blocks_df)
    # Add patch renderer to figure.
    tile_provider = get_provider(Vendors.ESRI_IMAGERY)
    tile_provider2 = get_provider(Vendors.ESRI_IMAGERY)
    p.add_tile(tile_provider)
    p.patches('x','y', source = blocks_source, 
                       fill_color = 'color',
                       line_color = 'black',
                       line_width = .5, 
                       fill_alpha = 0.5)
    p_map.add_tile(tile_provider2)
     
    density_slider = RangeSlider(start=0.0, end=1.0, value=(0.0,1.0), step=.01, title="Selected density")
    b_min = blocks['max_dist'].min()
    b_max = blocks['max_dist'].max()
    area_slider = RangeSlider(start=b_min, end=b_max, value=(b_min, b_max), title='Selected open area')

    javascript_string = """
            var data = source.data;
            var color = data['color'];

            var v_min = cb_obj.value[0];
            var v_max = cb_obj.value[1];
            var col_data = data[col];

            var v_min_other = other_slider.value[0];
            var v_max_other = other_slider.value[1];
            var other_col_data = data[other_col];

            var l = color.length;
            
            var cur_col_data = 0.0;
            var col_bool = true;

            var other_cur_col_data = 0.0;
            var other_col_bool = true;

            for (var i = 0; i < l; i++) {
              
              cur_col_data = col_data[i];
              other_cur_col_data = other_col_data[i];

              col_bool = cur_col_data >= v_min && cur_col_data <= v_max;
              other_col_bool = other_cur_col_data >= v_min_other && other_cur_col_data <= v_max_other;
              
              if (col_bool && other_col_bool) {
                color[i] = 'red';
              }
              else {
                color[i] = 'blue';
              }
            }

            source.change.emit();
        """

    density_callback = CustomJS(args=dict(source=blocks_source, 
                                          col='bldg_density',
                                          other_slider=area_slider,
                                          other_col='max_dist'), code=javascript_string)

    area_callback = CustomJS(args=dict(source=blocks_source, 
                                          col='max_dist',
                                          other_slider=density_slider,
                                          other_col='bldg_density'), code=javascript_string)


    density_slider.js_on_change('value', density_callback)
    area_slider.js_on_change('value', area_callback)

    layout = column(density_slider, area_slider, p, p_map)
    return layout, blocks


def save_selection(df: gpd.GeoDataFrame, 
                   name: str,
                   project_path: str) -> None:
    '''
    Saves selection to directory
    '''
    out_dir = Path(project_path) / 'exported' 
    out_dir.mkdir(parents=True, exist_ok=True)
    v = 0
    out_path = out_dir / "{}.v{}.geojson".format(name, v)
    while out_path.is_file():
        v += 1
        out_path = out_dir / "{}.v{}.geojson".format(name, v)
    if 'x' in df.columns:
        df = df.drop(columns=['x'])
    if 'y' in df.columns:
        df = df.drop(columns=['y'])
    df.to_file(str(out_path), driver='GeoJSON')
    print('Saved to: {}'.format(out_path.resolve()))
    
def EXPORT_SELECTION(data: gpd.GeoDataFrame,
                     search_name: str = 'MY_FIRST_SEARCH', 
                     density_minimum: float = None, 
                     density_maximum: float = None, 
                     area_minimum: float = None, 
                     area_maximum: float = None, 
                     block_list: List = None,
                     project_path: str = "/content/gdrive/My Drive/namib_landuse/"):
    '''
    Saves out a version of data with only the blocks that fullfill
    some criteria specified by the user
    '''
    
    # Select blocks based on search criteria
    b = pd.Series([True]*data.shape[0])
    if density_minimum is not None:
        b0 = data['bldg_density'] >= density_minimum
        b = np.all([b, b0], axis=0)
    if density_maximum is not None:
        b0 = data['bldg_density'] <= density_maximum
        b = np.all([b, b0], axis=0)
    if area_minimum is not None:
        b0 = data['max_dist'] >= area_minimum
        b = np.all([b, b0], axis=0)
    if area_minimum is not None:
        b0 = data['max_dist'] <= area_maximum
        b = np.all([b, b0], axis=0)
    
    total_crit = b.sum()
    print("Selecting {} blocks based on search criteria".format(total_crit))
    
    if block_list is not None:
        if len(block_list) > 0:
            block_set = set(block_list)
            b0 = data['block_id'].apply(lambda x: x in block_set)
            b = np.any([b, b0], axis=0)
            total_final = b.sum()
            added = total_final - total_crit
            s = "Hand selected {} more blocks".format(len(block_list))
            if len(block_list) != added:
                s += " [Note: {} hand added blocks were already in the selection]".format((len(block_list) - added))
            print(s)
    
    selected_data = data.iloc[b]
    print("Selecting {} total blocks in report".format(selected_data.shape[0]))
    print()
    save_selection(selected_data, search_name, project_path)
    #return selected_data
    








