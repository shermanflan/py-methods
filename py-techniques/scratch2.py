from itertools import combinations, permutations, combinations_with_replacement

def splitNumber(n, splitAt):

    d, n2, i = None, 0, 0

    while n > 0 and i < splitAt:
        d = n%10
        n2 = d*pow(10, i) + n2
    
        print(d, n, n2, i)

        n //= 10

        i += 1

    return (n, n2)

n, splitAt = 123456789, 5
print(splitNumber(n, splitAt))
