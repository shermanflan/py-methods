

def lcs_naive(a, b):
    """
    Longest common subsequence
    LCS Problem Statement: Given two sequences, find the length of
    longest subsequence present in both of them.
    """

    return __recurrence(a, len(a)-1, b, len(b)-1)


def __recurrence(a, i, b, j):
    if i < 0 or j < 0:
        return 0

    if a[i] == b[j]:
        return 1 + __recurrence(a, i-1, b, j-1)
    else:
        length1 = __recurrence(a, i-1, b, j)
        length2 = __recurrence(a, i, b, j-1)

        return max(length1, length2)


def lcs_memo(a, b):
    """
    Memoized, iterative version.
    Builds memo[m+1][n+1] in bottom up fashion
    memo[i][j] contains length of LCS of A[0..i-1] and B[0..j-1]

    O(mn)
    """
    m, n = len(a), len(b)

    # Declare the array for storing the lcs values
    memo = [[None] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):  # O(m)
        for j in range(n + 1):  # O(n)
            if i == 0 or j == 0:
                memo[i][j] = 0
            elif a[i - 1] == b[j - 1]:
                memo[i][j] = memo[i - 1][j - 1] + 1
            else:
                memo[i][j] = max(memo[i - 1][j], memo[i][j - 1])

    # memo[m][n] contains the length of LCS of A[0..n-1] & B[0..m-1]
    return memo[m][n]

