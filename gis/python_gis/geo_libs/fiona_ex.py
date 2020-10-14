import os
import pprint

import geojson
import fiona
from shapely.geometry import mapping, shape, box


"""
Fiona is the API of OGR. It can be used for reading and writing data formats. 
The main reason for using it instead of OGR is that it's closer to Python 
than OGR as well as more dependable and less error-prone. However, it may be
less memory-efficient.

You can use Fiona for input and output, and Shapely for creating and 
manipulating geospatial data. (Fiona > Shapely > Target)
"""


def read_shapefile(shp_path):
    """
    This uses an iterator to loop through the shapefile records. This
    may be more efficient than reading all to memory (i.e. geopandas).

    Usage:
    shp_path = os.path.join(os.environ["DATA_DIR"], 'countries', 'TM_WORLD_BORDERS-0.3.shp')

    :param shp_path:
    :type shp_path:
    :return:
    :rtype:
    """
    with fiona.open(shp_path) as c_iter:
        print(f"Driver: {c_iter.driver}, CRS: {c_iter.crs}")
        print(f"Num Records: {len(c_iter)}")

        rec = next(iter(c_iter))
        pprint.pprint(rec.keys())
        pprint.pprint(rec['type'])
        pprint.pprint(rec['id'])
        pprint.pprint(rec['properties'])
        pprint.pprint(rec['geometry'])

        # for rec in c_iter:
        #     pprint.pprint(rec['type'])
        #     pprint.pprint(rec['id'])
        #     pprint.pprint(rec['properties'])
        #     pprint.pprint(rec['geometry'])

        # Can also access by index (is this standard for iterators?)
        pprint.pprint(f"Access by index: {c_iter[21]}")


def read_geodatabase(dir_path, layer_name):
    """
    Usage:
    The following is in WGS84
    dir_path = os.path.join(os.environ["DATA_DIR"], 'landgrid', 'DI_basemaps_WGS84.gdb')

    :param dir_path:
    :type dir_path:
    :param layer_name:
    :type layer_name:
    :return:
    :rtype:
    """
    # List layers in GDB
    for name in fiona.listlayers(dir_path):
        print(name)

    # Read layer
    with fiona.open(dir_path, layer='States_US') as c_iter:
        print(f"Driver: {c_iter.driver}, CRS: {c_iter.crs}")
        print(f"Num Records: {len(c_iter)}")
        pprint(f"SCHEMA: {c_iter.schema}")

        rec = next(iter(c_iter))
        pprint(rec.keys())
        pprint(rec['type'])
        pprint(rec['id'])
        pprint(rec['properties'])
        pprint(rec['geometry'])

        # for rec in c_iter:
        #     pprint(rec['type'])
        #     pprint(rec['id'])
        #     pprint(rec['properties'])
        #     pprint(rec['geometry'])


def write_shapefile(gdb_src_path, shp_out_path):
    """
    Reads from GDB. Converts shapes to bounding boxes and also generates
    GeoJSON.

    Usage:
    # WGS84 (epsg:4326)
    gdb_src_path = os.path.join(os.environ["DATA_DIR"], 'landgrid', 'DI_basemaps_WGS84.gdb')
    shp_out_path = os.path.join(os.environ["DATA_DIR"], 'shapefile_out', 'test_fiona.shp')

    :param gdb_src_path:
    :type gdb_src_path:
    :param shp_out_path:
    :type shp_out_path:
    :return:
    :rtype:
    """
    with fiona.open(gdb_src_path, layer='States_US') as src:
        print(f"Driver: {src.driver}, CRS: {src.crs}")

        # Copy the source schema and add a property.
        schema = src.schema.copy()
        schema['properties']['new_prop'] = 'int'  # new
        schema['geometry'] = 'Polygon'  # update
        print(f"Schema: {schema}")

        with fiona.open(shp_out_path, 'w', driver='ESRI Shapefile',
                        schema=schema, crs=src.crs) as tgt:

            i = 0
            for f in src:
                # print(f"Coordinates: {f['geometry']['coordinates']}")

                # See https://shapely.readthedocs.io/en/latest/manual.html#python-geo-interface
                state = shape(f['geometry'])
                print(f"Type: {f['geometry']['type']}, State: {f['properties']['State_Name']}")
                # print(f"Bounds: {state.bounds}")

                if not state.is_valid:
                    clean_state = state.buffer(0.0)
                    assert clean_state.is_valid
                    assert clean_state.geom_type == 'MultiPolygon'
                    state = clean_state

                bbox = box(*state.bounds)

                # Writes as python-geo-interface (GeoJSON-like)
                f['geometry'] = mapping(bbox)
                pprint(f"Geometry: {f['geometry']}")

                # Create GeoJSON representation.
                pprint(f"GeoJSON: {geojson.dumps(f['geometry'], sort_keys=True)}")
                f['properties'].update(new_prop=i)
                i += 1

                tgt.write(f)


