import math

from algolib.apply.dynpro.coin_change import (
    coin_sum
)
from algolib.apply.dynpro.count_paths import num_paths
from algolib.apply.dynpro.lcs import (
    lcs_naive, lcs_memo
)
from algolib.apply.dynpro.levenshtein import (
    edit_naive, edit_memo
)
from algolib.apply.dynpro.lis import (
    lis_naive, lis
)

def test_coin_change():
    assert coin_sum([1, 5, 10], 10) == 1
    assert coin_sum([1, 5, 2], 10) == 2
    assert coin_sum([1, 3, 5, 7], 9) == 3
    assert coin_sum([2, 4, 6], 7) == math.inf


def test_lcs():

    assert lcs_naive('AGGTAB', 'GXTXAYB') == 4
    assert lcs_naive('ABCDGH', 'AEDFHR') == 3

    assert lcs_memo('AGGTAB', 'GXTXAYB') == 4
    assert lcs_memo('ABCDGH', 'AEDFHR') == 3


def test_levenshtein():

    assert edit_naive('geek', 'gesek') == 1
    assert edit_naive('cat', 'cut') == 1
    assert edit_naive('sunday', 'saturday') == 3
    assert edit_naive('apples', 'snapple') == 3

    assert edit_memo('geek', 'gesek') == 1
    assert edit_memo('cat', 'cut') == 1
    assert edit_memo('sunday', 'saturday') == 3
    assert edit_memo('apples', 'snapple') == 3


def test_numpaths():
    maze = [
        [0, 0, 0, 0]
        ,[0, 0, 0, 1]
        ,[0, 0, 0, 0]
        , [0, 0, 0, 0]
    ]

    assert num_paths(maze) == 10


def test_lis():

    assert lis('JMCNDOPAB') == list('JMNOP')
