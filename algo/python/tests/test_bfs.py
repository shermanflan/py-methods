from algolib.apply.search.bfs import bfs, bfs_level


def test_bfs(g):
    pred, dist = bfs(g, g['s'])

    # find s to t
    prev = pred['t']
    path = ['t']
    while prev != -1:
        path.append(prev)
        prev = pred[prev]

    assert path[::-1] == ['s', 8, 7, 9, 't']
    assert pred["t"] == 9
    assert dist["t"] == 4


def test_levels(g5):
    root = g5[0]
    pred, dist, levels = bfs_level(g5, root)

    assert levels[0] == [0]
    assert levels[1] == [1, 2]
    assert levels[2] == [3, 4]
