import math
from collections import deque

# O (n^2)
def climbingLeaderboard(scores, alice):
    output = []

    # 1. For each of Alice's marks
    for mark in alice: # O(n)
        # 2. Add Alice's mark to scores array
        scores_copy = scores[:]
        scores_copy.append(mark)

        # 3. Convert to Set
        scores_set = set(scores_copy)

        # 4. Sort array
        sorted_marks = sorted(list(scores_set), reverse=True)

        # 5. Lookup Alice's position in the array and return it.
        # O(n)
        alice_rank = [i+1 for i, p in enumerate(sorted_marks) if p == mark]
        output.append(alice_rank[0])

    return output

if __name__ == '__main__':
    scores = [100, 90, 90, 80, 75, 60]
    alice = [50, 65, 77, 90, 102]

    result = climbingLeaderboard(scores, alice)

    print(result)

