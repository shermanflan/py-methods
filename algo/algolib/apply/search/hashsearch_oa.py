from algolib.apply.math.hashing import hashcode


class HashSearchException(Exception):
    pass


# TODO:
# Consider implementing a rehash trigger based on a given load factor.
# Load factor = [elements]/[buckets] => [0.0, 1.0]
class HashSearchOA:

    def __init__(self, arr, buckets=2**9 - 1):

        self.buckets = buckets
        self.__ht = [None] * self.buckets
        self.__ht_d = [False] * self.buckets

        for t in arr:
            b = self.add(t)

    def search(self, elm):
        """
        SEARCH-003
        Hash based search using open addressing.

        Average: O(1)
        Worst: O(n)
        Best: O(1)

        :param elm: element to find
        :return: True if found, else False
        """
        k = hashcode(elm, self.buckets)
        ctr = 1

        while ctr <= self.buckets:
            if self.__ht[k] is None:
                return False

            if self.__ht[k] == elm and not self.__ht_d[k]:
                return True

            # Collision
            k = self.__probe(k)  # find next address
            ctr += 1

        return False

    def add(self, elm):
        """

        :param elm: the element to add
        :return: the probe count if added, else error
        """
        k = hashcode(elm, self.buckets)
        ctr = 1

        while ctr <= self.buckets:
            if self.__ht[k] is None or self.__ht_d[k]:
                self.__ht[k] = elm
                self.__ht_d[k] = False
                return ctr

            # Already there
            if self.__ht[k] == elm and not self.__ht_d[k]:
                return ctr

            # Collision - something else is there
            k = self.__probe(k)  # find next address
            ctr += 1

        raise HashSearchException(f"Could not add {elm} on probing.")

    def delete(self, elm):
        """
        Deletes existing items in the table and handles possibility that
        collisions have occurred.

        :param elm: the element to delete
        :return: the probe count if deleted, else error
        """
        k = hashcode(elm, self.buckets)
        ctr = 1

        while ctr <= self.buckets:
            if not self.__ht[k]:
                raise HashSearchException(f"{elm} does not exist.")

            # Remove
            if self.__ht[k] == elm and not self.__ht_d[k]:
                # TODO: Set to None as well?
                self.__ht_d[k] = True
                return ctr

            # Collision
            k = self.__probe(k)  # find next address
            ctr += 1

        raise HashSearchException(f"Could not delete {elm} on probing.")

    def __probe(self, hk):
        """
        Linear probe. Other variants are possible.

        :param hk: The value to hash
        :return: The hashtable index
        """
        return (hk + 37) % self.buckets
