
import shapely.wkt
import shapely.geometry

# GDAL libraries
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
from osgeo import gdal_array
from osgeo import gdalconst

from python_gis.geo_libs.ogr_ex import write_shapefile

gdal.UseExceptions()


def get_nearest_neighbors(neighbors_path, target_path, max_distance=0.1):
    """
    Find parks near polygons within max_distance.

    in_path = os.path.join(home, "cbsa", "tl_2019_us_cbsa.shp")
    parks = os.path.join(home, "cbsa", "CA_Features_20191101.txt")

    :param neighbors_path:
    :type neighbors_path:
    :param target_path:
    :type target_path:
    :param max_distance:
    :type max_distance:
    :return:
    :rtype:
    """
    urbanAreas = {}  # Maps area name to Shapely polygon.

    shapefile = ogr.Open(neighbors_path)
    layer = shapefile.GetLayer(0)

    for i in range(layer.GetFeatureCount()):
        print("Dilating feature {} of {}".format(i, layer.GetFeatureCount()))

        feature = layer.GetFeature(i)
        name = feature.GetField("NAME")
        geometry = feature.GetGeometryRef()
        wkt = geometry.ExportToWkt()
        outline = shapely.wkt.loads(wkt)
        dilatedOutline = outline.buffer(max_distance)  # angular dist 0.1 = 1km
        urbanAreas[name] = dilatedOutline

    with open(target_path) as f:
        for line in f.readlines():
            chunks = line.rstrip().split("|")

            if chunks[2] == "Park":
                park_name = chunks[1]
                latitude = float(chunks[9])
                longitude = float(chunks[10])

                pt = shapely.geometry.Point(longitude, latitude)
                for urbanName, urbanArea in urbanAreas.items():
                    if urbanArea.contains(pt):
                        print("{} is in or near {}".format(park_name, urbanName))


def get_common_border(from_path, to_path):
    """
    in_path = os.path.join(home, "countries", "TM_WORLD_BORDERS-0.3.shp")
    out_path = os.path.join(home, "shapefile_out", "TH_MM_border.shp")

    :param to_path:
    :type to_path:
    :param from_path:
    :type from_path:
    :return:
    :rtype:
    """

    shapefile = ogr.Open(from_path)
    layer = shapefile.GetLayer(0)

    thailand = None
    myanmar = None

    for i in range(layer.GetFeatureCount()):

        feature = layer.GetFeature(i)

        if feature.GetField("ISO2") == "TH":
            geometry = feature.GetGeometryRef()
            thailand = shapely.wkt.loads(geometry.ExportToWkt())
        elif feature.GetField("ISO2") == "MM":
            geometry = feature.GetGeometryRef()
            myanmar = shapely.wkt.loads(geometry.ExportToWkt())

    commonBorder = thailand.intersection(myanmar)

    write_shapefile(to_path, commonBorder)

