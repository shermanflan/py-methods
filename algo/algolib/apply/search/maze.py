from collections import namedtuple, deque
from math import inf

Pos = namedtuple('Pos', 'x, y')


def solve(graph, root):
    """
    BFS to solve a maze given as a matrix. This will
    search all possible paths in the maze from position
    root. It will return predecessor and distance
    dictionaries.

    """
    pred, dist, visited = {}, {}, {}
    rows, cols = len(graph), len(graph[0])

    # Initialize to not visited
    for row in range(rows):
        for col in range(cols):
            pred[(row, col)] = -1
            visited[(row, col)] = False
            dist[(row, col)] = inf

    dist[root] = 0
    visited[root] = True

    q = deque([root])

    while q:
        parent = q.popleft()  # FIFO

        # Explore neighbors
        nodes = get_neighbors(graph, rows, cols, parent)
        for child in nodes:
            if not visited[child]:
                dist[child] = dist[parent] + 1
                pred[child] = parent
                visited[child] = True
                q.append(child)

    return dist, pred


def get_neighbors(grid, rows, cols, cur_pos):
    """
    Return all possible directions from current position.
    This takes into accounts borders as well as non-empty
    positions.
    """
    nodes = set()  # using set eliminates dups

    if grid[max(cur_pos.x - 1, 0)][cur_pos.y] != 1:  # up
        nodes.add(Pos(max(cur_pos.x - 1, 0), cur_pos.y))

    if grid[cur_pos.x][max(cur_pos.y - 1, 0)] != 1:  # left
        nodes.add(Pos(cur_pos.x, max(cur_pos.y - 1, 0)))

    if grid[cur_pos.x][min(cur_pos.y + 1, cols - 1)] != 1:  # right
        nodes.add(Pos(cur_pos.x, min(cur_pos.y + 1, cols - 1)))

    if grid[min(cur_pos.x + 1, rows - 1)][cur_pos.y] != 1:  # down
        nodes.add(Pos(min(cur_pos.x + 1, rows - 1), cur_pos.y))

    nodes -= {cur_pos}
    return nodes
