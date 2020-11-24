import logging

import utility.logging
from utility import JOB_PACKAGE, JOB_DEFINITION
from utility.api.oracle import OracleFusion

logger = logging.getLogger(__name__)


if __name__ == '__main__':

    # tmp_folder = './local/data'
    tmp_folder = './jupyter/data'

    erp = OracleFusion()

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
                                                          tmp_folder)

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
        logger.info(f"Downloading {r.dOriginalName} to {tmp_folder}")

        doc_df = erp.get_file(r.dID, tmp_folder)

        logger.info(f"Downloaded {doc_df.shape[0]} documents")

    logger.info(f"Process complete")