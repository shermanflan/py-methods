

# TODO: Not sure if this is canonical.
def num_paths(grid):
    """
    Count the paths a robot can traverse in getting from bottom left
    to top right. The robot can only travel up and right. 1 in the
    input matrix represents a blocked path.

    Return the total number of possible paths.
    """
    rows, cols = len(grid), len(grid[0])

    paths = [[0]*cols for _ in range(rows)]
    paths[rows-1][0] = 1

    for row in range(rows-1, -1, -1):  # bottom to top
        for col in range(cols):  # left to right

            if grid[row][col] == 0:

                if col > 0:
                    paths[row][col] += paths[row][col-1]  # path from left
                if row < rows-1:
                    paths[row][col] += paths[row+1][col]  # path from bottom

    return paths[0][cols-1]
