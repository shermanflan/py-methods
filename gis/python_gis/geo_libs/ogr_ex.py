import os, os.path, shutil, random

import shapely
import shapely.wkt
from shapely.geometry import Polygon, box

# GDAL libraries
from osgeo import gdal  # raster
from osgeo import ogr  # vector
from osgeo import osr  # spatial reference
from osgeo import gdal_array  # numpy integration
from osgeo import gdalconst

gdal.UseExceptions()

"""
Consider using batch commands ogrinfo, ogr2ogr over Python in some cases.
For example, when reprojecting vector data.
"""


def open_shapefile(shp_path):
    """
    Usage: This shape file uses NAD83
    shp_path = os.path.join(os.environ["DATA_DIR"], 'us_states', 'tl_2014_us_state.shp')

    :param path:
    :type path:
    :return:
    :rtype:
    """
    driver = ogr.GetDriverByName("ESRI Shapefile")

    # 0 means readonly
    dataSource = driver.Open(shp_path, 0)
    # Or:
    #dataSource = ogr.Open(shp_path)

    layer = dataSource.GetLayer()

    print(layer.GetSpatialRef())
    print(layer.GetFeatureCount())

    # Enumerate features attributes and geometry
    for feature in layer:
        print(feature.GetField("NAME"))

        geom = feature.GetGeometryRef()
        print(geom.Centroid().ExportToWkt())  # gets Geometry's centroid

    # Also:
    # for i in range(layer.GetFeatureCount()):
    #     print(layer.GetFeature(i).GetField("NAME"))


def write_shapefile(shp_path, shape=None):
    """
    Note that file handles need to be destroyed.

    Usage:
    shp_path = os.path.join(os.environ["DATA_DIR"], 'shapefile_out', 'ogr_ex.shp')

    :param shp_path:
    :type shp_path:
    :return:
    :rtype:
    """
    # 1 set the spatial reference (WGS84)
    spatial_ref = osr.SpatialReference()
    spatial_ref.SetWellKnownGeogCS('WGS84')

    # 2 create a new shapefile
    driver = ogr.GetDriverByName('ESRI Shapefile')
    shape_data = driver.CreateDataSource(shp_path)

    # 3 create the layer
    new_layer = shape_data.CreateLayer('polygon_layer', spatial_ref, ogr.wkbPolygon)

    id_field = ogr.FieldDefn("ID", ogr.OFTInteger)
    id_field.SetWidth(4)
    new_layer.CreateField(id_field)

    feature = ogr.Feature(new_layer.GetLayerDefn())
    feature.SetFID(0)
    feature.SetField("ID", 21)

    # 4 geometry is put inside feature
    # Json
    # geojson = '{"type":"Polygon","coordinates":[[[1,1],[5,1],[5,5],[1,5],[1,1]]]}'
    # polygon = ogr.CreateGeometryFromJson(geojson)
    # feature.SetGeometry(polygon)

    # WKT
    if not shape:
        shape = box(0.0, 0.0, 1.0, 1.0)
    wkt = shapely.wkt.dumps(shape)
    geometry = ogr.CreateGeometryFromWkt(wkt)
    feature.SetGeometry(geometry)

    # 5 feature is put into layer
    new_layer.CreateFeature(feature)

    # THIS IS ESSENTIAL - basically closes the feature
    feature.Destroy()  # or feature = None

    # THIS IS ESSENTIAL - basically closes the file handle
    shape_data.FlushCache()
    shape_data.Destroy()  # or shape_data = None


def create_polygon_from_json(geojson):
    """
    Usage:
    geojson = '{"type":"Polygon","coordinates":[[[1,1],[5,1],[5,5],[1,5], [1,1]]]}'

    :param geojson:
    :type geojson:
    :return:
    :rtype:
    """
    polygon = ogr.CreateGeometryFromJson(geojson)

    return polygon


def create_polygon():
    r = ogr.Geometry(ogr.wkbLinearRing)
    r.AddPoint(1, 1)
    r.AddPoint(5, 1)
    r.AddPoint(5, 5)
    r.AddPoint(1, 5)
    r.AddPoint(1, 1)
    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(r)

    print(poly.ExportToWkt())

    return poly


