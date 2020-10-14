import pytest

from algolib.model.linkedlist import LinkedList


def test_delete_at(ll2):
    ll2.delete_at(2)

    assert ll2.to_list(ll2.head) == [1, 2, 4, 5]


def test_nth_to_last(ll):

    assert ll.nth_to_last(2).data == 7


def test_find_middle(ll):
    mid = LinkedList.find_middle(ll)

    assert mid.data == 5


def test_is_cycle(ll_cycle):
    assert ll_cycle.is_cycle()


def test_find_cycle_start(ll_cycle):
    start = ll_cycle.find_cycle_start()

    assert start.data == 4


def test_reverse(ll_reverse):
    rev = LinkedList.reverse(ll_reverse)

    assert LinkedList.to_list(rev) == [5, 4, 3, 2, 1]


def test_distinct(ll_distinct2):
    set_ll = LinkedList.distinct(ll_distinct2)

    assert LinkedList.to_list(set_ll.head) == [1, 2]


def test_iterator(ll):
    it = iter(ll)

    assert next(it).data == 1

    next(it)
    next(it)

    assert next(it).data == 4

    n = 0
    for _ in ll:
        n += 1

    assert n == 9
