import logging

import pyarrow.parquet as pq

import utility.log

logger = logging.getLogger(__name__)


def load_dataset(parquet_directory):

    dataset = pq.ParquetDataset(parquet_directory)
    table = dataset.read()

    return table.to_pandas()