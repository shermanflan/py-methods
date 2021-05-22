from functools import reduce

from math import (
    sqrt, log10, floor, ceil
)
"""
print(reduce(gcd, [10, 18, 36]))
print(reduce(lcm, [7, 6, 5, 9]))
print(reduce(lambda x, y: x * y, [1, 2, 3]))
"""


# TODO: Not sure this is completely accurate.
def fraction_reduce(num, den):
    """
    Take the fraction and reduce to lowest terms.
    4/16 => 1/4
    """
    gcd_frac = gcd(num, den)

    num //= gcd_frac
    den //= gcd_frac

    return num, den


def get_msb_digits(n):
    num_digits = floor(log10(n))
    degree_of_10 = 10**num_digits

    while n > 0:

        div, n = divmod(n, degree_of_10)
        degree_of_10 //= 10

        yield div


def get_lsb_digits(n):

    while n > 0:
        yield n%10
        n //= 10


def to_decimal(n, b):
    """
    Convert to decimal from any base.
    """
    assert 2 <= b <= 10

    result, multiplier = 0, 1

    while n > 0:
        result += (n % 10) * multiplier  # get lsd
        multiplier *= b
        n //= 10

    return result


def from_decimal(n, b):
    """
    Convert from decimal to a number in any base.
    """
    assert 2 <= b <= 10

    result, multiplier = 0, 1

    while n > 0:
        result += (n % b) * multiplier  # extract lsb by base
        multiplier *= 10
        n //= b

    return result


def from_decimal2(n, b):
    """
    Convert from decimal to a number in any base.
    """
    assert 2 <= b <= 20
    chars = "0123456789ABCDEFGHIJ"
    result = ""

    while n > 0:
        result = chars[n%b] + result
        n //= b

    return result


def is_prime(n):
    """
    Naive
    """
    if n <= 1:
        return False
    if n == 2:
        return True
    if n%2 == 0:  # evens are not prime
        return False

    for i in range(3, ceil(sqrt(n)), 2):
        if n%i == 0:
            return False

    return True


def is_prime_sieve(n):
    """
    Sieve of Eratosthenes
    O(n * log log n)
    """
    prime = [True]*(n+1)

    prime[0] = False
    prime[1] = False

    for i in range(2, ceil(sqrt(n))):
        if prime[i]:
            # Set all multiples of i to False
            for k in range(i*i, n+1, i):
                prime[k] = False

    return [n for n, v in enumerate(prime) if v]


def reverse(n):
    """ Reverses a number """
    rev = 0

    while n > 0:
        lsd = n % 10
        rev = rev * 10 + lsd  # make room for digit (shift left)
        n //= 10  # get next digit

    return rev


def split_num(n, pos):
    lsd, n2, i = None, 0, 0

    while n > 0 and i < pos:
        lsd = n % 10
        n2 = lsd * pow(10, i) + n2  # move digit to the left

        n //= 10
        i += 1

    return n, n2


def gcd(a, b):
    """
    Euclid's algo
    https://en.wikipedia.org/wiki/Greatest_common_divisor
    """
    if a == 0:
        return b
    if b == 0:
        return a

    # 25, 15 = 5
    while a > 0 and b > 0:
        if a > b:
            a -= b  # 5
        elif b > a:
            b -= a  # 5
        else:
            break

    return a


def lcm(a, b):
    """
    https://en.wikipedia.org/wiki/Least_common_multiple
    """
    return (a / gcd(a, b)) * b


# TODO
def prime_factors(n):
    pass


def is_power_of_two(self, n):
    """
    For a number to be a power of two, there must only be one bit that is a 1.
    We can use the following bit manipulation trick to determine this:

    n & (n - 1)

    Here's an example why:
    0000 1000 = n
    0000 0111 = n-1
    0000 0000 = n & n-1, result = 0
    """
    if n is None:
        raise TypeError('n cannot be None')
    if n <= 0:
        return False
    return (n & (n - 1)) == 0