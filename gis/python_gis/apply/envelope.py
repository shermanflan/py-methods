import shapely.wkt
import shapely.geometry

# GDAL libraries
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
from osgeo import gdal_array
from osgeo import gdalconst


# TODO: Exclude islands.
# Split each country's MultiPolygon into individual Polygon objects and then
# check the area of each polygon to exclude those that are smaller than a given
# total value.
def get_bounding_box(path):
    """
    Calculate polygon's bounding box.
    path = os.path.join(home, "countries", "TM_WORLD_BORDERS-0.3.shp")

    :return:
    :rtype:
    """
    shapefile = ogr.Open(path)
    layer = shapefile.GetLayer(0)

    # List of (code, name, minLat, maxLat, minLong, maxLong).
    countries = []

    for i in range(layer.GetFeatureCount()):
        feature = layer.GetFeature(i)

        countryCode = feature.GetField("ISO3")
        countryName = feature.GetField("NAME")

        shape = feature.GetGeometryRef()

        minLong, maxLong, minLat, maxLat = shape.GetEnvelope()
        countries.append((countryName, countryCode, minLat, maxLat, minLong, maxLong))

    for name, code, minLat, maxLat, minLong, maxLong in countries[:5]:
        print(f"{name} ({code}) lat={minLat:.4f}..{maxLat:.4f},long={minLong:.4f}..{maxLong:.4f}")

    print(f"Country Count: {len(countries)}")
    return countries


# TODO: Use similar pattern with:
# shapely.geometry.buffer(0.0): removes bowties in polygons
# shapely.geometry.simplify(0): removes repeat points (smooths complex shapes)
def write_centroids(src_path, dst_path, datum='WGS84'):
    """
    Use Shapely to calculate centroid. Output a shapefile with the points.
    in_path = os.path.join(home, "countries", "TM_WORLD_BORDERS-0.3.shp")
    dst_path = os.path.join(home, "shapefile_out", "TM_WORLD_BORDERS-centroids.shp")

    :param src_path:
    :type src_path:
    :param dst_path:
    :type dst_path:
    :param datum:
    :type datum:
    :return:
    :rtype:
    """
    src_shapefile = ogr.Open(src_path)
    src_layer = src_shapefile.GetLayer(0)

    driver = ogr.GetDriverByName("ESRI Shapefile")
    dst_shapefile = driver.CreateDataSource(dst_path)

    spatial_ref = osr.SpatialReference()
    spatial_ref.SetWellKnownGeogCS(datum)
    dst_layer = dst_shapefile.CreateLayer("centroids", spatial_ref)

    field = ogr.FieldDefn("ID", ogr.OFTInteger)
    field.SetWidth(4)
    dst_layer.CreateField(field)

    field = ogr.FieldDefn("ISO3", ogr.OFTString)
    field.SetWidth(3)
    dst_layer.CreateField(field)

    field = ogr.FieldDefn("NAME", ogr.OFTString)
    field.SetWidth(4)
    dst_layer.CreateField(field)

    centroids = []

    for i in range(src_layer.GetFeatureCount()):
        feature = src_layer.GetFeature(i)

        country_code = feature.GetField("ISO3")
        country_name = feature.GetField("NAME")
        shape = feature.GetGeometryRef()

        # Convert to shapely geometry
        country_shape = shapely.wkt.loads(shape.ExportToWkt())
        centroid_wkt = shapely.wkt.dumps(country_shape.centroid)
        centroids.append(centroid_wkt)

        feature = ogr.Feature(dst_layer.GetLayerDefn())
        feature.SetField("ID", i)
        feature.SetField("ISO3", country_code)
        feature.SetField("NAME", country_name)
        geometry = ogr.CreateGeometryFromWkt(centroid_wkt)
        feature.SetGeometry(geometry)

        dst_layer.CreateFeature(feature)

        # Close feature
        feature.Destroy()  # or feature = None

    # Close file handle
    dst_shapefile.FlushCache()
    dst_shapefile.Destroy()  # or dst_shapefile = None

    return centroids
