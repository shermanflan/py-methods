

def edit_naive(str1, str2):
    """
    Find minimum number of edits (operations) required to convert
    ‘str1’ into ‘str2’.
    """
    memo = {}

    def edits(a, b, i, j):

        if i >= len(a):
            return len(b) - j

        if j >= len(b):
            return len(a) - i

        if a[i] == b[j]:
            return edits(a, b, i + 1, j + 1)

        if (i, j) in memo:
            return memo[(i, j)]
        else:
            inserts = edits(a, b, i + 1, j + 1)
            deletes = edits(a, b, i, j + 1)
            memo[(i, j)] = 1 + min([inserts, deletes])

        return memo[(i, j)]

    return edits(str1, str2, 0, 0)


def edit_memo(str1, str2):
    m, n = len(str1), len(str2)
    memo = [[0]*(n+1) for _ in range(m+1)]

    for row in range(m + 1):
        for col in range(n + 1):

            # If first string is empty, only option is to
            # insert all characters of second string
            if row == 0:
                memo[row][col] = col

            # If second string is empty, only option is to
            # remove all characters of second string
            elif col == 0:
                memo[row][col] = row

            # If last characters are same, ignore last char
            # and recur for remaining string
            elif str1[row-1] == str2[col-1]:
                memo[row][col] = memo[row-1][col-1]

            # If last character are different, consider all
            # possibilities and find minimum
            else:
                ins = memo[row][col-1]
                rem = memo[row-1][col]
                rep = memo[row-1][col-1]

                memo[row][col] = 1 + min(ins, rem, rep)

    return memo[m][n]
