from math import floor

from algolib.apply.sort.insertionsort import insertion_sort


# TODO: Not sure these are the correct variations.
def bucket_sort(arr):
    """
    SORT-004
    Bucket sort is good when drawing from a universally dense set. A good
    example is sorting floats in range(0, 1) which is assumed by this
    algorithm. Basic idea is to not use comparison between elements as the
    basis for sorting but instead to use the elements as keys into a hash map
    which can then be combined into the output sorted array.

    Use in the following conditions:

    1. Uniform model distribution. N buckets are created to evenly
    partition the input range.
    2. Ordered hash function. The buckets are ordered.

    Given a set of n elements, Bucket Sort constructs a set of n
    ordered buckets into which the elements of the input set are
    partitioned.

    Average: O(n)
    Worst: O(n)
    Best: O(n)

    :param arr: input list will be sorted in place.
    :return: None
    """
    idx, n = 0, len(arr)

    # Typically use linked list for each bucket
    buckets = [[] for _ in range(n)]

    # Partition
    for i in range(n):

        # Hash normalizes the value in [0, buckets)
        k = floor(arr[i]*n)
        buckets[k].append(arr[i])

    # Extract
    for i in range(n):
        # Sort elements hashed to same bucket
        insertion_sort(buckets[i])  # O(n log n)?

        for e in buckets[i]:
            arr[idx] = e
            idx += 1


def hash_sort(array, k=5):
    """
    Hash Sort variation creates N buckets of K size up front.
    Works well when model is evenly distributed.
    """

    # Determine minimum and maximum values
    min_elm = min(array)  # O(n)?
    max_elm = max(array)  # O(n)?

    # Initialize buckets
    n = (max_elm - min_elm)//k + 1  # even sized
    buckets = [[] for _ in range(n)]

    # Distribute input array values into buckets
    for i in range(len(array)):
        buckets[(array[i] - min_elm)//n].append(array[i])

    # Sort buckets and place back into new array
    array = []
    for i in range(n):
        buckets[i].sort()  # O(n log(n))?
        array.extend(buckets[i])

    return array


