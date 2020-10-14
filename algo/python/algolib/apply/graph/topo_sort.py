

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

    # Ready_q will be empty if a cycle exists as no vertices will have
    # in degree of 0.
    while ready_q:
        v = ready_q.pop()
        topo.append(v)  # add to topological sort

        for edge in g.outgoing[v.uid].values():  # get outgoing neighbors
            neighbor = edge.opposite(v)

            in_deg[neighbor.uid] -= 1  # remove v's constraint

            if in_deg[neighbor.uid] == 0:
                ready_q.append(neighbor)

    # Returns None if there is a cycle
    return topo
