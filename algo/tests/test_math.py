from algolib.apply.math.nums import (
    is_prime, is_prime_sieve,
    to_decimal, from_decimal,
    from_decimal2, get_lsb_digits,
    get_msb_digits, gcd, fraction_reduce,
    reverse, split_num, lcm
)


def test_msb_digits():

    n = 123456789

    assert list(get_msb_digits(123456789)) == [1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_lsb_digits():

    n = 123456789

    assert list(get_lsb_digits(123456789)) == [9, 8, 7, 6, 5, 4, 3, 2, 1]


def test_to_decimal():

    assert to_decimal(1011, 2) == 11
    assert to_decimal(110001, 2) == 49


def test_from_decimal():

    assert from_decimal(43, 2) == 101011
    assert from_decimal(49, 2) == 110001
    assert from_decimal2(65535, 16) == 'FFFF'


def test_isprime():

    assert is_prime(2)
    assert not is_prime(4)
    assert is_prime(1091)

    assert is_prime_sieve(20) == [2, 3, 5, 7, 11, 13, 17, 19]


def test_reverse():
    assert reverse(12345) == 54321


def test_split():
    assert split_num(123456, 3) == (123, 456)


def test_gcd():

    assert fraction_reduce(77, 22) == (7, 2)

    assert lcm(14, 21) == 42

    assert lcm(14, 23) == 322

    assert gcd(77, 22) == 11

    assert gcd(3, 7) == 1

    assert gcd(21, 14) == 7
