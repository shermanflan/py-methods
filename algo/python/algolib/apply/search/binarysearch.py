

class DoesNotExistError(Exception):
    pass


def binary_search(arr, t):
    """
    SEARCH-001
    Formally, given an array A and a target value, return the index
    of the first element in A equal to OR GREATER than the target value.

    Binary Search divides the problem size approximately in half every
    time it executes the loop. This algorithm is useful if the input
    collection is already sorted. If the collection is dynamic, then
    using a binary search trees is more appropriate.

    At the end of the loop, mid contains the index where the element is
    and low contains the index where it should be inserted if it does
    not exist in the collection.

    Average: O(log n)
    Worst: O(log n)
    Best: O(log n)

    :param arr: sorted List
    :param t: element to find in arr
    :return: True if found, else False
    """
    low, hi = 0, len(arr)-1

    while low <= hi:
        mid = (low + hi)//2  # only for positive n

        if t < arr[mid]:
            hi = mid - 1
        elif t > arr[mid]:
            low = mid + 1
        else:
            return True

    return False


def binary_search_general(arr, target, p: lambda x, t: x >= t):
    """
    General form (first True)
    At the end of the loop, lo contains the index where the first element
    satisfying the predicate exists.
    """
    lo, hi = 0, len(arr)-1

    while lo < hi:
        # The following is more accurate than (lo+hi)//2, which only works
        # if all numbers in S are > 0.
        mid = lo + (hi-lo)//2

        if p(arr[mid], target):
            # Discard 2nd half of Search Space but keep mid
            # as it may be the first satisfying P.
            hi = mid
        else:
            # P(mid) is False so exclude it as well as first half.
            lo = mid + 1

    if not p(arr[lo], target):
        raise DoesNotExistError(f"P({target}) is False for all e in arr.")

    return lo, arr[lo]  # contains least x for which P is True


def binary_search_last_false(arr, target, p: lambda x, t: x >= t):
    """
    Alternate form (last False)
    At the end of the loop, lo contains the index where the last element
    not satisfying the predicate exists.
    """
    lo, hi = 0, len(arr)-1

    while lo < hi:
        # Always round up.
        mid = lo + (hi-lo+1)//2

        if p(arr[mid], target):
            # Discard 2nd half of Search Space including mid.
            hi = mid - 1
        else:
            # P(mid) is False so include it as well as last half.
            lo = mid

    if p(arr[lo], target):
        raise DoesNotExistError(f"P({target}) is True for all e in arr.")

    return lo, arr[lo]  # contains greatest x for which P is False
