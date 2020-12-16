from collections import namedtuple

"""
Adjacency list graph "sparse representation":
The base structure is a one-dimensional array of vertices in the graph.
When using an adjacency list to store an undirected graph, the same edge
(u, v) appears twice: once in the linked list of neighbor vertices for u
and once for v.

A cycle is a path of vertices that includes the same vertex multiple times.

If a path exists between any two pairs of vertices in a graph, then that
graph is connected.

Examples:
    1. A graph can be used to represent a maze. A vertex is created for
    each branching point in the maze as well as “dead ends.” An edge exists
    only if there is a direct path in the maze between the two vertices where
    no choice in direction can be made.
"""
from collections import defaultdict


class GraphException(Exception):
    pass


# TODO: Also create a simple Graph representation that's easy to remember.
# Maybe Graph of Dictionary(uid, Node), Node of Dictionary(uid, (Edge, Node))
# Or, list of named tuple (p, q, e) where index represents ith node in graph.
class Graph:
    """
    DATA-003
    Adjacency map implementation. When a graph is undirected, adding edge
    (u, v) also adds edge (v, u).
    """
    def __init__(self, directed=False):
        self.directed = directed
        self.vertices = {}
        self.outgoing = defaultdict(dict)  # dict (uid, dict (uid: edge))

        # If directed also track incoming edges as a separate view.
        self.incoming = defaultdict(dict) if directed else self.outgoing

    def add_vertex(self, uid, val=None):
        v = Vertex(uid, val)
        self.vertices[uid] = v
        return v

    def add_edge(self, source, destination, weight=1):

        e1 = Edge(source, destination, weight)

        # Add edge from source and from destination
        self.outgoing[source.uid][destination.uid] = e1
        self.incoming[destination.uid][source.uid] = e1

    def edge_count(self):
        n = sum([len(edges) for edges in self.outgoing.values()])

        return n if self.directed else n//2

    def get_edges(self):
        result = set()

        for e in self.outgoing.values():
            result.update(e.values())

        return result

    def get_edge(self, start, end):
        return self.outgoing[start].get(end)  # or None

    def in_degree(self, uid):
        return len(self.incoming[uid])

    def out_degree(self, uid):
        return len(self.outgoing[uid])

    def in_edges(self, uid):
        for edge in self.incoming[uid].values():
            yield edge

    def out_edges(self, uid):
        for edge in self.outgoing[uid].values():
            yield edge

    def __getitem__(self, item):
        return self.vertices[item]

    def __len__(self):
        return len(self.outgoing)

    def __iter__(self):
        for v in self.vertices.values():
            yield v


class Vertex:
    def __init__(self, uid, val=None):
        self.uid = uid
        self.val = val

    def __repr__(self):
        return str(self.uid)


class Edge:

    def __init__(self, u, v, weight):
        self.origin = u
        self.destination = v
        self.weight = weight

    def endpoints(self):
        return self.origin, self.destination

    def opposite(self, v):
        return self.destination if v is self.origin else self.origin

    def __repr__(self):
        return f"{self.origin}=>{self.destination}"
