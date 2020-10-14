import os

import psycopg2
import shapefile  # from pyshp
import fiona
from shapely.geometry import shape, Point, Polygon
from shapely.wkb import loads

# GDAL libraries
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
from osgeo import gdal_array
from osgeo import gdalconst

"""
TODO:
Consider ST_Subdivide to denormalize large polygons (States, Countries)
for more efficient indexing.
http://postgis.net/docs/using_postgis_dbmanagement.html#idm1618

Consider using Postgis utilities:
shp2pgsql (from shapefile)
pgsql2shp (to shapefile)
"""


def load_shapefile(src_path, pg_host, pg_db, pg_user, pg_pwd):

    connection = psycopg2.connect(host=pg_host, database=pg_db, user=pg_user, password=pg_pwd)
    cursor = connection.cursor()

    ddl = """
    DROP TABLE IF EXISTS public.borders;
    
    CREATE TABLE public.borders 
    (
        id          SERIAL      NOT NULL
            PRIMARY KEY,
        name        VARCHAR     NOT NULL,
        iso_code    VARCHAR     NOT NULL,
        outline     GEOGRAPHY   NOT NULL
    );
    
    CREATE INDEX border_index 
        ON public.borders 
    USING GIST(outline);
    """

    dml = """
        INSERT INTO public.borders (name, iso_code, outline) 
        VALUES (%s, %s, ST_GeogFromText(%s))
    """

    cursor.execute(ddl)
    connection.commit()

    shapefile = ogr.Open(src_path)
    layer = shapefile.GetLayer(0)

    for i in range(layer.GetFeatureCount()):
        feature = layer.GetFeature(i)
        name = feature.GetField("NAME")
        iso_code = feature.GetField("ISO3")
        geometry = feature.GetGeometryRef()
        wkt = geometry.ExportToWkt()

        cursor.execute(dml, (name, iso_code, wkt))

    connection.commit()


def load_geometry(path, pg_host, pg_db, pg_user, pg_pwd):
    """
    Another example loading from shapefile with points in WGS84.

    :return:
    :rtype:
    """

    ddl = """
    DROP TABLE IF EXISTS public.nyc_museums;

    CREATE TABLE public.nyc_museums
    (
        id          SERIAL                  NOT NULL 
            PRIMARY KEY, 
        NAME        VARCHAR(255)            NULL,
        URL         VARCHAR(255)            NULL,
        location    GEOMETRY(POINT, 4326)   NULL
        --TODO: Use below to store any kind of geometry
        --location    GEOMETRY(GEOMETRY, 4326)   NULL
        --location    GEOGRAPHY(POINT, 4326)   NULL
    );

    CREATE INDEX nyc_museums_points_gix 
        ON public.nyc_museums 
    USING GIST (location);
    """

    with psycopg2.connect(host=pg_host, database=pg_db, user=pg_user, password=pg_pwd) as c, \
            shapefile.Reader(path) as shp_reader:

        try:
            # Execute DDL
            cursor = c.cursor()
            cursor.execute(ddl)
            c.commit()

            # Execute DML
            cursor = c.cursor()

            dml = """
            INSERT INTO public.nyc_museums (NAME, URL, location)
            VALUES (%s, %s, ST_GeomFromText(%s, 4326))
            """

            # Read both attributes and geometries.
            for srec in shp_reader.shapeRecords():
                pt = Point(srec.shape.points[0][0], srec.shape.points[0][1])
                cursor.execute(dml, (srec.record['NAME'], srec.record['URL'], pt.wkt))

            c.commit()

        except Exception as e:
            c.rollback()
            raise e


def read_geometry(pg_host, pg_db, pg_user, pg_pwd):
    dml = """
    SELECT id
    		, name
    		, url
    		, location 
    FROM	public.nyc_museums
    LIMIT 10;
    """

    with psycopg2.connect(host=pg_host, database=pg_db, user=pg_user, password=pg_pwd) as c:
        cursor = c.cursor()

        cursor.execute(dml)

        for rec in cursor.fetchall():
            pt = loads(rec[3], hex=True)
            print(pt)


def load_polygons(pg_host, pg_db, pg_user, pg_pwd):
    """
    Uses pyshp to load shapefile.

    :param pg_host:
    :type pg_host:
    :param pg_db:
    :type pg_db:
    :param pg_user:
    :type pg_user:
    :param pg_pwd:
    :type pg_pwd:
    :return:
    :rtype:
    """
    ddl = """
    DROP TABLE IF EXISTS public.us_states;

    CREATE TABLE public.us_states
    (
        id SERIAL NOT NULL 
            PRIMARY KEY, 
        NAME VARCHAR(100) NULL,
        CODE CHAR(2) NULL,
        ABBREV CHAR(2) NULL,
        AREA BIGINT NULL,
        -- NAD 83
        -- Can be MultiPolygon. Handle both by using GEOMETRY.
        location    GEOMETRY(GEOMETRY, 4269)   NULL
    );

    CREATE INDEX us_states_poly_gix 
    ON public.us_states
    USING GIST (location);
    """
    # NAD83 and contains both Polygon and MultiPolygon types.
    shp_path = os.path.join(os.environ["DATA_DIR"], 'us_states', 'tl_2014_us_state.shp')

    with psycopg2.connect(host=pg_host, database=pg_db, user=pg_user, password=pg_pwd) as c, \
            shapefile.Reader(shp_path) as shp:

        try:
            # Execute DDL
            cursor = c.cursor()
            cursor.execute(ddl)
            c.commit()

            # Execute DML
            cursor = c.cursor()

            dml = """
            INSERT INTO public.us_states (NAME, CODE, ABBREV, AREA, location)
            VALUES (%s, %s, %s, %s, ST_GeomFromText(%s, 4269))
            """

            # Read both attributes and geometries.
            # TODO: Can also import as binary, hex-encoded for PostGIS using:
            # [shape].wkb.encode('hex')
            # May be more efficient?
            for srec in shp.shapeRecords()[:5]:
                poly = Polygon(srec.shape.points)
                cursor.execute(dml, (srec.record['NAME'], srec.record['STATEFP'],
                                     srec.record['STUSPS'], srec.record['ALAND'], poly.wkt))

            c.commit()

        except Exception as e:
            c.rollback()
            raise e


