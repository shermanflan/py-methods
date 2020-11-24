import logging

from utility import (
    JOB_PACKAGE, JOB_DEFINITION,
    LAKE_CONTAINER, LAKE_FOLDER_PATH)
from utility.api.lake import LakeFactory
from utility.api.oracle import OracleFusionHook
import utility.logging

logger = logging.getLogger(__name__)


def request_and_load(output_folder):
    erp = OracleFusionHook()

    logger.info(f"Initiating {JOB_DEFINITION} job request")

    job_id = erp.submit_ess_job_request(package=JOB_PACKAGE,
                                        job=JOB_DEFINITION)

    logger.info(f"Checking job status for job {job_id}")

    job_status = erp.get_ess_job_status(job_id)

    if job_status != 'SUCCEEDED':
        raise Exception(f"Job request for {JOB_DEFINITION} failed")

    logger.info(f"Job request {job_id} complete")

    logger.info(f"Downloading job details for job {job_id}")

    documents_df = erp.download_ess_job_execution_details(job_id,
                                                          output_folder)

    logger.info(f"Downloaded {documents_df.shape[0]} documents")

    file_name = 'MANIFEST_DATA_41'
    # file_name = 'file_fscmtopmodelam_finartoppublicmodelam_transactionheaderpvo-batch1944942919-20201012_063148.zip'
    search_query = f"""
    dOriginalName <starts> `{file_name}`
    <AND> dSecurityGroup <starts> `OBIAImport`
    """.strip()

    logger.info(f"Searching files for '{search_query}'")

    results_df = erp.get_search_results(search_query)

    if results_df.shape[0] > 0:
        logger.info(f"Found {results_df.shape[0]} documents")
    else:
        raise Exception(f"No documents found")

    for r in results_df.itertuples(index=False):
        logger.info(f"Downloading {r.dOriginalName} to {output_folder}")

        doc_df, file_paths = erp.get_file(r.dID, output_folder)

        logger.info(f"Downloaded {len(file_paths)} documents")

        logger.info("Uploading to lake")
        LakeFactory().upload_files(lake_container=LAKE_CONTAINER,
                                   lake_dir=LAKE_FOLDER_PATH,
                                   files=file_paths)
