import logging
import os
from time import sleep
from zipfile import ZipFile

from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client, Settings
from zeep.cache import SqliteCache
from zeep.transports import Transport

from client import (
    ERP_URI, SOAP_URI, FUSION_USER, FUSION_USER_PWD, JOB_PACKAGE,
    JOB_DEFINITION)
log_level_code = getattr(logging, os.environ.get('LOG_LEVEL', ''), logging.DEBUG)
logging.basicConfig(
    format='%(asctime)s %(levelname)s [%(name)s]: %(message)s'
    , datefmt='%Y-%m-%d %I:%M:%S %p'
    , level=log_level_code)

logger = logging.getLogger(__name__)


def submit_ess_job(client, tmp_folder, package, job):
    request_id = client.service.submitESSJobRequest(
        jobPackageName=package,
        jobDefinitionName=job)

    logger.info(f"Checking job status for job {request_id}")

    status = client.service.getESSJobStatus(requestId=request_id)

    while status != 'SUCCEEDED':
        logger.info(f"Job status is {status}")
        status = client.service.getESSJobStatus(requestId=request_id)
        sleep(secs=60)

    logger.info(f"Downloading job details for job {request_id}")

    # Returns ns5:DocumentDetails[]
    # ns5: DocumentDetails(
    #     Content: ns6: base64Binary - DataHandler,
    #     FileName: xsd:string,
    #     ContentType: xsd:string,
    #     DocumentTitle: xsd:string,
    #     DocumentAuthor: xsd:string,
    #     DocumentSecurityGroup: xsd:string,
    #     DocumentAccount: xsd:string,
    #     DocumentName: xsd:string,
    #     DocumentId: xsd:string
    # )
    pack = client.service.downloadESSJobExecutionDetails(
        requestId=request_id,
        fileType="all")

    for a in pack:
        logger.debug(f"Attachment: {a.DocumentId}, {a.DocumentName}, {a.DocumentTitle}, {a.ContentType}")

        tmp_zip = os.path.join(tmp_folder, a.DocumentName)

        with open(tmp_zip, 'wb') as f:
            f.write(a.Content)

        with ZipFile(tmp_zip) as z:
            z.extractall(path=tmp_folder)

    return request_id


if __name__ == '__main__':

    session = Session()
    session.auth = HTTPBasicAuth(FUSION_USER, FUSION_USER_PWD)

    settings = Settings(strict=True,
                        xml_huge_tree=True,
                        raw_response=False,
                        force_https=True
                        )
    transport = Transport(cache=SqliteCache(), session=session)

    # erp_client = Client(wsdl=ERP_URI,
    #                     settings=settings,
    #                     transport=transport)

    # logger.info("Initiating job request")
    #
    # request_id = submit_ess_job(erp_client,
    #                             tmp_folder='./jupyter/data',
    #                             package=JOB_PACKAGE,
    #                             job=JOB_DEFINITION)
    #
    # logger.info(f"Job request {request_id} complete")

    # logger.info(f"Searching files for {request_id} complete")
    soap_client = Client(wsdl=SOAP_URI,
                         settings=settings,
                         transport=transport)
    factory = soap_client.type_factory('ns0')

    field_element = soap_client.get_element(name='ns0:Field')

    search_for = 'dOriginalName &lt;starts> `MANIFEST_DATA_41` &lt;AND> dSecurityGroup &lt;starts> `OBIAImport`'
    logger.info(f"field: {field_element(search_for, name='QueryText')}")

    # service_type = soap_client.get_type(name='ns0:Service')
    # search_service = service_type(Document={
    #     [
    #         field_element(name='QueryText')
    #     ]
    # })
