from collections import deque, defaultdict, Counter
from itertools import permutations

def permute(s, s2):
    st1 = deque(s)

    for i in range(1, len(s) + 1):
        st1.rotate(i)
        tmpr = ''.join(st1)
        print(tmpr)
        if tmpr == s2:
            return True

    return False

def main():

    s1 = 'amazon'
    s2 = 'zonama'
    
    print(permute(s1, s2))   
    
if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()