def spatial_filter(shp_path, minx, miny, maxx, maxy):
    """
    Filter input shapefile features by given bounding box.

    Usage:
    shp_path = os.path.join(os.environ["DATA_DIR"], 'us_states', 'tl_2014_us_state.shp')
    minx = -102, miny = 26, maxx = -94, maxy = 36
    :param minx:
    :type minx:
    :param miny:
    :type miny:
    :param maxx:
    :type maxx:
    :param maxy:
    :type maxy:
    :return:
    :rtype:
    """
    driver = ogr.GetDriverByName('ESRI Shapefile')
    data_source = driver.Open(shp_path, 0)  # read only

    layer = data_source.GetLayer()

    # Pass in the coordinates for the data frame to the SetSpatialFilterRect() function.
    # This filter creates a rectangular extent and selects the features inside the extent
    layer.SetSpatialFilterRect(minx, miny, maxx, maxy)

    for feature in layer:
        print(feature.GetField("NAME"))

    # THIS IS ESSENTIAL - basically closes the file handle
    data_source.FlushCache()
    data_source.Destroy()  # or data_source = None


def polygon_operations(poly):
    """

    :param poly:
    :type poly:
    :return:
    :rtype:
    """
    print(poly.Centroid())  # Point
    print(poly.GetBoundary())  # Linestring
    print(poly.ConvexHull())  # Polygon
    print(poly.Buffer(0))  # Polygon

    # Containment
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(10, 10)
    print(poly.Contains(point))


def analyze_geometry(geometry, indent=0):
    """
    Recursive

    :param geometry:
    :type geometry:
    :param indent:
    :type indent:
    :return:
    :rtype:
    """
    s = []
    s.append("  " * indent)
    s.append(geometry.GetGeometryName())
    if geometry.GetPointCount() > 0:
        s.append(" with {} data points".format(geometry.GetPointCount()))
    if geometry.GetGeometryCount() > 0:
        s.append(" containing:")

    print("".join(s))

    for i in range(geometry.GetGeometryCount()):
        analyze_geometry(geometry.GetGeometryRef(i), indent + 1)


def find_points(geometry, results):
    """
    Recursive

    :param geometry:
    :type geometry:
    :param results:
    :type results:
    :return:
    :rtype:
    """
    for i in range(geometry.GetPointCount()):
        x, y, z = geometry.GetPoint(i)
        if results['north'] == None or results['north'][1] < y:
            results['north'] = (x, y)
        if results['south'] == None or results['south'][1] > y:
            results['south'] = (x, y)

    for i in range(geometry.GetGeometryCount()):
        find_points(geometry.GetGeometryRef(i), results)


def random_examples(shapefile):
    """
    Using ogr to manipulate geo_libs spatial objects (shapefile)
    Usage: shapefile = ogr.Open("data/us_states/tl_2014_us_state.shp")

    :return:
    :rtype:
    """
    numLayers = shapefile.GetLayerCount()

    print(f"Shapefile contains {numLayers} layers")

    for layerNum in range(numLayers):
        layer = shapefile.GetLayer(layerNum)
        spatialRef = layer.GetSpatialRef().ExportToProj4()
        numFeatures = layer.GetFeatureCount()
        print(f"Layer {layerNum} has spatial reference {spatialRef}")
        print(f"Layer {layerNum} has {numFeatures} features")

        for featureNum in range(numFeatures):
            feature = layer.GetFeature(featureNum)
            featureName = feature.GetField("NAME")

            print(f"Feature {featureNum} has name {featureName}")

    layer = shapefile.GetLayer(0)
    feature = layer.GetFeature(12)

    print("Feature 12 has the following attributes:")

    attributes = feature.items()

    for key,value in attributes.items():
      print(f"  {key} = {value}")

    geometry = feature.GetGeometryRef()
    geometryName = geometry.GetGeometryName()

    print(f"Feature's geometry data consists of a {geometryName}")

    layer = shapefile.GetLayer(0)
    feature = layer.GetFeature(13)
    geometry = feature.GetGeometryRef()

    analyze_geometry(geometry)

    layer = shapefile.GetLayer(0)
    feature = layer.GetFeature(13)
    geometry = feature.GetGeometryRef()

    results = {'north': None,
               'south': None}

    find_points(geometry, results)

    print("Northernmost point is ({:.4f}, {:.4f})".format(
        results['north'][0], results['north'][1]))
    print("Southernmost point is ({:.4f}, {:.4f})".format(
        results['south'][0], results['south'][1]))

    from python_gis.apply.distance import haversine

    distance = haversine((results['north'][1], results['north'][0]), (results['south'][1], results['south'][0]))

    print("Great circle distance is {:0.0f} kilometers".format(distance))
