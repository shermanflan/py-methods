from datetime import datetime
import logging
import os

from python_gis.poc.landgrid_processor import LandgridProcessor
from python_gis.poc.io.pgsql import PgWriter
from python_gis.poc.io.mssql import MsWriter

import python_gis.poc.util.log_config
# import python_gis.poc.util.log_config

logger = logging.getLogger(__name__)

if __name__ == "__main__":

    # WGS84 (epsg:4326)
    gdb_path = os.path.join(os.environ["DATA_DIR"], 'landgrid',
                            'DI_basemaps_WGS84.gdb')
    ddl_path = os.path.join(os.environ["DIML_HOME"], 'database',
                            'mssql', 'schema.sql')
    dml_path = os.path.join(os.environ["DIML_HOME"], 'database',
                            'mssql', 'validations.sql')
    # idx_path = os.path.join(os.environ["DIML_HOME"], 'database',
    #                         "indexes.sql")
    out_path = os.path.join(os.environ["DATA_DIR"], 'shapefile_out')

    logger.info(f"Starting landgrid processing...")
    start = datetime.now()

    with MsWriter(driver=os.environ["MSSQL_DRIVER"],
                  host=os.environ["MSSQL_SERVER"],
                  db=os.environ["MSSQL_DATABASE"],
                  uid=os.environ["MSSQL_UID"],
                  pwd=os.environ["MSSQL_PWD"]) as db:

        logger.info(f"Creating database schema...")

        db.execute_script(ddl_path, auto_commit=True)  # TODO: add if_exists skip.

        logger.info(f"Running landgrid ETL...")

        landgrid = LandgridProcessor(gdb_path, out_path, db)
        landgrid.to_shapefiles(redo_grid=False)
        landgrid.run_transforms()

        logger.info(f"Running validations...")

        db.execute_script(dml_path, auto_commit=True)

    # with PgWriter(host=os.environ["PG_SERVER"],
    #               database=os.environ["PG_DATABASE"],
    #               user=os.environ["PG_UID"],
    #               password=os.environ["PG_PWD"]) as db:
    #
    #     logger.info(f"Creating database schema...")
    #
    #     db.execute_script(ddl_path, auto_commit=True)  # TODO: add if_exists skip.
    #
    #     logger.info(f"Running landgrid ETL...")
    #
    #     landgrid = LandgridProcessor(gdb_path, out_path, db)
    #     landgrid.to_shapefiles(redo_grid=False)
    #     landgrid.run_transforms()
    #     landgrid.to_datastore()
    #
    #     logger.info(f"Building spatial indexes...")
    #
    #     db.execute_script(idx_path, auto_commit=True)

    elapsed = datetime.now() - start
    logger.info(f"Finished landgrid processing in {elapsed}.")
