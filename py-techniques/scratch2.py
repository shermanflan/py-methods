from collections import deque, defaultdict, Counter
from itertools import permutations
import math
from crack.tree import BSTNode
import time
from datetime import datetime


def main():

    n = 8
    tmprow = [0] * n    
    tmpDS = [[0] * n for _ in range(0, n)]

    for i in range(0, n):
        print(i)

    print(tmpDS)

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()