import logging
import os

import fiona
from shapely.geometry import (
    mapping, shape
)

logger = logging.getLogger(__name__)


# TODO: Optimize: METHOD=ONLY_CC

def get_shapefile_meta(shape_path):
    try:
        with fiona.open(shape_path) as src:

            return src.crs, src.schema, src.driver

    except Exception as e:
        logger.exception(f"Error reading metadata from {shape_path}.", e)
        raise e


def read_shapefile(shapefile_path, validate=False):
    try:
        with fiona.open(shapefile_path) as src:

            layer = os.path.split(shapefile_path)[1]

            for rec in src:

                try:
                    poly = shape(rec['geometry'])
                except Exception as e:
                    logger.exception(f"Error reading geometry: {layer} {rec['properties']}", e)
                    continue

                if validate and not poly.is_valid:
                    logger.warning(f"Cleaning {layer} {rec['properties']}...")

                    clean = poly.buffer(0.0)
                    assert clean.is_valid, 'Invalid Polygon!'
                    assert clean.geom_type in ('MultiPolygon', 'Polygon'), \
                        f'{clean.geom_type} is not a Polygon!'
                    poly = clean
                    rec['geometry'] = mapping(poly)

                yield rec

    except Exception as e:
        logger.exception(f"Error processing {layer}.", e)
        raise e


def split_shapefile(records, crs, schema, shp_out_path, batchsize=10000):
    """
    Reads from iterator. Writes features/attributes to shapefile.
    Return the list of paths.

    References
    - https://shapely.readthedocs.io/en/latest/manual.html#python-geo-interface
    - https://github.com/Toblerity/Fiona/blob/2ec38d087fea72c8bd0e7696d8ac1a6203df8851/examples/with-shapely.py#L22

    :param records:
    :param crs:
    :param schema:
    :param shp_out_path:
    :type shp_out_path:
    :param batchsize:
    :return:
    :rtype:
    """

    try:
        cur_rec, cur_idx = 0, 0
        base_path, shp_file = os.path.split(shp_out_path)
        shp_filename, shp_ext = os.path.splitext(shp_file)
        batch_path = os.path.join(base_path,
                                  f"{shp_filename}_{cur_idx}{shp_ext}")
        batches = [batch_path]

        # Copy the source schema and standardize to polygon to
        # support both polygon and multipolygon in output.
        new_schema = schema.copy()
        new_schema['geometry'] = 'Polygon'

        tgt = fiona.open(batch_path, 'w', driver='ESRI Shapefile',
                         schema=new_schema, crs=crs)

        for rec in records:

            if cur_rec == batchsize:
                tgt.close()
                cur_rec = 0
                cur_idx += 1
                batch_path = os.path.join(base_path,
                                          f"{shp_filename}_{cur_idx}{shp_ext}")
                batches.append(batch_path)

                logger.info(f"Splitting to {os.path.split(batch_path)[1]}...")

                tgt = fiona.open(batch_path, 'w', driver='ESRI Shapefile',
                                 schema=new_schema, crs=crs)

            tgt.write(rec)
            cur_rec += 1

        tgt.close()

        return sorted(batches)

    except Exception as e:
        logger.exception(f"Error writing {shp_out_path}.", e)
        raise e


def write_shapefile(records, crs, schema, shp_out_path):
    """
    Reads from iterator. Writes features/attributes to shapefile.

    References
    - https://shapely.readthedocs.io/en/latest/manual.html#python-geo-interface
    - https://github.com/Toblerity/Fiona/blob/2ec38d087fea72c8bd0e7696d8ac1a6203df8851/examples/with-shapely.py#L22

    :param records:
    :param crs:
    :param schema:
    :param shp_out_path:
    :type shp_out_path:
    :return:
    :rtype:
    """

    try:
        # Copy the source schema and standardize to polygon, seems to
        # support both polygon and multipolygon in output.
        new_schema = schema.copy()
        new_schema['geometry'] = 'Polygon'

        with fiona.open(shp_out_path, 'w', driver='ESRI Shapefile',
                        schema=new_schema, crs=crs) as tgt:

            for rec in records:
                tgt.write(rec)

    except Exception as e:
        logger.exception(f"Error writing {shp_out_path}.", e)
        raise e
