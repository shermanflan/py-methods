import logging

import pandas as pd

from parquet_util import (
    ACCOUNT_KEY, ACCOUNT_NAME, CONTAINER_NAME,
    SQL_HOST, SQL_DB, SQL_USER, SQL_PASSWORD,
    SQL_DRIVER
)
from parquet_util.api.blob import AzureBlobHook
from parquet_util.api.db import SQLHook
from parquet_util.api.parquet import load_dataset
import parquet_util.log

logger = logging.getLogger(__name__)


def import_datasets(output_folder):

    blob_service = AzureBlobHook(account_name=ACCOUNT_NAME,
                                 account_key=ACCOUNT_KEY)
    sql_service = SQLHook(host=SQL_HOST, db=SQL_DB,
                          user=SQL_USER, password=SQL_PASSWORD,
                          driver=SQL_DRIVER)

    logger.info(f"Importing Kinnser patient branches")

    with sql_service.get_engine().connect() as c:

        branches = pd.read_csv('data/patient_branch_zip.csv')
        branches.to_sql(name='KinnserPatientBranch', con=c, schema='Staging',
                        if_exists='append', index=True)

    logger.info(f"Importing Kinnser patient scores")

    with sql_service.get_engine().connect() as c:

        branches = pd.read_csv('data/patient_score_kinnser.csv')
        branches.to_sql(name='KinnserPatientScore', con=c, schema='Staging',
                        if_exists='append', index=True)

    logger.info(f"Importing LTC400 patient scores")

    with sql_service.get_engine().connect() as c:

        branches = pd.read_csv('data/patient_score_ltc400.csv')
        branches.to_sql(name='LTC400PatientScore', con=c, schema='Staging',
                        if_exists='append', index=True)

    logger.info(f"Importing patient model datasets")

    datasets = [
        # Home health patients
        ('KinnsrBIBaseData/1787208c-08e2-4cf4-a7af-1bd118788a20',
         f'{output_folder}/KinnsrBIBaseData',
         'KinnserBIBaseData'),
        # Chronic condition lookup
        ('cc_crosswalk_kinnser/7d1fb957-c9e2-4500-bd5b-be57ae339c83',
         f'{output_folder}/cc_crosswalk_kinnser',
         'KinnserCrosswalk'),
        # Proprietary score, patient_risk_score
        # ('patient_score_kinnser/2c3491d7-5d7f-44df-80cb-654035b4652e',
        #  f'{output_folder}/patient_score_kinnser',
        #  'KinnserPatientScore'),
        # Nursing home patients
        ('LTC400BaseData/d3f05045-d122-4715-8d4f-144f834ac951',
         f'{output_folder}/LTC400BaseData',
         'LTC400BaseData'),
        # Chronic condition lookup
        ('cc_crosswalk_ltc400/45bc2e2d-75ca-4e8f-bbfb-584db8806f53',
         f'{output_folder}/cc_crosswalk_ltc400',
         'LTC400Crosswalk'),
        # Proprietary score
        # ('patient_score_ltc400/0a094741-5a7d-4b42-9443-3802ebb0f582',
        #  f'{output_folder}/patient_score_ltc400',
        #  'LTC400PatientScore'),
    ]

    for source, target, table in datasets:

        blob_service.blob_to_folder(
            container_name=CONTAINER_NAME,
            blob_prefix=source,
            output_directory=target
        )

        logger.debug(f'Downloaded {source}')

        df = load_dataset(target)

        logger.debug(f'Loaded {target}')

        with sql_service.get_engine().connect() as c:
            df.to_sql(name=table, con=c, schema='Staging',
                      if_exists='append', index=True)

        logger.debug(f"Exported to {table}")
