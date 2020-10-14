

def lis(arr):
    """
    Longest increasing sub-sequence.
    Iterative O(n**2)
    """
    # Track longest sequence ending at arr[pos].
    len_memo = [0]*len(arr)
    len_memo[0] = 1  # base case, first element

    # Track previous element in sequence.
    prev = {arr[0]: -1}

    # End index of longest subsequence.
    best_index = 0

    for pos in range(1, len(arr)):

        len_memo[pos] = 1  # first time
        prev[arr[pos]] = -1  # start of sequence

        for start in range(pos):
            if arr[start] < arr[pos] and len_memo[start]+1 > len_memo[pos]:
                # We can improve length
                len_memo[pos] = len_memo[start] + 1
                prev[arr[pos]] = start

                # Track longest sequence so far.
                if len_memo[pos] > len_memo[best_index]:
                    best_index = pos

    longest_list = [arr[best_index]]
    cur = prev[arr[best_index]]

    while cur != -1:
        longest_list.append(arr[cur])
        cur = prev[arr[cur]]

    return longest_list[::-1]


# TODO:
def lis_naive(arr):
    """
    O(2**n)
    """
    pass