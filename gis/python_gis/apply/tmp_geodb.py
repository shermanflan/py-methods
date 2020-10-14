import logging
import os

import fiona
import geojson
from shapely.geometry import box, mapping, shape

logger = logging.getLogger(__name__)
#logger.setLevel(level=logging.DEBUG)


def load_states(gdb_path, layer, datastore):

    dml = """
    INSERT INTO landgrid.state_us (State_Name, Shape_Length, 
                                   Shape_Area, geobounds, shape)
    VALUES (%s, %s, %s, %s, ST_GeomFromText(%s, 4326));
    """

    with fiona.open(gdb_path, layer=layer) as src:
        try:
            # logger.info(f"Schema: {src.schema}")

            datastore.execute_dml('TRUNCATE TABLE landgrid.state_us;');  # restart

            logger.info(f"Starting load of {len(src)} states...")

            for rec in src:

                poly = shape(rec['geometry'])
                if not poly.is_valid:
                    logger.warning(f"Cleaning {rec['properties']['State_Name']}...")
                    clean = poly.buffer(0.0)
                    assert clean.is_valid
                    assert clean.geom_type == 'MultiPolygon'
                    poly = clean

                bbox = box(*poly.bounds)
                g_json = geojson.dumps(mapping(bbox), sort_keys=True)

                datastore.write_record(dml, (rec['properties']['State_Name'],
                                             rec['properties']['Shape_Length'],
                                             rec['properties']['Shape_Area'],
                                             g_json,
                                             poly.wkt))

                logger.info(f"Processed {rec['id']} of {len(src)}: {rec['properties']['State_Name']}")

            datastore.batch_commit()

            logger.info("Completed state load.")

        except Exception as e:
            # datastore.rollback()
            logger.exception("Error processing States.", e)
            raise e


def load_states_grid(datastore):

    dml2 = """
    INSERT INTO landgrid.state_us_grid (State_Name, shape)
    SELECT 	State_Name, ST_Subdivide(shape, 255) AS grid_shape
    FROM	landgrid.state_us
    ;
    """

    try:

        datastore.execute_dml('TRUNCATE TABLE landgrid.state_us_grid;');  # restart

        # TODO: Consider simplifying as well?
        logger.info("Starting tesselated state load...")

        datastore.execute_dml(dml2, auto_commit=True)
        # datastore.commit()

        logger.info("Completed tesselated state load.")

        # TODO: Rebuild stats
        # VACUUM ANALYZE [table_name] [(column_name)];

    except Exception as e:
        # datastore.rollback()
        logger.exception("Error processing State Grid.", e)
        raise e


def load_counties(gdb_path, layer, datastore):

    dml = """
    INSERT INTO landgrid.county_us (County_Name, State_Name, CountyID, 
                                    StateID, FIPS_State, FIPS_County, 
                                    API_State, API_County, LAT, LON,
                                    Shape_Length, Shape_Area, geobounds, 
                                    shape)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            ST_GeomFromText(%s, 4326));
    """

    with fiona.open(gdb_path, layer=layer) as src:
        try:
            # logger.info(f"Schema: {src.schema}")

            datastore.execute_dml('TRUNCATE TABLE landgrid.county_us;');  # restart

            total = len(src)
            logger.info(f"Starting load of {total} counties...")

            for i, rec in enumerate(src):

                poly = shape(rec['geometry'])
                if not poly.is_valid:
                    logger.warning(f"Cleaning {rec['properties']['County_Name']}...")
                    clean = poly.buffer(0.0)
                    assert clean.is_valid, f"Invalid County {rec['properties']['County_Name']}!"
                    assert clean.geom_type == 'MultiPolygon' or clean.geom_type == 'Polygon', \
                        f'{clean.geom_type} is not a Polygon!'
                    poly = clean

                bbox = box(*poly.bounds)
                g_json = geojson.dumps(mapping(bbox), sort_keys=True)

                datastore.write_record(dml, (rec['properties']['County_Name'],
                                             rec['properties']['State_Name'],
                                             rec['properties']['CountyID'],
                                             rec['properties']['StateID'],
                                             rec['properties']['FIPS_State'],
                                             rec['properties']['FIPS_County'],
                                             rec['properties']['API_State'],
                                             rec['properties']['API_County'],
                                             rec['properties']['LAT'],
                                             rec['properties']['LON'],
                                             rec['properties']['Shape_Length'],
                                             rec['properties']['Shape_Area'],
                                             g_json,
                                             poly.wkt))

                if i % 500 == 0:
                    logger.info(f"{round(i / total * 100, 2)}%: {i} of {total}: {rec['properties']['County_Name']}")

            datastore.batch_commit()
            # cursor.close()

            logger.info("Completed county load.")

        except Exception as e:
            # datastore.rollback()
            logger.exception("Error processing Counties", e)
            raise e


