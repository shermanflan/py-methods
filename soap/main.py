import logging
from tempfile import TemporaryDirectory

from utility.etl import request_and_load

logger = logging.getLogger(__name__)


if __name__ == '__main__':

    # with TemporaryDirectory() as tmp_folder:
    # tmp_folder = './local/data'
    tmp_folder = './jupyter/data'

    request_and_load(output_folder=tmp_folder)

    logger.info(f"Process complete")