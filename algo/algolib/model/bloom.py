

"""
A Bloom Filter provides a bit array structure B that ensures constant
performance when adding elements from C into B or checking whether an
element HAS NOT BEEN added to B.

Checking whether an element is in B might return a false positive even
though the element does not exist in C. The Bloom Filter can accurately
determine when an element has not been added to B, so it never returns
a false negative.
"""


class Bloom:
    """
    DATA-002
    Only useful when false positives can be tolerated. Use a Bloom Filter
    to reduce the number of expensive searches by filtering out those that
    are guaranteed to fail—for example, use a Bloom Filter to confirm
    whether to conduct an expensive search over disk-based storage.

    As an another example, a bloom filter could be used as an initial
    duplicate filter in an API. If the filter returns a negative, then the
    value is definitely not a duplicate. However, if a positive is returned,
    then a more expensive database query can be issued.

    Average: O(k)
    Worst: O(k)
    Best: O(k)
    """

    def __init__(self, size=10_000_000, hash_k=None):
        """
        Assumes the existence of k hash functions, each of which takes the
        value to be inserted and the size of the bit array.

        :param size: initial size of bit array
        :param hash_k: the hash functions
        """
        self.bits = 0
        self.size = size

        if not hash_k:
            # TODO: Use a large prime number generator to generate k hash
            #  functions of the form [abs(hash(e))+P]%sz
            # TODO:: Maybe use miller-rabin? See:
            # https://medium.com/@prudywsh/how-to-generate-big-prime-numbers-miller-rabin-49e6e6af32fb
            # TODO: Use pickle to serialize state.
            self.k = 1
            self.hash_k = [lambda e, sz: abs(hash(e))%sz]
        else:
            self.k = len(hash_k)
            self.hash_k = hash_k

    def add_all(self, *argsv):
        """
        Add a list of values.

        :param argsv: List
        :return: None
        """
        for e in argsv:
            self.add(e)

    def add(self, value):
        """
        Uses Python’s ability to work with arbitrarily large “bignum” values.

        :param value: the value to add to the filter.
        :return: None
        """
        for hf in self.hash_k:
            bit = 1 << hf(value, self.size)
            self.bits |= bit

    def __contains__(self, value):
        """
        if any bit position is set to 0, you know the value could not have
        been added, so it returns False. However, if these k bit positions
        are all set to 1, you can only state that the value may have been
        added.

        :param value: check if this value exists
        :return: True or False
        """
        for hf in self.hash_k:
            bit = 1 << hf(value, self.size)

            # Never false negative.
            if self.bits & bit == 0:
                return False

        # May be a false positive.
        return True

