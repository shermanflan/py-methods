from itertools import permutations, combinations

def separateNumbers(s):
    # Complete this function
    if s[0] == s:
        print('NO')
        return

    for i in range(1, len(s)):
        mystack = []
        mystack.append(s[:i])

        while len(''.join(mystack)) < len(s):
            # Pop stack add 1, and then push result
            mystack.append(str(int(mystack[-1]) + 1))

        print(f'{i}, {str(int(mystack[-1]) + 1)}, {mystack}')
        if ''.join(mystack) == s:
            print('YES', mystack[0])
            break
        if i == len(s) - 1:
            print('NO')

print(separateNumbers('891011'))