def load_townships(gdb_path, layer_queue, datastore):
    dml = """
    INSERT INTO landgrid.plss_township (TWPCODE, MER, MST, TWP, THALF, 
                                        TNS, RGE, RHALF, REW, /*SecCount,*/ 
                                        TWPLabel, Shape_Length, Shape_Area, 
                                        State_Name, geobounds, shape)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            ST_GeomFromText(%s, 4326));
    """

    try:
        datastore.execute_dml('TRUNCATE TABLE landgrid.plss_township;');  # restart

        for ts in layer_queue:
            with fiona.open(gdb_path, layer=ts.layer) as src:

                total = len(src)
                logger.info(f"Starting load of {ts.layer}: {total} townships...")
                # logger.info(f"Schema: {src.schema}")

                for i, rec in enumerate(src):

                    try:
                        poly = shape(rec['geometry'])
                    except Exception as e:
                        logger.error(f"Error reading {rec['properties']['TWPLabel']}: {rec['geometry']}")
                        logger.exception("Unknown error", e)
                        continue

                    if not poly.is_valid:
                        logger.warning(f"Cleaning {rec['properties']['TWPLabel']} [{ts.layer}]...")

                        clean = poly.buffer(0.0)
                        assert clean.is_valid, 'Invalid Polygon!'
                        assert clean.geom_type == 'MultiPolygon' or clean.geom_type == 'Polygon', \
                            f'{clean.geom_type} is not a Polygon!'
                        poly = clean

                    bbox = box(*poly.bounds)
                    g_json = geojson.dumps(mapping(bbox), sort_keys=True)

                    datastore.write_record(dml, (rec['properties']['TWPCODE'],
                                                 rec['properties']['MER'],
                                                 rec['properties']['MST'],
                                                 rec['properties']['TWP'],
                                                 rec['properties']['THALF'],
                                                 rec['properties']['TNS'],
                                                 rec['properties']['RGE'],
                                                 rec['properties']['RHALF'],
                                                 rec['properties']['REW'],
                                                 # rec['properties']['SecCount'],
                                                 rec['properties']['TWPLabel'],
                                                 rec['properties']['Shape_Length'],
                                                 rec['properties']['Shape_Area'],
                                                 ts.state,  # TMP
                                                 g_json,
                                                 poly.wkt))

                    if i % 500 == 0:
                        logger.info(f"{round(i / total * 100, 2)}%: {i} of {total} [{ts.layer}]")

                datastore.batch_commit()

                logger.info(f"Completed {ts.layer} load.")

    except Exception as e:
        # datastore.rollback()
        logger.exception("Error processing townships.", e)
        raise e


