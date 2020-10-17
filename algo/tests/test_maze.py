
from algolib.apply.search.maze import Pos, solve


def test_maze_search():
    maze = [
        [0, 0, 0, 0],
        [1, 1, 1, 0],
        [0, 0, 0, 0],
        [1, 1, 1, 1]
    ]

    start = Pos(0, 0)

    distances, paths = solve(maze, start)

    assert distances[(2, 0)] == 8
    assert paths[(2, 0)] == (2, 1)
