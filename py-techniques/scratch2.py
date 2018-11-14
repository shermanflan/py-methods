from collections import deque, defaultdict, Counter
from itertools import permutations
import math
from crack.tree import BSTNode


def main():

    s = '{[ []] ]'
    tokens = s.replace(' ', '')
    tokens = list(tokens)

    brace = []

    for b in tokens:

        if b in ('{', '[', '('):
            brace.append(b)
        elif b == ')':
            if brace[-1] == '(':
                brace.pop()
            else:
                print(False)
                break
        elif b == ']':
            if brace[-1] == '[':
                brace.pop()
            else:
                print(False)
                break
        elif b == '}':
            if brace[-1] == '{':
                brace.pop()
            else:
                print(False)
                break
        else:
            raise Exception('Invalid symbol!')
    else:
        print(True)

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()