def load_sections(gdb_path, layer_queue, datastore):
    dml = """
    INSERT INTO landgrid.plss_section (StateID, StateAPI, TWPCODE,
                                        SECCODE, MER, MST, TWP, THALF,
                                        TNS, RGE, RHALF, REW, SEC,
                                        Shape_Length, Shape_Area, 
                                        State_Name, geobounds, shape)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, ST_GeomFromText(%s, 4326));
    """

    try:

        datastore.execute_dml('TRUNCATE TABLE landgrid.plss_section;');  # restart

        for ts in layer_queue:
            with fiona.open(gdb_path, layer=ts.layer) as src:

                total = len(src)
                logger.info(f"Starting load of {ts.layer}: {total} sections...")
                # logger.info(f"Schema: {src.schema}")

                for i, rec in enumerate(src):

                    try:
                        poly = shape(rec['geometry'])
                    except Exception as e:
                        logger.error(f"Error reading {rec['properties']['SECCODE']}: {rec['geometry']}")
                        logger.exception("Unknown error", e)
                        continue

                    if not poly.is_valid:
                        logger.warning(f"Cleaning {rec['properties']['SECCODE']} [{ts.layer}]...")

                        clean = poly.buffer(0.0)
                        assert clean.is_valid, 'Invalid Polygon!'
                        assert clean.geom_type == 'MultiPolygon' or clean.geom_type == 'Polygon', \
                            f'{clean.geom_type} is not a Polygon!'
                        poly = clean

                    bbox = box(*poly.bounds)
                    g_json = geojson.dumps(mapping(bbox), sort_keys=True)

                    datastore.write_record(dml, (rec['properties']['StateID'],
                                                 rec['properties']['StateAPI'],
                                                 rec['properties']['TWPCODE'],
                                                 rec['properties']['SECCODE'],
                                                 rec['properties']['MER'],
                                                 rec['properties']['MST'],
                                                 rec['properties']['TWP'],
                                                 rec['properties']['THALF'],
                                                 rec['properties']['TNS'],
                                                 rec['properties']['RGE'],
                                                 rec['properties']['RHALF'],
                                                 rec['properties']['REW'],
                                                 rec['properties']['SEC'],
                                                 rec['properties']['Shape_Length'],
                                                 rec['properties']['Shape_Area'],
                                                 ts.state,  # TMP
                                                 g_json,
                                                 poly.wkt))

                    if i % 5000 == 0:
                        logger.info(f"{round(i / total * 100, 2)}%: {i} of {total} [{ts.layer}]")

                datastore.batch_commit()

                logger.info(f"Completed {ts.layer} load.")

    except Exception as e:
        # datastore.rollback()
        logger.exception(f"Error processing {rec['properties']['SECCODE']}", e)
        raise e


def load_oh_sections(gdb_path, layer, datastore):
    dml = """
    INSERT INTO landgrid.ohio_section (SUBDIV_NM, TWP, TNS, RGE, REW, SEC, 
                                       QTR_TWP, ALLOTMENT, TRACT, LOT, DIVISION, 
                                       FRACTION, COUNTY, TOWNSHIP, SURVEY_TYP, 
                                       ObjectID, VMSLOT, OTHER_SUB, Shape_Length, 
                                       Shape_Area, State_Name, geobounds, shape)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, ST_GeomFromText(%s, 4326));
    """

    try:
        with fiona.open(gdb_path, layer=layer) as src:

            datastore.execute_dml('TRUNCATE TABLE landgrid.ohio_section;');  # restart

            total = len(src)
            logger.info(f"Starting load of {layer}: {total} sections...")
            # logger.info(f"Schema: {src.schema}")

            for i, rec in enumerate(src):

                poly = shape(rec['geometry'])
                if not poly.is_valid:
                    logger.warning(f"Cleaning {rec['properties']['TOWNSHIP']}...")

                    clean = poly.buffer(0.0)
                    assert clean.is_valid, 'Invalid Polygon!'
                    assert clean.geom_type == 'Polygon' or clean.geom_type == 'MultiPolygon', \
                        f'{clean.geom_type} is not a Polygon!'
                    poly = clean

                bbox = box(*poly.bounds)
                g_json = geojson.dumps(mapping(bbox), sort_keys=True)

                datastore.write_record(dml, (rec['properties']['SUBDIV_NM'],
                                             rec['properties']['TWP'],
                                             rec['properties']['TNS'],
                                             rec['properties']['RGE'],
                                             rec['properties']['REW'],
                                             rec['properties']['SEC'],
                                             rec['properties']['QTR_TWP'],
                                             rec['properties']['ALLOTMENT'],
                                             rec['properties']['TRACT'],
                                             rec['properties']['LOT'],
                                             rec['properties']['DIVISION'],
                                             rec['properties']['FRACTION'],
                                             rec['properties']['COUNTY'],
                                             rec['properties']['TOWNSHIP'],
                                             rec['properties']['SURVEY_TYP'],
                                             rec['properties']['ObjectID'],
                                             rec['properties']['VMSLOT'],
                                             rec['properties']['OTHER_SUB'],
                                             rec['properties']['Shape_Length'],
                                             rec['properties']['Shape_Area'],
                                             'Ohio',  # TMP
                                             g_json,
                                             poly.wkt))

                if i % 5000 == 0:
                    logger.info(f"{round(i / total * 100, 2)}%: {i} of {total}: {rec['properties']['TOWNSHIP']}")

            datastore.batch_commit()

            logger.info(f"Completed {layer} load.")

    except Exception as e:
        # datastore.rollback()
        logger.exception("Error processing OH Sections.", e)
        raise e


