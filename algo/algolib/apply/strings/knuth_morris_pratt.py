

# TODO: Not sure if the specifics are worth memorizing
#  but definitely understanding the algorithm and its
#  cost savings at a conceptual level would be helpful.
def kmp(text, pattern, start):
    """
    Knuth-morris-pratt pattern matching algorithm
    Return the lowest index of t at which p begins, or else -1.
    O(n + m)
    """
    assert text and pattern

    n, m = len(text), len(pattern)
    fail = __kmp_fail(pattern)
    j, k = start, 0

    while j < n:

        if text[j] == pattern[k]:
            if k == m-1:
                return j - m + 1
            j += 1
            k += 1
        elif k > 0:
            k = fail[k-1]
        else:
            j += 1

    return -1


def __kmp_fail(pattern):
    """
    Compute failure table which allows already matched text to
    be used.
    """
    end = len(pattern)
    fail = [0]*end
    j, k = 1, 0

    while j < end:

        if pattern[j] == pattern[k]:
            fail[j] == k + 1
            j += 1
            k += 1
        elif k > 0:
            k = fail[k - 1]
        else:
            j += 1

    return fail

