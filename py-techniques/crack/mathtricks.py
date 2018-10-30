from functools import reduce

def reverseNum(n):
    """ Reverses a number """
    reverse = 0
    
    while n > 0:
        lastdigit = n%10
        reverse = reverse*10 + lastdigit # make room for digit (shift left)
        n //= 10 # next digit
    
    return reverse

def splitNumber(n, splitAt):

    digit, n2, i = None, 0, 0

    while n > 0 and i < splitAt:
        digit = n%10
        n2 = digit*pow(10, i) + n2 # move digit to the left

        n //= 10
        i += 1

    return (n, n2)

def lcm(a, b):
    """
    https://en.wikipedia.org/wiki/Least_common_multiple
    """

    return (a/gcd(a, b)) * b

def gcd(a, b):
    """
    Euclid's algo
    https://en.wikipedia.org/wiki/Greatest_common_divisor
    """
    if a == 0:
        return b
    if b == 0:
        return a

    while a > 0 and b > 0:
        if a > b:
            a = a - b
        elif b > a:
            b = b - a
        else:
            break

        #print(f'p:{a},{b}')
        #debug += 1
    return a

print(reduce(gcd, [10, 18, 36]))
print(reduce(lcm, [7, 6, 5, 9]))

# Multiply list elements
print(reduce(lambda x, y: x*y, [1, 2, 3]))