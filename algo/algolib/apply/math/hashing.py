"""
A good hashing function computes a polynomial from the symbols of the
input string modulo a prime number. For example, if you have a string
with symbols S = S1 S2 ... Sn, the hash function would compute:

    H(S) = (S1 * A^(n-1) + S2 * A^(n-2) + ... + [Sn-1] * A + Sn) mod P.

Some presentation of the symbols as numbers needs to be used and a value
for A is to be chosen. The prime number P gives you the size of the
resulting set of values.
"""


def hashcode(elm, buckets):
    """
    A hash function should have good distribution and should be quick
    to compute with respect to machine cycles.

    :param elm: input element
    :param buckets: number of buckets
    :return: Return bucket index
    """
    return abs(hash(elm)) % buckets
