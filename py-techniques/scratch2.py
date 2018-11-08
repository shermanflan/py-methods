from collections import deque, defaultdict, Counter


def main():

    s1 = 'ricardozricardoz'
    
    letters = Counter(s1)

    for c in letters:

        if letters[c] == 1:
            print(c)
            break

    else:
        print(None)
    
    
if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()