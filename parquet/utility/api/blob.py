import logging
import os

from azure.core.exceptions import ResourceNotFoundError
from azure.storage.blob import BlobServiceClient

import utility.log

logger = logging.getLogger(__name__)


class AzureBlobHook:

    def __init__(self, account_name, account_key):
        if not account_name or not account_key:
            raise Exception('Missing blob credentials')

        self.account_name = account_name
        self.account_key = account_key
        self.client = None

    def get_client(self):
        if self.client:
            return self.client

        logger.info("Authenticating to blob service")

        self.client = BlobServiceClient(
            account_url=f'https://{self.account_name}.blob.core.windows.net/',
            credential=self.account_key)
        return self.client

    def blob_to_folder(self, container_name,
                       blob_prefix, output_directory):
        container_client = self.get_client().get_container_client(
            container_name)

        parquet_blobs = []

        for blob in container_client.list_blobs(name_starts_with=blob_prefix):
            logger.debug(f"Found {blob.name}")
            parquet_blobs.append(blob.name)
            # if blob.name.endswith('.parquet'):
            #     logger.debug(f"Found {blob.name}")
            #     parquet_blobs.append(blob.name)

        os.makedirs(output_directory, exist_ok=True)

        for blob in parquet_blobs:

            file_name = os.path.split(blob)[1]
            target_path = os.path.join(output_directory, file_name)

            try:
                logger.info(f'Downloading {file_name} to {target_path}')
                blob_client = container_client.get_blob_client(blob)

                with open(target_path, "wb") as f:
                    storage_stream = blob_client.download_blob()
                    storage_stream.download_to_stream(f)

            except ResourceNotFoundError as e:
                logger.error("No blob found.")

        return output_directory
