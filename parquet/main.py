import logging
from tempfile import TemporaryDirectory

from utility.etl import import_datasets
import utility.log

logger = logging.getLogger(__name__)


if __name__ == '__main__':

    logger.info('Starting import')

    with TemporaryDirectory() as tmp_folder:
        import_datasets(tmp_folder)

    logger.info('Process complete')
