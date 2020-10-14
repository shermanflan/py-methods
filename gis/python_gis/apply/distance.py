from math import radians, sin, cos, asin, sqrt, atan2, degrees
from collections import deque

import pyproj

# GDAL libraries
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
from osgeo import gdal_array
from osgeo import gdalconst


def get_geodetic_distance(segments, spatial_ref, src_proj, dst_proj, datum="WGS84"):
    """
    Measures distance on the surface of earth (geodetic).
    Handles projected input, Standardizes datum to WGS84.

    :return:
    :rtype:
    """
    geod = pyproj.Geod(ellps=datum)

    totLength = 0.0
    for segment in segments:
        for i in range(len(segment)-1):
            pt1 = segment[i]
            pt2 = segment[i+1]

        long1, lat1 = pt1
        long2, lat2 = pt2

        if spatial_ref.IsProjected():
            long1, lat1 = pyproj.transform(src_proj, dst_proj, long1, lat1)
            long2, lat2 = pyproj.transform(src_proj, dst_proj, long2, lat2)

        angle1, angle2, distance = geod.inv(long1, lat1, long2, lat2)
        totLength += distance

    return totLength


def get_line_segments_from_geometry(input_path, default_datum='WGS84'):
    """
    Inspects input multi-line.
    in_path = os.path.join(home, "shapefile_out", "TH_MM_border.shp")
    Handles projected input, Standardizes datum to WGS84.

    :param input_path:
    :type input_path:
    :return: individual segments
    :rtype:
    """
    shapefile = ogr.Open(input_path)
    layer = shapefile.GetLayer(0)
    spatial_ref = layer.GetSpatialRef()

    if not spatial_ref:
        print(f"Shapefile lacks a spatial reference, using {default_datum}.")
        spatial_ref = osr.SpatialReference()
        spatial_ref.SetWellKnownGeogCS(default_datum)

    src_proj = dst_proj = None
    if spatial_ref.IsProjected():
        src_proj = pyproj.Proj(spatial_ref.ExportToProj4())
        dst_proj = pyproj.Proj(proj='longlat', ellps='WGS84', datum='WGS84')
    else:
        print("Non projected input.")

    feature = layer.GetFeature(0)
    geometry = feature.GetGeometryRef()

    segments = []
    queue = deque()
    queue.append(geometry)

    while queue:

        tmp_geometry = queue.popleft()

        if tmp_geometry.GetPointCount() > 0:
            segment = []
            for i in range(tmp_geometry.GetPointCount()):
                segment.append(tmp_geometry.GetPoint_2D(i))
            segments.append(segment)

        for i in range(tmp_geometry.GetGeometryCount()):
            subGeometry = tmp_geometry.GetGeometryRef(i)
            queue.append(subGeometry)

    return segments, spatial_ref, src_proj, dst_proj


def haversine(point1, point2):
    """
    Haversine great-circle distance formula. Decimal degrees
    Usage: haversine((-90.21, 32.31), (-88.95, 30.43)))

    :param point1: lat, lon
    :type point1: Tuple
    :param point2:
    :type point2:
    :return:
    :rtype:
    """
    x1, y1 = point1
    x2, y2 = point2
    x_dist = radians(x1 - x2)
    y_dist = radians(y1 - y2)
    y1_rad = radians(y1)
    y2_rad = radians(y2)
    a = sin(y_dist/2)**2 + sin(x_dist/2)**2 * cos(y1_rad) * cos(y2_rad)
    c = 2 * asin(sqrt(a))
    return c * 6371  # kilometers


def euclidean(point1, point2):
    """
    Pythagorean theorem. Cartesian coordinates

    :param point1:
    :type point1:
    :param point2:
    :type point2:
    :return:
    :rtype:
    """
    x1, y1 = point1
    x2, y2 = point2
    x_dist = x1 - x2
    y_dist = y1 - y2
    dist_sq = x_dist ** 2 + y_dist ** 2
    return sqrt(dist_sq)


# TODO:
def vincenty(point1, point2):
    raise NotImplementedError("Most accurate distance measurement.")


def forward_azimuth(point1, point2):
    """
    Initial bearing between 2 points (a.k.a forward azimuth).
    Decimal degrees (lon, lat).
    http://www.movable-type.co.uk/scripts/latlong.html

    Usage: forward_azimuth((-90.21, 32.31), (-88.95, 30.43))

    :return:
    :rtype:
    """
    lon1, lat1 = point1
    lon2, lat2 = point2

    angle = atan2(cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(lon2 - lon1),
                  sin(lon2 - lon1) * cos(lat2))

    bearing = (degrees(angle) + 360) % 360

    return bearing
