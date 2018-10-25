from itertools import combinations
from collections import defaultdict, Counter

# Complete the countTriplets function below.
def countTriplets(arr, r):
    triples = 0
    left = defaultdict(int)
    right = Counter(arr)
    
    # left = current/r, right = current * r
    for n in arr:

        #print('L{0}: {1}'.format(n, left))
        #print('R{0}: {1}'.format(n, right))

        # Decrement right (in use)
        right[n] -= 1

        if n%r == 0:
            n3 = right[n*r]
            n1 = left[n//r]
            triples += n1*n3

        left[n] += 1
        
    return triples

# File harness
try:

    with open("C:\\Users\\rguzman\\Desktop\\test.txt", "r", encoding="utf-8") as f:
        n, r = list(map(int, f.readline().rstrip().split()))

        nums = list(map(int, f.readline().rstrip().split()))
    
    results = countTriplets(nums, r)
    print(results)

except Exception as e:
    print(e)