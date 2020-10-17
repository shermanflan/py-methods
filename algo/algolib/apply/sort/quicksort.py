from random import randint


# TODO: Implement iteratively
# TODO: Implement naive solution (for quick interview recall)
def quick_sort(arr):
    """
    SORT-003
    Quick sort is good in the average case. Not as good on sorted
    or nearly sorted.

    A standard optimization is to use insertion sort on sub-arrays when
    they fall below a minimum size.

    Average: O(n log n)
    Worst: O(n^2) - when pivot does not split evenly
    Best: O(n log n)

    :param arr: input list will be sorted in place.
    :return: None
    """
    def qsort(a, start, end):
        if start < end:
            idx = __pivot(a, start, end)
            pvt = __partition(a, start, end, idx)

            qsort(a, start, pvt-1)
            qsort(a, pvt+1, end)

    qsort(arr, 0, len(arr)-1)


def __partition(arr, start, end, idx):
    """
    Partition the input array into 2 sub-arrays in place. All elements
    less than or equal to the pivot in the left sub-array, and all
    other elements in the right sub-array. Returns the index of the
    pivot point.

    :param arr: input array
    :param start: start of sub-array
    :param end: end of sub-array
    :param idx: index of pivot
    :return: None
    """
    pivot = arr[idx]
    arr[end], arr[idx] = arr[idx], arr[end]

    store = start
    for i in range(start, end):

        # Find and shift smaller elements.
        if arr[i] <= pivot:
            arr[i], arr[store] = arr[store], arr[i]
            store += 1

    # Move pivot back into its place.
    arr[store], arr[end] = arr[end], arr[store]

    return store


def __pivot(arr, i, j):
    """
    Use the median of three values, taken respectively from the
    front, middle, and tail of the array.

    :param start: start of range
    :param end: end of range
    :return: the index of the pivot point
    """
    # randint(start, end) may be an option but has overhead
    mid = (i + j) // 2
    pick3 = [(arr[i], i), (arr[j], j), (arr[mid], mid)]
    return sorted(pick3, key=lambda x: x[0])[1][1]