def load_pa_townships(gdb_path, layer, datastore):

    dml = """
    INSERT INTO landgrid.pa_township (MSLINK, COUNTY, MUNICIPAL_, MUNICIPAL1,
                                      FIPS_MUN_C, FED_AID_UR, FIPS_COUNT,  
                                      FIPS_AREA_, FIPS_NAME, FIPS_SQ_MI,
                                      FIPS_MUN_P, FED_ID_NUM, CLASS_OF_M,
                                      Shape_Length, Shape_Area, County_Name,
                                      County_TOWNSHIP, State_Name, geobounds, 
                                      shape)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, ST_GeomFromText(%s, 4326));
    """

    try:
        with fiona.open(gdb_path, layer=layer) as src:

            datastore.execute_dml('TRUNCATE TABLE landgrid.pa_township;');  # restart

            total = len(src)
            logger.info(f"Starting load of {layer}: {total} sections...")
            # logger.info(f"Schema: {src.schema}")

            for i, rec in enumerate(src):

                poly = shape(rec['geometry'])
                if not poly.is_valid:
                    logger.warning(f"Cleaning {rec['properties']['MUNICIPAL1']}...")

                    clean = poly.buffer(0.0)
                    assert clean.is_valid, 'Invalid Polygon!'
                    assert clean.geom_type == 'Polygon' or clean.geom_type == 'MultiPolygon', \
                        f'{clean.geom_type} is not a Polygon!'
                    poly = clean

                bbox = box(*poly.bounds)
                g_json = geojson.dumps(mapping(bbox), sort_keys=True)

                datastore.write_record(dml, (rec['properties']['MSLINK'],
                                             rec['properties']['COUNTY'],
                                             rec['properties']['MUNICIPAL_'],
                                             rec['properties']['MUNICIPAL1'],
                                             rec['properties']['FIPS_MUN_C'],
                                             rec['properties']['FED_AID_UR'],
                                             rec['properties']['FIPS_COUNT'],
                                             rec['properties']['FIPS_AREA_'],
                                             rec['properties']['FIPS_NAME'],
                                             rec['properties']['FIPS_SQ_MI'],
                                             rec['properties']['FIPS_MUN_P'],
                                             rec['properties']['FED_ID_NUM'],
                                             rec['properties']['CLASS_OF_M'],
                                             rec['properties']['Shape_Length'],
                                             rec['properties']['Shape_Area'],
                                             rec['properties']['County_Name'],
                                             rec['properties']['County_TOWNSHIP'],
                                             'Pennsylvania',  # TMP
                                             g_json,
                                             poly.wkt))

                if i % 5000 == 0:
                    logger.info(f"{round(i / total * 100, 2)}%: {i} of {total}: {rec['properties']['MUNICIPAL1']}")

            datastore.batch_commit()

            logger.info(f"Completed {layer} load.")

    except Exception as e:
        # datastore.rollback()
        logger.exception("Error processing PA Townships.", e)
        raise e


