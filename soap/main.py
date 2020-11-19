"""
References:
- https://docs.python-zeep.org/en/master/index.html

Miscellaneous:
- See this [post](https://stackoverflow.com/questions/48655638/python-zeep-send-un-escaped-xml-as-content)
for special handling re: XML escaping
"""
import logging
import os
from time import sleep
from xml import etree
from zipfile import ZipFile

from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client, Settings, Plugin
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


def get_document_id(soap_client, search_query):
    # factory = soap_client.type_factory('ns0')
    field_element = soap_client.get_element(name='ns0:Field')
    service_type = soap_client.get_type(name='ns0:Service')
    search_element = field_element(search_query, name='QueryText')

    search_service = service_type(
        Document={
            "Field": [
                search_element
            ]
        },
        IdcService='GET_SEARCH_RESULTS')

    logger.info(f"field: {search_element}")
    logger.info(f"service: {search_service}")

    response = soap_client.service.GenericSoapOperation(
        Service=search_service, webKey='cs')

    for result in response['Service']['Document']['ResultSet']:
        if result['name'] == 'SearchResults':
            for row in result['Row']:
                for field in row['Field']:
                    if field['name'] == 'dID':
                        return field['_value_1']
    return None


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
                         transport=transport
                         )

    search_query = u"""
    dOriginalName <starts> `MANIFEST_DATA_41`
    <AND> dSecurityGroup <starts> `OBIAImport`
    """.strip()

    logger.info(f"Searching files for '{search_query}'")

    document_id = get_document_id(soap_client, search_query)

    if document_id:
        logger.info(f"Found document {document_id}")
    else:
        raise Exception(f"Document {document_id} does not exist")

    document_id = 57296
    logger.info(f"Downloading document {document_id}")

    field_element = soap_client.get_element(name='ns0:Field')
    service_type = soap_client.get_type(name='ns0:Service')
    doc_id_element = field_element(document_id, name='dID')

    file_service = service_type(
        Document={
            "Field": [
                doc_id_element
            ]
        },
        IdcService='GET_FILE')

    logger.info(f"field: {doc_id_element}")
    logger.info(f"service: {file_service}")

    # ns0:Field(xsd:string, name: xsd:anySimpleType)
    # ns0:ResultSet(Row: ns0:Row[], name: xsd:anySimpleType)
    # ns0:Container(Field: ns0:Field[], ResultSet: ns0:ResultSet[], OptionList: ns0:OptionList[], _attr_1: {})
    # ns0:Service(
    #     User: ns0:Container,
    #     Document: {
    #         Field: ns0:Field[],
    #         ResultSet: ns0:ResultSet[],
    #         OptionList: ns0:OptionList[],
    #         File: ns0:File[],
    #         _attr_1: {}},
    #     IdcService: xsd:anySimpleType)
    # GenericSoapOperation(Service: ns0:Service, webKey: xsd:anySimpleType)
    #     -> Service: ns0:Service, webKey: xsd:anySimpleType
    response = soap_client.service.GenericSoapOperation(
        Service=file_service, webKey='cs')

    doc_name = None
    # TODO: look into pandas explode, melt, etc.
    for attach in response['Service']['Document']['ResultSet']:
        if attach['name'] == 'FILE_DOC_INFO':
            for row in attach['Row']:
                for field in row['Field']:
                    if field['name'] == 'dOriginalName':
                        doc_name = field['_value_1']
                        break

    if doc_name:
        tmp_folder = './jupyter/data'
        doc_content = None
        for attach in response['Service']['Document']['File']:
            with open(os.path.join(tmp_folder, doc_name), 'wb') as f:
                f.write(attach['Contents'])

            # with ZipFile(tmp_zip) as z:
            #     z.extractall(path=tmp_folder)

            logger.info(f"Downloaded document {doc_name}")
