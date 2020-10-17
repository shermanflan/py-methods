

from algolib.model.heap import Heap


def heap_sort_inplace(arr):
    """
    SORT-002
    Heap sort is good when needing to avoid worst case behavior. Not
    a stable sort.

    Requires the use of a Heap model structure. This implementation is
    similar to selection sort. In-place version using max heap.

    Requires the use of a Heap model structure. Creates 2 sub-arrays.

    1. Unsorted sub-array which gets smaller and re-heaped.
    2. Sorted sub-array which gets larger by taking the max from the
    max heap sub-array.

    Average: O(n log n)
    Worst: O(n log n)
    Best: O(n log n)

    :param arr: input list
    :return: None
    """
    build_heap(arr)  # max heap
    n = len(arr)

    for i in range(n - 1, 0, -1):
        # Move largest to sorted sub-array.
        arr[0], arr[i] = arr[i], arr[0]

        # Heapify unsorted sub-array
        heapify_down(arr, 0, i)


def build_heap(arr, cmp=lambda x, y: x > y):  # max
    """

    :param cmp: the comparison function
    :param arr: input list is converted into a heap in place.
    :return: None
    """
    n = len(arr)
    for i in range((n - 1)//2, -1, -1):  # start in the middle
        heapify_down(arr, i, n, cmp)


def heapify_down(arr, idx, sz, priority=lambda x, y: x > y):
    """
    Recursively builds a heap from the input array.

    :param arr: the input list
    :param idx: position of current element
    :param sz: size of the input list
    :param priority: function comparator returning bool
    :return: None
    """
    elm = idx
    left_child = 2 * idx + 1
    right_child = 2 * idx + 2

    # Find highest priority
    if left_child < sz and priority(arr[left_child], arr[idx]):
        elm = left_child

    if right_child < sz and priority(arr[right_child], arr[elm]):
        elm = right_child

    if elm != idx:  # swap
        arr[idx], arr[elm] = arr[elm], arr[idx]
        heapify_down(arr, elm, sz, priority)


# TODO: Add version using builtin heapq.
def heap_sort_py(arr):
    """
    SORT-002
    This implementation is similar to selection sort and used
    the built in heapq module (min heap).

    Average: O(n log n)
    Worst: O(n log n)
    Best: O(n log n)

    :param arr: input list
    :return: None
    """
    from heapq import heappush, heappop

    h = []
    for value in arr:  # create heap
        heappush(h, value)

    # Repeatedly pop min and re-heapify.
    return [heappop(h) for _ in range(len(h))]