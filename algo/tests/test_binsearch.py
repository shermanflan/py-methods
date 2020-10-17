

from algolib.apply.search.binarysearch import (
    binary_search_general,
    binary_search_last_false
)


def test_bs():

    arr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

    assert binary_search_general(arr, 'e', lambda x, t: x >= t) == (4, 'e')

    arr = ['a', 'b', 'c', 'd', 'f', 'g', 'h', 'i']

    assert binary_search_general(arr, 'e', lambda x, t: x >= t) == (4, 'f')

    assert binary_search_last_false(arr, 'e', lambda x, t: x >= t) == (3, 'd')
