import pyproj

"""
The difference between using PROJ.4 separately instead of using it with a package 
such as GDAL is that it enables you to re-project individual points, and packages 
using PROJ.4 do not offer this functionality.
"""


def hello():
    print(pyproj.__version__)


def get_distance(point1, point2):
    geod = pyproj.Geod(ellps="WGS84")
    angle1, angle2, distance = geod.inv(point1[1], point1[0], point2[1], point2[0])

    return distance


def to_latlon(UTM_X, UTM_Y):
    """
    Go from UTM coordinates to lat/lon
    :return:
    :rtype:
    """
    srcProj = pyproj.Proj(proj="utm", zone="11", ellps="clrk66", units="m")
    dstProj = pyproj.Proj(proj='longlat', ellps='WGS84', datum='WGS84')

    long, lat = pyproj.transform(srcProj, dstProj, UTM_X, UTM_Y)

    print("UTM zone 17 coordinate " +
          "({:.4f}, {:.4f}) ".format(UTM_X, UTM_Y) +
          "= {:.4f}, {:.4f}".format(long, lat))


def to_distance(lat, long, distance, angle):
    """
    Calculates a point x distance, y angle forward.

    :return:
    :rtype:
    """
    geod = pyproj.Geod(ellps='clrk66')
    long2, lat2, invAngle = geod.fwd(long, lat, angle, distance)

    print("{:.4f}, {:.4f}".format(lat2, long2) +
          " is 10km northeast of " +
          "{:.4f}, {:.4f}".format(lat, long))


def re_project(shape):

    proj_4326 = Proj('epsg:4326')
    proj_3832 = Proj('epsg:3832')
    project_to = Transformer.from_proj(proj_4326,  # source coordinate system
                                       proj_3832  # destination coordinate system
                                       ).transform
    project_back = Transformer.from_proj(proj_3832,  # source coordinate system
                                         proj_4326  # destination coordinate system
                                         ).transform

    # This matches existing bounding box but still spans the world.
    shape_3832 = transform(project_to, shape)
    bbox_3832 = shape_3832.envelope
    bbox = transform(project_back, bbox_3832)

    return bbox
