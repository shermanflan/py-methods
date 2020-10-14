import logging

import fiona
from shapely.geometry import (
    mapping, shape
)

logger = logging.getLogger(__name__)


def get_gdb_layer_meta(gdb_path, layer):
    try:
        with fiona.open(gdb_path, layer=layer) as src:

            return src.crs, src.schema, src.driver

    except Exception as e:
        logger.exception(f"Error reading metadata from {layer}.", e)
        raise e


# TODO: Use validation.explain_validity to get details on invalid polygons.
# See: https://shapely.readthedocs.io/en/latest/manual.html#diagnostics
def read_gdb_layer(gdb_path, layer, validate=True):
    """

    References
    - https://shapely.readthedocs.io/en/latest/manual.html#python-geo-interface
    - https://github.com/Toblerity/Fiona/blob/2ec38d087fea72c8bd0e7696d8ac1a6203df8851/examples/with-shapely.py#L22

    :param gdb_path:
    :type gdb_path:
    :param layer:
    :type layer:
    :param validate:
    :type validate:
    :return:
    :rtype:
    """
    try:
        with fiona.open(gdb_path, layer=layer) as src:

            for rec in src:

                if validate:

                    try:
                        poly = shape(rec['geometry'])
                    except Exception as e:
                        logger.exception(f"Error reading geometry: {layer} {rec['properties']}", e)
                        continue

                    # NOTE: is_valid is not a static property but evaluates the polygon lazily.
                    if not poly.is_valid:
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


