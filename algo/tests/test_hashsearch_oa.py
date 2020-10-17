import pytest

from algolib.apply.search.hashsearch_oa import HashSearchOA


@pytest.fixture(scope="session")
def hash_oa():
    arr = ["This", "is", "test", "of", "Hash", "Search",
           "but", "with", "more", "elements"]

    return HashSearchOA(arr)


def test_search(hash_oa):

    assert hash_oa.search("elements")


def test_not_search(hash_oa):

    assert not hash_oa.search("missing")


def test_delete(hash_oa):
    hash_oa.add("twenty-one")

    assert hash_oa.search("twenty-one")

    hash_oa.delete("twenty-one")

    assert not hash_oa.search("twenty-one")

    hash_oa.add("twenty-one")

    assert hash_oa.search("twenty-one")
