import io
import json
import logging
import os
from tempfile import TemporaryDirectory
import uuid
from zipfile import ZipFile

from utility import (
    EVENT_TOPIC_URI, EVENT_TOPIC_KEY,
    LAKE_URL, STORE_KEY,
    LAKE_CONTAINER, LAKE_PATH)
from utility.api.event import EventGridHook
from utility.api.lake import LakeFactory
from utility.api.oracle import OracleFusionHook
from utility.etl import request_and_load
import utility.logging

logger = logging.getLogger(__name__)


if __name__ == '__main__':

    event_client = EventGridHook(
        topic_uri=EVENT_TOPIC_URI,
        topic_key=EVENT_TOPIC_KEY)

    for i in range(1):
        logger.info(f"Publishing event {i}")

        event_client.publish_event(
            subject="new-job-oracle-fusion",
            event_type="new-job-event-3",
            data={
                "source": "bsh.aci.oracle2lake.dev",
                "tracking_id": i,
                "file_name_prefix": "file_fscmtopmodelam_finartoppublicmodelam_transactionheaderpvo-batch1944942919-20201012_063148.zip",
                # "file_name_prefix": "MANIFEST_DATA_41",
                "lake_container": "event-grid-subscribe",
                "lake_path": "output"
            })
        # event_client.publish_event(
        #     subject="new-job-1",
        #     event_type="new-job-event-1",
        #     data={
        #         "source": "bsh.aci.oracle2lake.dev",
        #         "tracking_id": i
        #     })

    # with TemporaryDirectory() as tmp_folder:
    # to_folder = './jupyter/data'

    # request_and_load(output_folder=tmp_folder)

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

    # Using bytes
    # data = io.BytesIO()
    # num_bytes = data.write(b"some data2")
    # data_bytes = data.getvalue()  # read()
    #
    # LakeFactory().upload_data(lake_container=LAKE_CONTAINER, lake_dir=LAKE_FOLDER_PATH,
    #                           file_name='test-03.txt', data=data_bytes)

    logger.info(f"Process complete")