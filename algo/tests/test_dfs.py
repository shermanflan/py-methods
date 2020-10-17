from algolib.apply.search.dfs import dfs, dfs_i


def test_dfs(g):
    n_s = g['s']
    pred = dfs(g, n_s)

    # find s to t
    prev = pred['t']
    path = ['t']
    while prev != -1:
        path.append(prev)
        prev = pred[prev]

    assert path[::-1] == ['s', 8, 7, 9, 't']
    assert pred["t"] == 9


def test_dfs_i(g):
    n_s = g['s']
    pred = dfs_i(g, n_s)

    # find s to t
    prev = pred['t']
    path = ['t']
    while prev != -1:
        path.append(prev)
        prev = pred[prev]

    assert path[::-1] == ['s', 8, 7, 9, 't']
    assert pred["t"] == 9
