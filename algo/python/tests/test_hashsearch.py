import pytest

from algolib.apply.search.hashsearch import hash_search


def test_hashsearch():
    arr = ["This", "is", "test", "of", "Hash", "Search"]

    assert hash_search(arr, "Search")


def test_not_hashsearch():
    arr = ["This", "is", "test", "of", "Hash", "Search"]

    assert not hash_search(arr, "Missing")
