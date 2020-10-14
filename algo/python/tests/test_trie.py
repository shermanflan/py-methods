
import pytest

from algolib.model.trees.trie import Trie


@pytest.fixture(scope="session")
def trie_a():
    words = ["ABASE", "ABBEY", "ABBOT", "ABDICATE", "ABERRATION",
             "ABHORRENT", "ABJECT", "ABNEGATE", "ABOMINATION",
             "ABORIGINAL", "ABDOMINAL", "ABORT"]

    lookup = Trie()
    for w in words:
        lookup.add(w)

    return lookup


def test_find(trie_a):

    assert trie_a.find("ABB") == 2


def test_not_find(trie_a):

    assert trie_a.find("ZEB") == 0


def test_find_words(trie_a):

    assert trie_a.find_words('ABB') == ['ABBEY', 'ABBOT']
    assert trie_a.find_words('ABO') == ["ABOMINATION", "ABORIGINAL", "ABORT"]


def test_remove_word(trie_a):
    assert trie_a.find("ABORT") == 1
    assert trie_a.remove("ABORT") == "ABORT"
    assert trie_a.find("ABORT") == 0

