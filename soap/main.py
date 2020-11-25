from datetime import datetime
import io
import json
import logging
from tempfile import TemporaryDirectory
import uuid

from azure.eventgrid import EventGridClient
from azure.core.exceptions import (ResourceNotFoundError,
                                   ResourceExistsError)
from azure.storage.filedatalake import DataLakeServiceClient
from msrest.authentication import TopicCredentials

from utility import (
    EVENT_TOPIC_URI, EVENT_TOPIC_KEY,
    LAKE_URL, STORE_KEY,
    LAKE_CONTAINER, LAKE_FOLDER_PATH)
from utility.api.lake import LakeFactory
from utility.etl import request_and_load

logger = logging.getLogger(__name__)


def publish_event():
    credentials = TopicCredentials(EVENT_TOPIC_KEY)
    event_grid_client = EventGridClient(credentials)
    event_grid_client.publish_events(
        topic_hostname=EVENT_TOPIC_URI,
        events=[{
            "id": uuid.uuid4(),
            "subject": "new-job-oracle-fusion",
            "data": {
                "source": "bsh.aci.oracle2lake.dev",
                "file_name_prefix": "MANIFEST_DATA_41"
            },
            "event_type": "new-job-event-3",
            "event_time": datetime.utcnow(),
            "data_version": 1
        }]
    )


if __name__ == '__main__':

    # with TemporaryDirectory() as tmp_folder:
    # tmp_folder = './local/data'
    # tmp_folder = './jupyter/data'
    # request_and_load(output_folder=tmp_folder)

    publish_event()

    # logger.info("Uploading to lake")

    # Using string
    # data = json.dumps({"key": "testing text"})
    # LakeFactory().upload_data(lake_container=LAKE_CONTAINER, lake_dir=LAKE_FOLDER_PATH,
    #                           file_name='test-02.txt', data=data)

    # Using bytes
    # data = io.BytesIO()
    # num_bytes = data.write(b"some data2")
    # data_bytes = data.getvalue()  # read()
    #
    # LakeFactory().upload_data(lake_container=LAKE_CONTAINER, lake_dir=LAKE_FOLDER_PATH,
    #                           file_name='test-03.txt', data=data_bytes)

    logger.info(f"Process complete")