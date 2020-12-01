import os

from azure.core.exceptions import ResourceNotFoundError
from azure.storage.blob import BlobServiceClient, BlobType

from utility import (
    ACCOUNT_KEY, ACCOUNT_NAME, CONTAINER_NAME
)


if __name__ == '__main__':

    blob_service = BlobServiceClient(
        account_url=f'https://{ACCOUNT_NAME}.blob.core.windows.net/',
        credential=ACCOUNT_KEY)

    container_client = blob_service.get_container_client(CONTAINER_NAME)

    # try:
    #     for blob in container_client.list_blobs():
    #         print("Found blob: ", blob.name)
    # except ResourceNotFoundError:
    #     print("Container not found.")

    block_blob_client = container_client.get_blob_client(
        blob = 'patient_score_kinnser/2c3491d7-5d7f-44df-80cb-654035b4652e/part-00000.parquet'
    )

    try:
        stream = block_blob_client.download_blob()
    except ResourceNotFoundError:
        print("No blob found.")