# TODO: Add struct logging
def load_polygons_fiona(gdb_path, pg_host, pg_db, pg_user, pg_pwd):
    """
    Same as above but using Fiona to load from a file GDB.

    Usage: below GDB uses WGS84 (epsg:4326)
    gdb_path = os.path.join(os.environ["DATA_DIR"], 'landgrid', 'DI_basemaps_WGS84.gdb')

    :param pg_host:
    :type pg_host:
    :param pg_db:
    :type pg_db:
    :param pg_user:
    :type pg_user:
    :param pg_pwd:
    :type pg_pwd:
    :return:
    :rtype:
    """
    ddl = """
    DROP TABLE IF EXISTS public.states_us;
    DROP TABLE IF EXISTS public.ok_township;

    CREATE TABLE public.states_us
    (
        id             SERIAL                         NOT NULL 
            PRIMARY KEY, 
        state_name     VARCHAR(50)                    NULL,
        shape_length   REAL                           NULL,
        shape_area     REAL                           NULL,
        shape          GEOMETRY(MULTIPOLYGON, 4326)   NULL
    );

    CREATE INDEX states_us_polys_gix 
        ON public.states_us 
    USING GIST (shape);

    CREATE TABLE public.ok_township
    (
        id             SERIAL                         NOT NULL 
            PRIMARY KEY, 
        twpcode        VARCHAR(24)                    NULL,
        mer            VARCHAR(5)                     NULL,
        mst            VARCHAR(20)                    NULL,
        twp            INTEGER                        NULL,
        thalf          INTEGER                        NULL,
        tns            CHAR(1)                        NULL,
        rge            INTEGER                        NULL,
        rhalf          INTEGER                        NULL,
        rew            CHAR(1)                        NULL,
        seccount       INTEGER                        NULL,
        twplabel       VARCHAR(20)                    NULL,    
        shape_length   REAL                           NULL,
        shape_area     REAL                           NULL,
        -- Support both Polygon and MultiPolygon
        shape          GEOMETRY(GEOMETRY, 4326)       NULL
    );

    CREATE INDEX ok_township_polys_gix 
        ON public.ok_township
    USING GIST (shape);

    """

    with psycopg2.connect(host=pg_host, database=pg_db, user=pg_user, password=pg_pwd) as c:

        try:
            # Execute DDL
            cursor = c.cursor()
            cursor.execute(ddl)
            c.commit()

        except Exception as e:
            c.rollback()
            raise e

    print("DDL Completed.")

    dml = """
    INSERT INTO public.ok_township (twpcode, mer, mst, twp, thalf, 
                                    tns, rge, rhalf, rew, seccount, 
                                    twplabel, shape_length, shape_area, 
                                    shape)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            ST_GeomFromText(%s, 4326));
    """

    with psycopg2.connect(host=pg_host, database=pg_db, user=pg_user, password=pg_pwd) as db, \
            fiona.open(gdb_path, layer='OK_township') as shape_iter:
        try:

            cursor = db.cursor()

            print(f"Starting load of {len(shape_iter)} townships...")

            for rec in shape_iter:

                poly = shape(rec['geometry'])
                if not poly.is_valid:
                    clean = poly.buffer(0.0)
                    assert clean.is_valid, 'Invalid Polygon!'
                    assert clean.geom_type == 'MultiPolygon' or clean.geom_type == 'Polygon', \
                        f'{clean.geom_type} is not a Polygon!'
                    poly = clean

                # TODO: Can also import as binary, hex-encoded for PostGIS using:
                # [shape].wkb.encode('hex')
                # May be more efficient?
                cursor.execute(dml, (rec['properties']['TWPCODE'],
                                     rec['properties']['MER'],
                                     rec['properties']['MST'],
                                     rec['properties']['TWP'],
                                     rec['properties']['THALF'],
                                     rec['properties']['TNS'],
                                     rec['properties']['RGE'],
                                     rec['properties']['RHALF'],
                                     rec['properties']['REW'],
                                     rec['properties']['SecCount'],
                                     rec['properties']['TWPLabel'],
                                     rec['properties']['Shape_Length'],
                                     rec['properties']['Shape_Area'],
                                     poly.wkt))

                print(f"Processed {rec['id']} of {len(shape_iter)}: {rec['properties']['TWPLabel']}")

            c.commit()

        except Exception as e:
            c.rollback()
            raise e

    print("DML Completed.")