import geopandas as gpd 
import pandas as pd 
from typing import List
from shapely.ops import unary_union
from shapely.geometry import Polygon

def add_block_id_to_buildings(bldgs: gpd.GeoDataFrame,
                              blocks: gpd.GeoDataFrame) -> gpd.GeoDataFrame:

    bldgs = gpd.sjoin(bldgs, bldgs, how='left', op='intersects')
    return bldgs

def convert_crs_4326_to_3395(gdf_list: List[gpd.GeoDataFrame]) -> List[gpd.GeoDataFrame]:
    '''
     conversion of dataframe to crs which allows
    for distance calculations
    '''

    rv = []
    for g in gdf_list:
        g.geometry.crs = {'init': 'epsg:4326'}  
        g.crs = {'init': 'epsg:4326'}
        g = g.to_crs("EPSG:3395")
        rv.append(g)
    return rv 

def building_density_per_block(bldgs: gpd.GeoDataFrame,
                               blocks: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    '''
    Adds a column to blocks dataframe which contains the total
    building area and the building density
    '''

    assert 'block_id' in bldgs.columns, "ERROR: bldgs dataframe does not have block_id"

    bldgs['bldg_area'] = bldgs.area 
    bldg_area_by_block = bldgs[['block_id', 'bldg_area']].groupby('block_id').sum()
    bldg_area_by_block.reset_index(inplace=True)

    blocks = blocks.merge(bldg_area_by_block, how='left', on='block_id')
    blocks['block_area'] = blocks.area 
    blocks['bldg_density'] = blocks['bldg_area'] / blocks['block_area']

    return blocks 


def max_min_distance(block_geom: Polygon, 
                     building_list: List[Polygon],
                     buffer_amt = 0.01) -> float:
    '''

    '''

    # Add the block's exterior to the building geom list
    block_bound_poly = block_geom.envelope.buffer(buffer_amt)
    block_exterior = block_bound_poly.difference(block_geom)
    building_list.append(block_exterior)

    # Make the buildings one geom
    other_geoms = unary_union(building_list)

    # Calculate hausdorff distance
    dist = block_geom.hausdorff_distance(other_geoms)

    return dist 

def get_block_building_list(bldgs: gpd.GeoDataFrame,
                            blocks: gpd.GeoDataFrame,
                            block_id: str) -> Tuple[Polygon, List[Polygon]]:
    '''
    Just a helper to get the buildings and block polygons 
    from their repsective sources, from the desired block_id
    '''

    block_geom = blocks[blocks['block_id']==block_id]['geometry'].iloc[0]
    building_list = list(bldgs[bldgs['block_id']==block_id]['geometry'].values)

    return block_geom, building_list




