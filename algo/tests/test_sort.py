from algolib.apply.sort.insertionsort import insertion_sort
from algolib.apply.sort.quicksort import quick_sort
from algolib.apply.sort.mergesort import merge_sort, merge_sort_naive, \
                                        merge_sort_iterative
from algolib.apply.sort.heapsort import heap_sort_py, \
                                        heap_sort_inplace
from algolib.apply.sort.bucketsort import bucket_sort, hash_sort
from algolib.apply.sort.radixsort import radix_sort


def test_insertion_sort():
    test = [21, 4, 1, 3, 9, 20, 25, 6, 21, 14]
    save = test.copy()

    insertion_sort(test)

    assert test == sorted(save)


def test_quick_sort():
    test = [21, 4, 1, 3, 9, 20, 25, 6, 21, 14]
    save = test.copy()

    quick_sort(test)

    assert test == sorted(save)


def test_merge_sort():
    test = [21, 4, 1, 3, 9, 20, 25, 6, 21, 14]
    save = test.copy()

    merge_sort(test)

    assert test == sorted(save)


def test_merge_sort_naive():
    test = [21, 4, 1, 3, 9, 20, 25, 6, 21, 14, 2, 11]
    save = test.copy()

    merge_sort_naive(test)

    assert test == sorted(save)


def test_merge_sort_iter():
    test = [21, 4, 1, 3, 9, 20, 25, 6, 21, 14, 2, 11]
    save = test.copy()

    merge_sort_iterative(test)

    assert test == sorted(save)


def test_hash_sort():
    test = [21, 4, 1, 3, 9, 20, 25, 6, 21, 14, 2, 11]
    save = test.copy()

    tmp = hash_sort(test)

    assert tmp == sorted(save)


def test_bucket_sort():

    from random import random

    test = [random() for _ in range(1000)]
    save = test.copy()

    bucket_sort(test)

    assert test == sorted(save)


def test_heap_sort_py():
    test = [21, 4, 1, 3, 9, 20, 25, 6, 21, 14]
    save = test.copy()

    assert heap_sort_py(test) == sorted(save)


def test_heap_sort_inplace():
    test = [21, 4, 1, 3, 9, 20, 25, 6, 21, 14]
    save = test.copy()
    heap_sort_inplace(test)

    assert test == sorted(save)


def test_radix_sort():

    arr = [170, 45, 75, 90, 802, 24, 2, 66]
    radix_sort(arr)

    assert arr == [2, 24, 45, 66, 75, 90, 170, 802]
