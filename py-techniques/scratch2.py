from collections import deque, defaultdict, Counter
from itertools import permutations
import math
from crack.tree import BSTNode

def search(arr, val):
    print(arr)
    if not arr:
        return -1

    mid = len(arr)//2

    if val == arr[mid]:
        return (mid, val)
    elif val < arr[mid]:
        return search(arr[0:mid], val)
    else:
        return search(arr[mid+1:], val)

def main():

    print(search([1, 2, 3, 4, 5, 6, 7, 8, 9], 10))

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()