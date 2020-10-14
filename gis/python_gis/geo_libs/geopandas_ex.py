import os

import geopandas as gpd

# GDAL libraries
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
from osgeo import gdal_array
from osgeo import gdalconst


"""
Built on top of pandas, Fiona (I/O), and Shapely (geometry)
"""

# TODO: Interesting iterative approach
"""
import geopandas as gdp
from shapely.wkb import loads

arenas_df = cc.read('arenas_nba')

# Maybe filter here by arenas' bounding box?
# NOTE: Some shape files have an index file .shx which make this efficient.
states_df = gdp.read_file("C:\Data\US_States\US_States.shp")

for index, orig in states_df.iterrows():
    for index2, ref in arenas_df.iterrows():
      if loads(ref['the_geom'], hex=True).intersects(orig['geometry']):
          print(orig['STATE'], ref['team'])
"""


# TODO: Consider a default constraint to check for valid polygons
# via CHECK (ST_IsValid(shape))
# TODO: Can create a trigger or rule to listen to geometry changes
# via: NOT ST_Equals(OLD.geom, NEW.geom).
def read_shapefile(shp_path):
    """
    Usage: This shape file uses NAD83
    shp_path = os.path.join(os.environ["DATA_DIR"], 'us_states', 'tl_2014_us_state.shp')

    :param shp_path:
    :type shp_path:
    :return:
    :rtype:
    """
    states_df = gpd.read_file(shp_path)
    states_df.head()

    # Inspect geometry types
    print(states_df.head(5).geom_type)

    # Inspect CRS
    print(states_df.crs)

    # Change CRS
    # Mercator: https://spatialreference.org/ref/epsg/3395/
    #merc = states_df.to_crs('epsg:3395')
    merc = states_df[states_df.STUSPS.isin(['TX', 'OK', 'NM', 'LA'])].to_crs(epsg=3395)

    return merc


def overlap_lister(gdb_path, child_layer, parent_layer):
    """
    Uses intersection to get overlapping polygons which are then aggregated
    in a STRING_AGG like operation.
    
    Usage:
    # In WGS84: EPSG:4326
    child layer = 'NM_township'
    parent layer = 'Counties_US_WGS84'
    gdb_path = os.path.join(os.environ["DATA_DIR"], 'landgrid', 'DI_basemaps_WGS84.gdb')

    :param gdb_path:
    :type gdb_path:
    :param child_layer:
    :type child_layer:
    :param parent_layer:
    :type parent_layer:
    :return:
    :rtype:
    """
    counties_df = gpd.read_file(gdb_path, layer=parent_layer)
    nm_twp_df = gpd.read_file(gdb_path, layer=child_layer)

    # pre-generate sindex if it doesn't already exist
    nm_twp_df.sindex
    ovlaps_df = gpd.sjoin(nm_twp_df, counties_df, how='inner', op='intersects')
    ovlaps_agg_df = ovlaps_df.loc[:, ['TWPCODE', 'TWPLabel', 'County_Name']].copy()

    # ovlaps_join_df = (ovlaps_agg_df
    #                   .groupby('TWPLabel', sort=False)
    #                   .filter(lambda x: len(x['County_Name']) > 2)  # like HAVING
    #                   .groupby('TWPLabel', sort=False)
    #                   .aggregate({'TWPCODE': 'first',
    #                               'County_Name': ','.join})
    #                  )

    #Pandas 0.25.0
    ovlaps_join_df = (ovlaps_agg_df
                      .groupby('TWPLabel', sort=False)
                      .filter(lambda x: len(x['County_Name']) > 2)  # like HAVING
                      .groupby('TWPLabel', sort=False)
                      .aggregate(TWPCODE=('TWPCODE', 'first'),
                                 County_Count=('County_Name', 'size'),
                                 County_Overlaps=('County_Name', ','.join)))

    return ovlaps_join_df.reset_index()


def spatial_dissolve(gdb_path, layer=None):
    """
    Example below loads from gdb in WGS84, EPSG:4326.

    Usage:
    gdb_path = os.path.join(os.environ["DATA_DIR"], 'landgrid', 'DI_basemaps_WGS84.gdb')
    layer = 'Ohio_Sections'

    :param shp_path1:
    :type shp_path1:
    :return:
    :rtype:
    """
    ohio_df = gpd.read_file(gdb_path, layer)

    ohio_muni_df = ohio_df.dissolve(by=['COUNTY', 'TOWNSHIP'], aggfunc='first')

    return ohio_muni_df


def spatial_join(shp_path1, shp_path2):
    """
    Note: If neither df has a spatial index, a spatial index will be generated for the
    longer df.

    Usage:
    # In NAD83: EPSG:4269
    shp_path1 = os.path.join(os.environ["DATA_DIR"], 'us_states', 'tl_2014_us_state.shp')
    # In NAD27: EPSG:4267
    shp_path2 = os.path.join(os.environ["DATA_DIR"], 'roads', 'roads.shp')

    :param shp_path1:
    :type shp_path1:
    :param shp_path2:
    :type shp_path2:
    :return:
    :rtype:
    """

    states_df = gpd.read_file(shp_path1)
    roads_df = gpd.read_file(shp_path2)

    # Standardize to to WGS84, EPSG:4326
    states_wgs84_df = states_df.loc[:, ['STATEFP', 'STUSPS', 'NAME', 'geometry']].copy().to_crs(epsg=4326)
    roads_wgs84_df = roads_df.copy().to_crs(epsg=4326)

    # pre-generate sindex if it doesn't already exist
    roads_wgs84_df.sindex

    # Returns roads within states (plus state attributes)
    # op: 'intersects', 'contains', 'within'
    # See http://geopandas.org/mergingdata.html
    roads_states_df = gpd.sjoin(roads_wgs84_df, states_wgs84_df, how='inner', op='within')
    return roads_states_df


def calculate_centroids(shp_path):
    """

    :param shp_path:
    :type shp_path:
    :return:
    :rtype:
    """
    geo_df = gpd.read_file(shp_path)
    geo_df['centroids'] = geo_df.centroid
    geo_points = geo_df
    geo_points = geo_points.set_geometry('centroids')

    return geo_points


def write_geojson(shp_df, path):
    """

    :param shp_df: Geodataframe
    :type shp_df:
    :return:
    :rtype:
    """
    shp_df.to_file(driver='GeoJSON', filename=path)