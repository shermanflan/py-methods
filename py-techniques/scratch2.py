from collections import deque, defaultdict, Counter
import math
import time
from datetime import date
import os.path


def main():
    """
    """
    S = set([9, 5, 3, 4, 100, 1])
    x = 10
    seen = set()

    for n in S:
        if x - n in seen:
            print(True, n, x-n)
            break
        
        seen.add(n)
    else:
        print(False)
                 

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()