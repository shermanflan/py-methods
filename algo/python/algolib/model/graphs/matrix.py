

# TODO: Add adjacency matrix implementation.
"""
Adjacency matrix graph "full representation":
The entry A[i][j] stores the weight of the edge from v_i to v_j; when
there is no edge from v_i to v_j, A[i][j] is set to some special value,
such as 0, –1, inf. When using an adjacency matrix to store an
undirected graph, entry A[i][j] = A[j][i].

With an adjacency matrix, checking whether an edge (v_i, v_j) exists takes
constant time, but with an adjacency list, it depends on the number of
edges in the list for v_i. In contrast, with an adjacency matrix, you need
more space and you lose the ability to identify all incident edges to a
vertex in time proportional to the number of those edges; instead, you must
check all possible edges, which becomes significantly more expensive when
the number of vertices becomes large.

You should use an adjacency matrix representation when working with dense
graphs in which nearly every possible edge exists.
"""