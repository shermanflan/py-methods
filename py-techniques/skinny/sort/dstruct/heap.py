#
# A priority queue can be implemented using a heap or an array of size n where:
# left child = 2*index + 1
# right child = 2*index + 2
# parent = (index - 1)//2
#
# Priority queues can be min-heaps or max-heaps.
#
class minheap(object):

    def __init__(self, l):
        super().__init__()

        self.maxsize = len(l)
        self.n = 0 # next open slot
        self.arr = [None]*self.maxsize

        #self.makeheap(l)
        self.makeheap2(l)

    def parent(self, i):
        """
        Assume zero-indexed.
        """
        if i < 1:
            return -1

        return (i-1)//2

    def lchild(self, i):
        return 2*i + 1

    def rchild(self, i):
        return 2*i + 2

    def makeheap(self, l):
        for n in l: # O(n)
            self.insert(n) # O(log n)

    def makeheap2(self, l):
        """
        Faster method uses bubbledown.
        """
        self.n = len(l)

        for i, e in enumerate(l): # O(n)
            self.arr[i] = e

        for j in range(self.n, 0, -1): # O(n)
            self.bubbledown(j-1) # O(log n)

    def insert(self, x):
        if self.n + 1 > self.maxsize:
            raise Exception('Size overflow.')

        # Heapify
        self.arr[self.n] = x
        self.bubbleup(self.n)
        self.n += 1

    def bubbleup(self, i):
        """
        O(log n)
        """
        p = self.parent(i)

        if p < 0:
            return

        if self.arr[i] < self.arr[p]:
            self.arr[i], self.arr[p] = self.arr[p], self.arr[i]
            self.bubbleup(p)
    
    def bubbledown(self, i):
        """
        O(log n)
        """
        lc = self.lchild(i)
        minidx = i

        # Find smallest among p, lc, rc.
        for s in range(2):
            if lc + s < self.n: # boundary
                if self.arr[lc + s] < self.arr[minidx]:
                    minidx = lc + s

        if minidx != i: # out of order
            self.arr[i], self.arr[minidx] = self.arr[minidx], self.arr[i]
            self.bubbledown(minidx)

    def getmin(self):
        if self.n <= 0:
            raise Exception('Empty heap.')

        lo = self.arr[0]
        self.arr[0] = self.arr[self.n-1]

        # Heapify
        self.n -= 1
        self.bubbledown(0)

        return lo

