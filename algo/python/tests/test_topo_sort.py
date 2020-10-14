from algolib.apply.graph.topo_sort import *
from algolib.model.graphs.sparse import *


def test_topological_sort():
    graph_test = Graph(directed=True)

    n_s = graph_test.add_vertex("s")
    n_7 = graph_test.add_vertex(7)
    n_8 = graph_test.add_vertex(8)
    n_9 = graph_test.add_vertex(9)
    n_t = graph_test.add_vertex("t")

    graph_test.add_edge(n_s, n_8)
    graph_test.add_edge(n_7, n_9)
    graph_test.add_edge(n_8, n_7)
    graph_test.add_edge(n_9, n_t)

    result = topological_sort(graph_test)

    assert result == [n_s, n_8, n_7, n_9, n_t]


def test_topological_sort_cycle():
    graph_test = Graph(directed=True)

    n_s = graph_test.add_vertex("s")
    n_7 = graph_test.add_vertex(7)
    n_8 = graph_test.add_vertex(8)
    n_9 = graph_test.add_vertex(9)
    n_t = graph_test.add_vertex("t")

    graph_test.add_edge(n_s, n_8)
    graph_test.add_edge(n_7, n_9)
    graph_test.add_edge(n_8, n_7)
    graph_test.add_edge(n_9, n_t)
    graph_test.add_edge(n_t, n_s)

    result = topological_sort(graph_test)

    assert result == []
