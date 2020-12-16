

"""
If we model a feasible set of tasks as vertices of a directed graph,
and we place a directed edge from u to v whenever the task for u must
be executed before the task for v, then we define a directed acyclic
graph.
"""


def topological_sort(g):
    """
    Repeatedly removes vertices with no constraints (incoming edges).
    If g has a cycle, the result will be incomplete.
    """
    topo = []
    ready_q = []  # vertices with no constraints (in deg == 0)
    in_deg = {}  # track in-degree per vertex

    for v in g:
        in_deg[v.uid] = g.in_degree(v.uid)

        if in_deg[v.uid] == 0:  # no constraints
            ready_q.append(v)

    while ready_q:
        v = ready_q.pop()
        topo.append(v)  # add to topological sort

        for edge in g.outgoing[v.uid].values():  # get outgoing neighbors
            neighbor = edge.opposite(v)

            in_deg[neighbor.uid] -= 1  # remove v's constraint

            if in_deg[neighbor.uid] == 0:
                ready_q.append(neighbor)

    # If there is a cycle, edges will remain
    return topo


def topological_sort2(node_count, prereqs):
    """
    Alternate implementation which accepts an input graph in edge list 
    format:
    
    [(a, b) such that a is dependent on b, i.e. b => a]
    
    TODO:
    - Convert edge list format to adjacency list
    - Convert edge list format to sparse matrix
    """
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
    return topo_sort, in_degree, visited


def get_out_edges(node, edges):
    return [u for u, v in edges if v == node]