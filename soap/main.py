import io
import json
import logging
import os
from tempfile import TemporaryDirectory
import uuid
import yaml
from yaml.loader import FullLoader
from zipfile import ZipFile

from utility import (
    APP_KEY, EVENT_TOPIC_URI, EVENT_TOPIC_KEY,
    LAKE_URL, STORE_KEY,
    LAKE_CONTAINER, LAKE_PATH)
from utility.api.event import EventGridHook
from utility.api.lake import LakeFactory
from utility.api.oracle import OracleFusionHook
from utility.etl import request_and_load
import utility.logging

logger = logging.getLogger(__name__)


if __name__ == '__main__':

    logger.info("Loading event configuration")

    with open('config/events.yaml', 'rt', encoding='utf-8') as f:
        config = yaml.load(f, Loader=FullLoader)

    logger.info(config)

    event_client = EventGridHook(
        topic_uri=EVENT_TOPIC_URI,
        topic_key=EVENT_TOPIC_KEY)

    for event in [e['event'] for e in config['events']]:
        logger.info(f"Publishing event {event}")

        event_client.publish_event(
            subject=event['subject'],
            event_type=event['eventType'],
            data={
                "source": APP_KEY,
                "tracking_id": str(uuid.uuid4()),
                "file_name_prefix": event['fileNamePrefix'],
                "lake_container": event['lakeContainer'],
                "lake_path": event['lakePath']
            })

    # with TemporaryDirectory() as tmp_folder:
    # to_folder = './jupyter/data'
    # request_and_load(output_folder=tmp_folder)

    # Using bytes
    # data = io.BytesIO()
    # num_bytes = data.write(b"some data2")
    # data_bytes = data.getvalue()  # read()
    # LakeFactory().upload_data(lake_container=LAKE_CONTAINER, lake_dir=LAKE_FOLDER_PATH,
    #                           file_name='test-03.txt', data=data_bytes)

    # file_name = 'MANIFEST_DATA_41'
    # file_name = 'file_fscmtopmodelam_finartoppublicmodelam_transactionheaderpvo-batch1944942919-20201012_063148.zip'
    # search_query = f"""
    # dOriginalName <starts> `{file_name}`
    # <AND> dSecurityGroup <starts> `OBIAImport`
    # """.strip()
    #
    # logger.info(f"Searching files for '{search_query}'")
    #
    # erp = OracleFusionHook()
    #
    # results_df = erp.get_search_results(search_query)
    #
    # if results_df.shape[0] > 0:
    #     logger.info(f"Found {results_df.shape[0]} documents")
    # else:
    #     raise Exception(f"No documents found")
    #
    # for r in results_df.itertuples(index=False):
    #     logger.info(f"Downloading {r.dOriginalName} to {LAKE_PATH}")
    #
    #     docs_df, content = erp.get_content(r.dID)
    #
    #     logger.info(f"Downloaded {docs_df.shape[0]} documents")
    #
    #     for attach in content:
    #
    #         logger.info("Uploading to lake")
    #
    #         content_type = docs_df.loc[
    #             docs_df.dOriginalName == attach['href'],
    #             'dFormat'].iloc[0]
    #
    #         if content_type == 'application/zip':
    #             with ZipFile(io.BytesIO(attach['Contents'])) as z:
    #                 for member in z.infolist():
    #                     file_name = f"{uuid.uuid4()}-{member.filename}"
    #                     data = z.open(name=member.filename)
    #
    #                     LakeFactory().upload_data(lake_container=LAKE_CONTAINER,
    #                                               lake_dir=LAKE_PATH,
    #                                               file_name=file_name,
    #                                               data=data.read())
    #         else:
    #             file_name = f"{uuid.uuid4()}-{attach['href']}"
    #
    #             LakeFactory().upload_data(lake_container=LAKE_CONTAINER,
    #                                       lake_dir=LAKE_PATH,
    #                                       file_name=file_name,
    #                                       data=attach['Contents'])

    logger.info(f"Process complete")