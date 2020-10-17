from math import inf


# TODO: Not sure this is the canonical example.
# TODO: Is this is the same of 0-1 Knapsack except maximizing vals?
def coin_sum(coins, total):
    """
    Given a list of N coins, their values (V1, V2, … , VN), and the
    total sum S. Find the minimum number of coins the sum of which
    is S (we can use as many coins of one type as we want), or
    report that it’s not possible to select coins in such a way that
    they sum up to S.
    """
    mins = [inf for _ in range(total+1)]
    mins[0] = 0  # base case
    coin = sorted(coins)

    for sum_i in range(1, total+1):
        for c_i in coin:

            if c_i <= sum_i and \
                    1 + mins[sum_i - c_i] < mins[sum_i]:
                mins[sum_i] = 1 + mins[sum_i - c_i]

    return mins[total]
