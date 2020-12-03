import logging

from utility import (
    ACCOUNT_KEY, ACCOUNT_NAME, CONTAINER_NAME
)

from utility.api.blob import AzureBlobHook
from utility.api.parquet import load_dataset
import utility.log

logger = logging.getLogger(__name__)


if __name__ == '__main__':

    blob_service = AzureBlobHook(account_name=ACCOUNT_NAME,
                                 account_key=ACCOUNT_KEY)

    logger.info('Loading Kinnser datasets')

    # Home health patients
    blob_service.blob_to_folder(
        container_name=CONTAINER_NAME,
        blob_prefix='KinnsrBIBaseData/1787208c-08e2-4cf4-a7af-1bd118788a20',
        output_directory='jupyter/data/KinnsrBIBaseData'
    )
    kinnser_bi_base_data_df = load_dataset('jupyter/data/KinnsrBIBaseData')

    logger.debug(f'Loaded KinnsrBIBaseData: {kinnser_bi_base_data_df.shape}')

    # May not need this, already incorporated into proprietary score.
    # For example, hcc_ce, hcupModelScore
    # hcup_pred_kinnser_df = 'hcup_pred_kinnser/ed317a1e-7158-4ce0-aef9-82f1bb6b8c6c'

    # Chronic condition lookup
    blob_service.blob_to_folder(
        container_name=CONTAINER_NAME,
        blob_prefix='cc_crosswalk_kinnser/7d1fb957-c9e2-4500-bd5b-be57ae339c83',
        output_directory='jupyter/data/cc_crosswalk_kinnser'
    )
    cc_crosswalk_kinnser_df = load_dataset('jupyter/data/cc_crosswalk_kinnser')

    logger.debug(f'Loaded cc_crosswalk_kinnser: {cc_crosswalk_kinnser_df.shape}')

    # CMS HCC score by chronic conditions
    # May not need this, too much detail?
    # patient_hcc_cc_kinnser1_df = 'patient_hcc_cc_kinnser/42184e27-7d2a-4cd7-9680-41624c449af9'
    # patient_hcc_cc_kinnser2_df = 'patient_hcc_cc_kinnser/d88ff446-3390-4d68-b41b-b9fa50dafd41'
    # patient_hcc_kinnser_1_df = 'patient_hcc_kinnser/99e42932-40e9-4045-ba4d-f96fa58263e0'
    # patient_hcc_kinnser_2_df = 'patient_hcc_kinnser/e0eecd6d-507c-40c7-a075-52a120738ce9'

    # Proprietary score, patient_risk_score
    blob_service.blob_to_folder(
        container_name=CONTAINER_NAME,
        blob_prefix='patient_score_kinnser/2c3491d7-5d7f-44df-80cb-654035b4652e',
        output_directory='jupyter/data/patient_score_kinnser'
    )
    patient_score_kinnser_df = load_dataset('jupyter/data/patient_score_kinnser')

    logger.debug(f'Loaded patient_score_kinnser: {patient_score_kinnser_df.shape}')

    logger.info('Loading LTC400 datasets')

    # Nursing home patients
    blob_service.blob_to_folder(
        container_name=CONTAINER_NAME,
        blob_prefix='LTC400BaseData/d3f05045-d122-4715-8d4f-144f834ac951',
        output_directory='jupyter/data/LTC400BaseData'
    )
    ltc400_base_data_df = load_dataset('jupyter/data/LTC400BaseData')

    logger.debug(f'Loaded LTC400BaseData: {ltc400_base_data_df.shape}')

    # May not need this, already incorporated into score
    # hcup_pred_ltc400_df = 'hcup_pred_ltc400/348ba97b-1cf1-4333-baa0-20dc4a2a860f'

    # Chronic condition lookup
    blob_service.blob_to_folder(
        container_name=CONTAINER_NAME,
        blob_prefix='cc_crosswalk_ltc400/45bc2e2d-75ca-4e8f-bbfb-584db8806f53',
        output_directory='jupyter/data/cc_crosswalk_ltc400'
    )
    cc_crosswalk_ltc400_df = load_dataset('jupyter/data/cc_crosswalk_ltc400')

    logger.debug(f'Loaded cc_crosswalk_ltc400: {cc_crosswalk_ltc400_df.shape}')

    # CMS HCC score by chronic conditions
    # May not need this, too much detail?
    # patient_hcc_cc_ltc400_1_df = 'patient_hcc_cc_ltc400/2ce16ecc-171e-45d8-b4c3-9f5dd44ac41a'
    # patient_hcc_cc_ltc400_2_df = 'patient_hcc_cc_ltc400/d6bee59d-c3bc-42a6-9c82-855e09b17c0e'
    # patient_hcc_ltc400_1_df = 'patient_hcc_ltc400/26adaa09-b1cd-4c06-877c-b6f6818f5917'
    # patient_hcc_ltc400_2_df = 'patient_hcc_ltc400/b31a848e-a57d-484c-bbd2-ac89bec99061'

    # Proprietary score
    blob_service.blob_to_folder(
        container_name=CONTAINER_NAME,
        blob_prefix='patient_score_ltc400/0a094741-5a7d-4b42-9443-3802ebb0f582',
        output_directory='jupyter/data/patient_score_ltc400'
    )
    patient_score_ltc400_df = load_dataset('jupyter/data/patient_score_ltc400')

    logger.debug(f'Loaded patient_score_ltc400: {patient_score_ltc400_df.shape}')

    logger.info('Process complete')
