from algolib.apply.search import Color

from collections import deque
import math


def bfs(g, root):
    """
    SEARCH-007
    Breadth-First Search systematically visits all vertices in the graph
    G = (V, E) that are k edges away from the source vertex s before
    visiting any vertex that is k + 1 edges away. Breadth-First Search
    is guaranteed to find the shortest path in the graph from vertex s
    to a desired target vertex.

    The implementation below performs breadth-first search on graph from
    vertex root, and compute BFS distance and predecessor vertex for all
    vertices in the graph.

    Average: O(V+E)
    Worst: O(V+E)
    Best: O(V+E)

    Storage: O(V)

    :param g: The input Graph
    :param root: The root or start Node
    :return: Return the pred, dist collections

    """
    pred, dist, color = {}, {}, {}

    # Initialize to not visited
    for n in g:
        pred[n.uid] = -1
        color[n.uid] = Color.WHITE
        dist[n.uid] = math.inf

    dist[root.uid] = 0
    q = deque([root])
    color[root.uid] = Color.GRAY

    while q:
        # This is FIFO, not LIFO
        node = q.popleft()

        # Explore neighbors
        for edge in g.outgoing[node.uid].values():
            friend = edge.opposite(node)

            if color[friend.uid] == Color.WHITE:
                dist[friend.uid] = dist[node.uid] + edge.weight
                pred[friend.uid] = node.uid
                q.append(friend)
                color[friend.uid] = Color.GRAY  # no longer unvisited

        color[node.uid] = Color.BLACK  # processed

    return pred, dist


def bfs_level(g, root):
    pred, dist, color = {}, {}, {}

    # Initialize to not visited
    for n in g:
        pred[n.uid] = -1
        color[n.uid] = Color.WHITE
        dist[n.uid] = math.inf

    dist[root.uid] = 0
    q = deque([root.uid])
    color[root.uid] = Color.GRAY
    level = [root]  # init with root
    save_levels = [[root.uid]]

    while level:

        next_level = []

        # Explore neighbors level by level.
        for node in level:
            for edge in g.outgoing[node.uid].values():
                friend = edge.opposite(node)

                if color[friend.uid] == Color.WHITE:
                    dist[friend.uid] = dist[node.uid] + edge.weight
                    pred[friend.uid] = node.uid
                    next_level.append(friend)
                    color[friend.uid] = Color.GRAY  # no longer unvisited

        color[node] = Color.BLACK  # processed
        save_levels.append([n.uid for n in next_level])

        # Setup next level to explore.
        level = next_level

    return pred, dist, save_levels


