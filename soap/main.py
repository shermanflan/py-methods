import io
import json
import logging
import os
from tempfile import TemporaryDirectory
from zipfile import ZipFile

from utility import (
    EVENT_TOPIC_URI, EVENT_TOPIC_KEY,
    LAKE_URL, STORE_KEY,
    LAKE_CONTAINER, LAKE_FOLDER_PATH)
from utility.api.event import EventGridHook
from utility.api.lake import LakeFactory
from utility.api.oracle import OracleFusionHook
from utility.etl import request_and_load
import utility.logging

logger = logging.getLogger(__name__)


if __name__ == '__main__':

    # with TemporaryDirectory() as tmp_folder:
    # tmp_folder = './local/data'
    # tmp_folder = './jupyter/data'
    # request_and_load(output_folder=tmp_folder)

    event_client = EventGridHook(
        topic_uri=EVENT_TOPIC_URI,
        topic_key=EVENT_TOPIC_KEY)

    for i in range(3):
        logger.info(f"Publishing event {i}")

        event_client.publish_event(
            subject="new-job-oracle-fusion",
            event_type="new-job-event-3",
            data={
                "source": "bsh.aci.oracle2lake.dev",
                "tracking_id": i,
                "file_name_prefix": "MANIFEST_DATA_41",
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

    # Using bytes
    # data = io.BytesIO()
    # num_bytes = data.write(b"some data2")
    # data_bytes = data.getvalue()  # read()
    #
    # LakeFactory().upload_data(lake_container=LAKE_CONTAINER, lake_dir=LAKE_FOLDER_PATH,
    #                           file_name='test-03.txt', data=data_bytes)

    logger.info(f"Process complete")