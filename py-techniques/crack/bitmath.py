class bitmath(object):
    """description of class"""

    def __init__(self):
        super().__init__()

    @staticmethod
    def getBit(n, ith):
        return (n & (1 << ith)) != 0

    @staticmethod
    def setBit(n, ith):
        return (n | (1 << ith))

    @staticmethod
    def clearBit(n, ith):
        return (n & ~(1 << ith))

    @staticmethod
    def clearMSBBits(n, ith):
        return (n & ((1 << ith) - 1))

    @staticmethod
    def clearLSBBits(n, ith):
        return (n & (-1 << (ith + 1)))

    @staticmethod
    def updateBit(n, ith, val):
        ''' val should be True or False. '''
        eraseBit = bitmath.clearBit(n, ith)
        newBit = (1 if val else 0) << ith
        return eraseBit | newBit

    # TODO
    def decimalToBinary(n):
        pass

    # TODO: Reverse a number using binary

    # TODO: Add binary numbers

    # TODO: Count 1's or 0's in a binary number