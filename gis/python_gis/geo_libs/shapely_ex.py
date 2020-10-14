import json
from pprint import pprint

import fiona
import shapely
import shapely.speedups
import shapely.wkt
from shapely.geometry import (
    Polygon, Point, LineString, LinearRing,
    MultiPoint, MultiLineString, MultiPolygon,
    mapping, shape
)

"""
Shapely is a Python package for manipulation and analysis of planar features, 
using functions from the GEOS library (the engine of PostGIS) and a port of the JTS.

The difference between Shapely and OGR is that Shapely has a more Pythonic and very 
intuitive interface, is better optimized, and has well-developed documentation.
"""


def meta():
    print(shapely.__version__)
    print(shapely.speedups.available)


def process_shapefile(shp_path):
    """
    Usage: this shapefile is in WGS84
    shp_path = os.path.join(os.environ["DATA_DIR"], 'countries', 'TM_WORLD_BORDERS-0.3.shp')

    :param shp_path:
    :type shp_path:
    :return:
    :rtype:
    """

    shapes = []
    with fiona.open(shp_path) as c_iter:
        for rec in c_iter[:5]:
            pprint(f"Type: {rec['type']}")
            pprint(f"ID: {rec['id']}")
            pprint(rec['properties'])
            pprint(rec['geometry'])

            # Load as shape or inspect rec['geometry']['type']
            print(f"Shape Type: {rec['geometry']['type']}")
            state = shape(rec['geometry'])
            shapes.append(state)

            # TODO: Can load to spatial db from here as state.wkt or state.wkb
            # See psycho_ex.py

    return shapes


def from_geojson(g_json):
    """
    Usage:
    g_json = '{"type": "Polygon", "coordinates": [[[1,1], [1,3 ], [3,3]]]}'

    :param g_json:
    :type g_json:
    :return:
    :rtype:
    """
    p = shape(json.loads(g_json))  # from geojson
    print(json.dumps(mapping(p)))  # to geojson

    print(p.area)

    return p


def create_geometries():
    p1 = Polygon(((1, 2), (5, 3), (5, 7), (1, 9), (1, 2)))

    print(p1.area)
    print(p1.bounds)
    print(p1.length)
    print(p1.geom_type)

    p2 = Polygon(((6, 6), (7, 6), (10, 4), (11, 8), (6, 6)))

    q = Point((2.0, 2.0))
    line = LineString([(0, 0), (10, 10)])
    ring = LinearRing([(0, 0), (3, 3), (3, 0)])
    points = MultiPoint([(0.0, 0.0), (3.0, 3.0)])
    lines = MultiLineString([((0, 0), (1, 1)), ((-1, 0), (1, 0))])
    polygons = MultiPolygon([p1, p2, ])


# TODO: Creative use of the buffering method provides ways to clean shapes.
# TODO: Use shapely.prepared.prep for efficient batch operations
# contains, intersects, etc.
# See: https://shapely.readthedocs.io/en/latest/manual.html#prepared-geometry-operations
def get_intersect():
    """
    Calculate intersection of circle and square.

    :return:
    :rtype:
    """
    pt = Point(0, 0)
    circle = pt.buffer(1.0)
    square = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])

    new_intersect = circle.intersection(square)

    for x, y in new_intersect.exterior.coords:
        print(x, y)
    print(shapely.wkt.dumps(new_intersect))

