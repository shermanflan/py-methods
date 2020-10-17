

def merge_sort(arr):
    """
    SORT-005
    Merge sort is good when needing to a stable sort.

    To sort a collection A, divide it evenly into two smaller collections,
    each of which is then sorted. A final phase merges these two sorted
    collections back into a single collection of size n.

    This implementation requires O(n) extra storage. The copy of the array
    is used as a buffer to sort in place and then is copied into the input
    result array. This is more efficient than generating a new result array
    at each recursive step.

    Average: O(n log n)
    Worst: O(n log n)
    Best: O(n log n)

    :param arr: input list will be sorted in place.
    :return: None
    """
    tmp = arr.copy()
    __merge_sort_array(tmp, arr, 0, len(arr) - 1)


def __merge_sort_array(tmp, result, start, end):
    if start == end:
        return
    if end - start == 1:
        if result[start] > result[end]:
            result[start], result[end] = result[end], result[start]
        return

    # Divide
    mid = (start + end) // 2
    __merge_sort_array(result, tmp, start, mid - 1)
    __merge_sort_array(result, tmp, mid, end)

    # Merge tmp => result
    left, right, target = start, mid, start

    while target <= end:
        if right > end or (left < mid and tmp[left] < tmp[right]):
            result[target] = tmp[left]
            left += 1
        else:
            result[target] = tmp[right]
            right += 1

        target += 1


def merge_sort_iterative(arr):
    """
    Iterative form.
    """
    def merge(src, tgt, start, inc):
        end1 = start + inc
        end2 = min(start + 2*inc, len(src))

        i, j, k = start, start+inc, start

        while i < end1 and j < end2:

            if src[i] < src[j]:
                tgt[k] = src[i]
                i += 1
            else:
                tgt[k] = src[j]
                j += 1

            k += 1

        if i < end1:
            tgt[k:end2] = src[i:end1]
        elif j < end2:
            tgt[k:end2] = src[j:end2]

    from math import ceil, log

    n = len(arr)

    # Calculate runs (height), i.e. how many times will n
    # be split?
    runs = ceil(log(n, 2))
    src, dest = arr, [None]*n

    for run_size in (2**k for k in range(runs)):
        for start_pos in range(0, n, 2*run_size):  # merge each half
            merge(src, dest, start_pos, run_size)

        src, dest = dest, src  # swap, use only 1 copy

    # In case of swaps
    if arr is not src:
        arr = src


def merge_sort_naive(arr):
    """
    :param arr: input list will be sorted in place.
    :return: None
    """
    if len(arr) < 2:
        return

    mid = len(arr)//2
    left = arr[:mid]  # create copies
    right = arr[mid:]
    merge_sort_naive(left)
    merge_sort_naive(right)

    # Merge copies into caller array
    i = j = 0
    while i + j < len(arr):
        if i < len(left) and (j == len(right) or left[i] < right[j]):
            arr[i+j] = left[i]
            i += 1
        else:
            arr[i+j] = right[j]
            j += 1


