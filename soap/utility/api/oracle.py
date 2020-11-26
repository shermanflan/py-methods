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
from zipfile import ZipFile

import pandas as pd
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client, Settings
from zeep.cache import SqliteCache
from zeep.transports import Transport

from utility import (
    ERP_URI, SOAP_URI, FUSION_USER, FUSION_USER_PWD
)
import utility.logging

logger = logging.getLogger(__name__)


class OracleFusionHook:
    def __init__(self):
        self.erp_client = None
        self.soap_client = None

    def get_soap_client(self):
        if self.soap_client:
            return self.soap_client

        session = Session()
        session.auth = HTTPBasicAuth(FUSION_USER, FUSION_USER_PWD)

        settings = Settings(strict=True,
                            xml_huge_tree=True,
                            raw_response=False,
                            force_https=True
                            )
        transport = Transport(cache=SqliteCache(), session=session)

        logger.info("Creating ERP client")

        self.soap_client = Client(wsdl=SOAP_URI,
                             settings=settings,
                             transport=transport
                             )
        return self.soap_client

    def get_erp_client(self):
        if self.erp_client:
            return self.erp_client

        session = Session()
        session.auth = HTTPBasicAuth(FUSION_USER, FUSION_USER_PWD)

        settings = Settings(strict=True,
                            xml_huge_tree=True,
                            raw_response=False,
                            force_https=True
                            )
        transport = Transport(cache=SqliteCache(), session=session)

        logger.info("Creating SOAP client")

        self.erp_client = Client(wsdl=ERP_URI,
                            settings=settings,
                            transport=transport)

        return self.erp_client

    def submit_ess_job_request(self, package, job, parameters=None):
        return self.get_erp_client().service.submitESSJobRequest(
            jobPackageName=package,
            jobDefinitionName=job,
            paramList=parameters)

    def get_ess_job_status(self, request_id, no_wait=False,
                           max_tries=360,
                           poke_interval=10):
        status = self.get_erp_client().service.getESSJobStatus(
            requestId=request_id)

        if not no_wait:
            # TODO: What are the completion statuses?
            tries = 0
            while status not in ('SUCCEEDED', 'FAILED') \
                    and tries < max_tries:
                logger.debug(f"Job status is {status}")
                status = self.get_erp_client().service.getESSJobStatus(
                    requestId=request_id)
                sleep(poke_interval)
                tries += 1

        return status

    def download_ess_job_execution_details(self, request_id,
                                           output_folder,
                                           file_type='log',
                                           save_attachments=False):
        pack = self.get_erp_client().service.downloadESSJobExecutionDetails(
            requestId=request_id,
            fileType=file_type)

        documents = []
        for a in pack:
            logger.debug(f"Attachment: {a.DocumentId}, {a.DocumentName}, {a.DocumentTitle}")

            documents.append({k: a[k] for k in a if k != 'Content'})

            if save_attachments:
                tmp_path = os.path.join(output_folder, a.DocumentName)

                with open(tmp_path, 'wb') as f:
                    f.write(a.Content)
                if a.ContentType == 'zip':
                    with ZipFile(tmp_path) as z:
                        z.extractall(path=output_folder)

        return pd.DataFrame(documents)

    def get_search_results(self, query):
        field_element = self.get_soap_client().get_element(name='ns0:Field')
        service_type = self.get_soap_client().get_type(name='ns0:Service')

        search_service = service_type(
            Document={
                "Field": [
                    field_element(query, name='QueryText')
                ]
            },
            IdcService='GET_SEARCH_RESULTS')

        logger.debug(f"service: {search_service}")

        response = self.get_soap_client().service.GenericSoapOperation(
            Service=search_service, webKey='cs')

        results = []
        for result in response['Service']['Document']['ResultSet']:
            if result['name'] == 'SearchResults':
                for row in result['Row']:
                    result = {}
                    for field in row['Field']:
                        result[field['name']] = field['_value_1']
                    results.append(result)

        return pd.DataFrame(results)

    def get_file(self, document_id, output_folder):
        field_element = self.get_soap_client().get_element(
            name='ns0:Field')
        service_type = self.get_soap_client().get_type(
            name='ns0:Service')

        file_service = service_type(
            Document={
                "Field": [
                    field_element(document_id, name='dID')
                ]
            },
            IdcService='GET_FILE')

        logger.debug(f"service: {file_service}")

        response = self.get_soap_client().service.GenericSoapOperation(
            Service=file_service, webKey='cs')

        documents = []
        for attach in response['Service']['Document']['ResultSet']:
            if attach['name'] == 'FILE_DOC_INFO':
                for row in attach['Row']:
                    document = {}
                    for field in row['Field']:
                        document[field['name']] = field['_value_1']
                    documents.append(document)

        docs_df = pd.DataFrame(documents)
        file_paths = []
        if docs_df.shape[0] > 0:

            for attach in response['Service']['Document']['File']:
                tmp_path = os.path.join(output_folder, attach['href'])
                with open(tmp_path, 'wb') as f:
                    f.write(attach['Contents'])

                content_type = docs_df.loc[
                    docs_df.dOriginalName == attach['href'],
                    'dFormat'].iloc[0]

                if content_type == 'application/zip':
                    with ZipFile(tmp_path) as z:
                        z.extractall(path=output_folder)
                        file_paths.extend(z.namelist())
                else:
                    file_paths.append(tmp_path)

            return docs_df, file_paths
        else:
            raise Exception("Document does not exist")

    def get_content(self, document_id):
        field_element = self.get_soap_client().get_element(
            name='ns0:Field')
        service_type = self.get_soap_client().get_type(
            name='ns0:Service')

        file_service = service_type(
            Document={
                "Field": [
                    field_element(document_id, name='dID')
                ]
            },
            IdcService='GET_FILE')

        logger.debug(f"service: {file_service}")

        response = self.get_soap_client().service.GenericSoapOperation(
            Service=file_service, webKey='cs')

        documents = []
        for attach in response['Service']['Document']['ResultSet']:
            if attach['name'] == 'FILE_DOC_INFO':
                for row in attach['Row']:
                    document = {}
                    for field in row['Field']:
                        document[field['name']] = field['_value_1']
                    documents.append(document)

        docs_df = pd.DataFrame(documents)
        if docs_df.shape[0] > 0:
            return docs_df, response['Service']['Document']['File']
        else:
            raise Exception("Document does not exist")
