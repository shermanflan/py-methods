from algolib.apply.math.hashing import hashcode


def hash_search(arr, elm, buckets=2**9-1):
    """
    SEARCH-002
    In Hash-Based Search the n elements of a collection C are first
    loaded into a hash table H with b bins structured as an array.
    This pre-processing step has O(n) performance. Once all elements
    have been inserted, searching for an item t becomes a search for
    t within H[hash(t)].

    The size of H is typically chosen to be a prime number to ensure
    that using the % modulo operator efficiently distributes the
    computed bin numbers (2**k - 1).

    Average: O(1)
    Worst: O(n)
    Best: O(1)

    :param arr: input List
    :param elm: element to find in arr
    :param buckets: number of buckets to use in hashtable
    :return: True if found, else False
    """
    ht = __build_table_list(buckets, arr)
    bucket = ht[hashcode(elm, buckets)]

    if bucket and elm in bucket:
        return True

    return False


def __build_table_list(buckets, arr):
    """
    Uses list to handle collisions. Open addressing is a variation
    which does not require additional linked list storage.

    :param buckets: the number of buckets
    :param arr: the input array
    :return: List of sz empty buckets
    """
    from collections import defaultdict

    ht = defaultdict(list)

    for elm in arr:
        hc = hashcode(elm, buckets)
        ht[hc].append(elm)

    return ht
