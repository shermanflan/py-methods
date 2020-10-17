from algolib.apply.search import Color


def dfs(g, root):
    """
    SEARCH-006
    Depth-first-search of a graph. Once Depth-First Search
    completes, the pred values can be used to generate a path
    from the original source vertex, s, to each vertex in the graph.
    By itself, dfs does not find the shortest path between any 2
    vertices.

    Average: O(V + E)
    Worst: O(V + E)
    Best: O(V + E)

    O(n) storage representing the colors assigned during visits.

    :param g: The input Graph
    :param root: The root or start Node
    :return: Return the pred collection
    """
    pred, color = {}, {}

    # Initialize to not visited
    for n in g:
        pred[n.uid] = -1
        color[n.uid] = Color.WHITE

    # Visit recursively
    def dfs_visit(n):

        color[n.uid] = Color.GRAY # pre-order

        for edge in g.outgoing[n.uid].values():
            # Search unvisited
            friend = edge.opposite(n)

            if color[friend.uid] == Color.WHITE:
                pred[friend.uid] = n.uid
                dfs_visit(friend)

        color[n.uid] = Color.BLACK # post-order

    dfs_visit(root)

    return pred


def dfs_i(g, root):
    """
    SEARCH-006

    Average: O(V + E)
    Worst: O(V + E)
    Best: O(V + E)

    O(n) storage representing the colors assigned during visits.

    :param g: The input Graph
    :param root: The root or start Node
    :return: Return the pred collection
    """
    pred, visited = {}, {}
    stack = []

    # Initialize to not visited
    for n in g:
        pred[n.uid] = -1
        visited[n.uid] = Color.WHITE

    stack.append(root)

    # Visit iteratively
    while stack:
        # This is LIFO, not FIFO.
        n = stack.pop()

        visited[n.uid] = Color.GRAY

        for edge in g.outgoing[n.uid].values():
            # Search unvisited
            friend = edge.opposite(n)

            if visited[friend.uid] == Color.WHITE:
                pred[friend.uid] = n.uid
                stack.append(friend)

        visited[n.uid] = Color.BLACK

    return pred