def load_wv_districts(gdb_path, layer, datastore):
    dml = """
    INSERT INTO landgrid.wv_district (WV_ID, DNAME, DNUMBER, CNAME, CNUMBER,
                                      Area_sqm, lat, long, Shape_Length, 
                                      Shape_Area, County_District, 
                                      State_Name, geobounds, shape)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            ST_GeomFromText(%s, 4326));
    """

    try:
        with fiona.open(gdb_path, layer=layer) as src:

            datastore.execute_dml('TRUNCATE TABLE landgrid.wv_district;');  # restart

            total = len(src)
            logger.info(f"Starting load of {layer}: {total} sections...")
            # logger.info(f"Schema: {src.schema}")

            for i, rec in enumerate(src):

                poly = shape(rec['geometry'])
                if not poly.is_valid:
                    logger.warning(f"Cleaning {rec['properties']['DNAME']}...")

                    clean = poly.buffer(0.0)
                    assert clean.is_valid, 'Invalid Polygon!'
                    assert clean.geom_type == 'Polygon' or clean.geom_type == 'MultiPolygon', \
                        f'{clean.geom_type} is not a Polygon!'
                    poly = clean

                bbox = box(*poly.bounds)
                g_json = geojson.dumps(mapping(bbox), sort_keys=True)

                datastore.write_record(dml, (rec['properties']['WV_ID'],
                                             rec['properties']['DNAME'],
                                             rec['properties']['DNUMBER'],
                                             rec['properties']['CNAME'],
                                             rec['properties']['CNUMBER'],
                                             rec['properties']['Area_sqm'],
                                             rec['properties']['lat'],
                                             rec['properties']['long'],
                                             rec['properties']['Shape_Length'],
                                             rec['properties']['Shape_Area'],
                                             rec['properties']['County_District'],
                                             'West Virginia',  # TMP
                                             g_json,
                                             poly.wkt))

                if i % 5000 == 0:
                    logger.info(f"{round(i / total * 100, 2)}%: {i} of {total}: {rec['properties']['DNAME']}")

            datastore.batch_commit()

            logger.info(f"Completed {layer} load.")

    except Exception as e:
        # datastore.rollback()
        logger.exception("Error processing WV Districts.", e)
        raise e


def load_tx_abstracts(gdb_path, layer, datastore):
    dml = """
    INSERT INTO landgrid.tx_abstract (PERIMETER, FIPS, CountyName, 
                                      Shape_Length, Shape_Area, 
                                      AbstractNumber, AbstractName,
                                      Block, Township, Section,
                                      AbstractNameALT, FormNumber,
                                      ControlNumber, State_Name, 
                                      geobounds, shape)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, ST_GeomFromText(%s, 4326));
    """

    try:
        with fiona.open(gdb_path, layer=layer) as src:

            datastore.execute_dml('TRUNCATE TABLE landgrid.tx_abstract;');  # restart

            total = len(src)
            logger.info(f"Starting load of {layer}: {total} abstracts...")
            # logger.info(f"Schema: {src.schema}")

            for i, rec in enumerate(src):

                poly = shape(rec['geometry'])
                if not poly.is_valid:
                    logger.warning(f"Cleaning {rec['properties']['AbstractName']}...")

                    clean = poly.buffer(0.0)
                    assert clean.is_valid, 'Invalid Polygon!'
                    assert clean.geom_type == 'Polygon' or clean.geom_type == 'MultiPolygon', \
                        f'{clean.geom_type} is not a Polygon!'
                    poly = clean

                bbox = box(*poly.bounds)
                g_json = geojson.dumps(mapping(bbox), sort_keys=True)

                datastore.write_record(dml, (rec['properties']['PERIMETER'],
                                             rec['properties']['FIPS'],
                                             rec['properties']['CountyName'],
                                             rec['properties']['Shape_Length'],
                                             rec['properties']['Shape_Area'],
                                             rec['properties']['AbstractNumber'],
                                             rec['properties']['AbstractName'],
                                             rec['properties']['Block'],
                                             rec['properties']['Township'],
                                             rec['properties']['Section'],
                                             rec['properties']['AbstractNameALT'],
                                             rec['properties']['FormNumber'],
                                             rec['properties']['ControlNumber'],
                                             'Texas',  # TMP
                                             g_json,
                                             poly.wkt))

                if i % 5000 == 0:
                    logger.info(f"{round(i / total * 100, 2)}%: {i} of {total}: {rec['properties']['AbstractName']}")

            datastore.batch_commit()

            logger.info(f"Completed {layer} load.")

    except Exception as e:
        # datastore.rollback()
        logger.exception("Error processing Texas Abstracts.", e)
        raise e