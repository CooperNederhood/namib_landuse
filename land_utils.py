import geopandas as gpd 
import pandas as pd 

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

 