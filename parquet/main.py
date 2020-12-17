import logging
from tempfile import TemporaryDirectory

from parquet_util.etl import import_datasets
import parquet_util.log

logger = logging.getLogger(__name__)


def get_out_edges(node, edges):
    return [u for u, v in edges if v == node]


def topological_sort(node_count, prereqs):
    from collections import deque

    topo_sort = []
    in_degree = [0 for _ in range(node_count)]

    # Calculate in degree for each vertex
    for end, start in prereqs:
        in_degree[end] += 1

    # Construct initial ready queue
    ready_queue = deque([i for i, d in enumerate(in_degree) if d == 0])
    visited = 0

    while ready_queue:

        pre_req = ready_queue.popleft()
        topo_sort.append(pre_req)
        visited += 1

        for post_req in get_out_edges(pre_req, prereqs):

            # Remove edge
            in_degree[post_req] -= 1

            if in_degree[post_req] == 0:
                ready_queue.append(post_req)

    # If there is a cycle, edges will remain
    # if no cycle, then visited == node_count
    return topo_sort, in_degree


if __name__ == '__main__':

    # logger.info('Starting import')

    topo_sort, in_degree = topological_sort(2, [
        [0, 1],  # cycle
    ])
    logger.info(f'topo_sort: {topo_sort}')
    logger.info(f'final: {in_degree}')

    # logger.info('Process complete')
