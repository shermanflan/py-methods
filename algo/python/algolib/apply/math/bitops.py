class BitMath(object):
    """
    TODO
    - Is x a power of 2: x & (x-1) == 0
    - Clear least significant set bit: x = x & (x-1)
        - Can be used to count 1's in a number by repeating in a loop until zero
    -

    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_bit(n, ith):
        return (n & (1 << ith)) != 0

    @staticmethod
    def set_bit(n, ith):
        return n | (1 << ith)

    @staticmethod
    def clear_bit(n, ith):
        return n & ~(1 << ith)

    @staticmethod
    def clear_msb(n, ith):
        return n & ((1 << ith) - 1)

    @staticmethod
    def clear_lsb(n, ith):
        return n & (-1 << (ith + 1))

    @staticmethod
    def update_bit(n, ith, val):
        """
        val should be True or False.

        :param n:
        :param ith:
        :param val:
        :return:
        """
        erasebit = BitMath.clear_bit(n, ith - 1)
        newbit = (1 if val else 0) << (ith - 1)
        return erasebit | newbit

    # TODO: Reverse a number using binary
    @staticmethod
    def reverse(n):
        rev = 0

        # traversing bits of 'n' from the right
        while n > 0:

            # bitwise left shift 'rev' by 1
            rev <<= 1

            # if current bit is '1'
            if (n & 1) == 1:
                rev ^= 1

            # bitwise right shift 'n' by 1
            n >>= 1

        return rev

    # TODO: Rotate a binary number

    # TODO: Add binary numbers

    # TODO: Count 1's or 0's in a binary number
