import logging

import geopandas as gpd
import pandas as pd
from shapely.geometry import (
    LineString, Polygon, MultiPolygon
)
from shapely.ops import (
    split as shapely_split, transform
)

logger = logging.getLogger(__name__)

MAX_DEPTH = 50


# TODO: Use a queue and implement iteratively?
def sub_divide(poly, geobag, max_vertices=255, depth=0):
    """
    Subdivides a given polygon so that each part has less than max_vertices.
    Based on postgis' ST_SUBDIVIDE implementation.

    References:
    - https://snorfalorpagus.net/blog/2016/03/13/splitting-large-polygons-for-faster-intersections/
    - https://github.com/postgis/postgis/blob/570fbdb10de728e56957f3b7b449ac9532a53a47/liblwgeom/lwgeom.c#L2268

    To Do:
    - Reuse existing points on polygon split
    - Handle polygon interiors (may not need to change much as Shapely's split
    may handle interiors automatically - review source)
    - Handle non-polygon geometries

    :param poly:
    :param geobag:
    :param max_vertices:
    :param depth:
    :return:
    """
    assert poly.geom_type in ('Polygon', 'MultiPolygon'), \
        f"Unsupported geometry type: {poly.geom_type}"

    if poly.geom_type == 'MultiPolygon':
        for part in poly.geoms:
            sub_divide(part, geobag, max_vertices, depth)
        return

    if len(poly.interiors) > 0:
        raise NotImplementedError("Polygons with interiors not supported.")

    if depth > MAX_DEPTH:  # max recursions reached
        geobag.append(poly)
        return

    num_vertex = len(poly.exterior.coords)

    if num_vertex <= max_vertices:  # vertex threshold reached
        geobag.append(poly)
        return

    xmin, ymin, xmax, ymax = poly.bounds
    width, height = xmax - xmin, ymax - ymin

    split_ew = True if width > height else False
    center = (xmin + xmax)/2 if split_ew else (ymin + ymax)/2

    if split_ew:  # split left to right
        meridian = LineString([(center, ymin), (center, ymax)])
    else:
        meridian = LineString([(xmin, center), (xmax, center)])

    halves = shapely_split(poly, meridian)

    for half in halves:
        sub_divide(half, geobag, max_vertices, depth + 1)

    return


def remove_holes(poly):
    assert poly.geom_type in ('Polygon', 'MultiPolygon'), \
        f"Unsupported geometry type: {poly.geom_type}"

    if poly.geom_type == 'Polygon' and len(poly.interiors) > 0:
        poly = Polygon(poly.exterior)

        logger.info(f'Removed hole from Polygon: {len(poly.interiors)}')

    elif poly.geom_type == 'MultiPolygon':
        polys = []
        for ring in poly.geoms:
            if len(ring.interiors) > 0:
                tmp_poly = Polygon(ring.exterior)
                polys.append(tmp_poly)

                logger.info(f'Removed hole from MultiPolygon: {len(tmp_poly.interiors)}')
            else:
                polys.append(ring)

        poly = MultiPolygon(polys)

    return poly


def de_aggregate(poly_df):

    # Get multipolygons
    mpoly_df = (poly_df
                .loc[poly_df.geometry.geom_type == 'MultiPolygon', :]
                .copy())

    # Split list of geometries into DataFrame columns
    to_columns_df = pd.DataFrame(mpoly_df.geometry.tolist(),
                                 index=mpoly_df.index)

    # Save original index values
    to_columns_df['id'] = to_columns_df.index

    # Melt (convert columns to rows)
    to_columns_df = to_columns_df.melt(id_vars='id', value_name='Unity')

    # Remove empty values
    to_columns_df.dropna(subset=['Unity'], inplace=True)
    to_columns_df.set_index('id', inplace=True)

    # Join with original dissolved data set
    df_deagg = poly_df.join(to_columns_df, how='left')  #.copy()
    df_deagg.loc[df_deagg.geometry.geom_type == 'MultiPolygon', ['geometry']] = \
        df_deagg[df_deagg.geometry.geom_type == 'MultiPolygon'].Unity

    df_deagg.drop(columns=['variable', 'Unity'], inplace=True)

    # Each polygon is now unique so resetting index.
    df_deagg.reset_index(inplace=True, drop=True)

    return df_deagg


def get_overlaps(parent_df, child_df, label, grouping_column):

    olaps_df = gpd.sjoin(child_df, parent_df, how='inner', op='intersects')
    # olaps_df.loc[olaps_df[grouping_column].isna(), [grouping_column]] = 'Unknown'  # null join

    olaps_pre_df = (olaps_df.loc[:, [grouping_column]]
                    .reset_index()
                    .drop_duplicates()  # remove duplicate names
                    .set_index('index')
                    )

    olaps_join_df = (olaps_pre_df
                     .groupby(olaps_pre_df.index, sort=False)
                     .aggregate(**{label: (grouping_column, ','.join)})  # Pandas 0.25
                     )

    olap_df = child_df.join(olaps_join_df, how='left')

    return olap_df


# Meridian, Anti-Meridian operations
WEST_MERIDIAN = LineString([(-180, 90), (-180, -90)])


def shift_west(x, y, z=None):
    """
    Shift to west hemisphere.

    :param x:
    :param y:
    :param z:
    :return:
    """
    return tuple(filter(None, ((x - 360)%-360, y, z)))


def unshift_west(x, y, z=None):
    """
    Shift back to east hemisphere.

    :param x:
    :param y:
    :param z:
    :return:
    """
    return tuple(filter(None, ((x + 360), y, z)))


def shift_east(x, y, z=None):
    """
    Shift to east hemisphere.

    :param x:
    :param y:
    :param z:
    :return:
    """
    return tuple(filter(None, ((x + 360)%360, y, z)))


def unshift_east(x, y, z=None):
    """
    Shift back to west hemisphere.

    :param x:
    :param y:
    :param z:
    :return:
    """
    return tuple(filter(None, ((x - 360), y, z)))


def is_near_idl(x):
    """
    International dateline check.

    :param x: longitude
    :return:
    """
    return x < -150 or x > 150


def fix_anti_meridian(poly):
    """
    Check for anti-meridian and split polygon if necessary,
    keeping the right side.

    :param poly:
    :return:
    """

    min_x, _, max_x, _ = poly.bounds

    if is_near_idl(min_x) or is_near_idl(max_x):
        shape_shift = transform(shift_west, poly)
        shape_envelope = shape_shift.envelope

        if shape_envelope.intersects(WEST_MERIDIAN):

            logger.info(f"Polygon crosses IDL: {poly.bounds}.")

            _, right_half = shapely_split(shape_envelope, WEST_MERIDIAN)
            min_x, _, max_x, _ = right_half.envelope.bounds

            # Shift back to the east hemisphere.
            if min_x < -180 or max_x < -180:  # check west hemi
                right_half = transform(unshift_west, right_half.envelope)

            return right_half

    return poly

