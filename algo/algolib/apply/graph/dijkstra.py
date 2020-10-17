
"""
Finds minimum distance in a graph with positive edges (w(e) >= 0).
This algorithm is undefined for negative-weight paths.

An example of a "greedy" algorithm which solve the problem at hand
by repeatedly selecting the best choice from among those available
in each iteration. Greedy approaches are useful when trying to
optimize some cost function over a collection of objects.
"""
from math import inf
from algolib.model.heap import *


def shortest_path(g, start):
    dist = {}  # shortest distances so far
    cloud = {}  # shortest path to vertices so far
    pq = Heap()  # min heap of dist[v]: v
    pq_index = {}  # locators to heap nodes

    # Initialize distances
    for v in g:
        if v is start:
            dist[v.uid] = 0
        else:
            dist[v.uid] = inf
        pq_index[v.uid] = pq.add(dist[v.uid], v)

    while not pq.is_empty():
        key, u = pq.remove_min()
        cloud[u.uid] = key  # shortest path
        del pq_index[u.uid]  # processed u

        for e in g.out_edges(u.uid):
            v = e.opposite(u)
            if v not in cloud:
                # Relaxation
                if dist[u.uid] + e.weight < dist[v.uid]:
                    dist[v.uid] = dist[u.uid] + e.weight
                    pq.update(pq_index[v.uid], dist[v.uid], v)

    return cloud


def build_shortest_path_tree(g, start, dist):
    """
    Constructs minimum path from start to a vertex v as
    stored in the tree map (vertex to edge from predecessor).
    """
    tree = {}
    for v in dist:
        if v != start.uid:
            for edge in g.in_edges(v):
                u = edge.opposite(g[v])
                if dist[v] == dist[u.uid] + edge.weight:
                    tree[v] = edge

    return tree
