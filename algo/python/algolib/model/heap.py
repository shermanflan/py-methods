

class HeapNode(object):

    def __init__(self, key, value, location=None):
        self.key = key
        self.val = value
        self.location = location

    def __lt__(self, other):
        assert isinstance(other, HeapNode), "Invalid HeapNode type comparison."

        return self.key < other.key

    def __repr__(self):
        return f"{self.key}: {self.val} @{self.location}"


# TODO: Implement an n-ary heap where n > 2
class Heap:
    """
    DATA-001:
    A min heap is a binary tree with 2 properties:

    1. Nodes have to be added from left to right. No gaps.
    2. Each node has a value that is less than or equal to its children.

    A heap is stored in an array.

    1. The left child of a node at index i is 2*i + 1.
    2. The right child is at 2*i + 2.
    3. For a node i (non-root), its parent is floor((i - 1)/2).
    """

    def __init__(self):
        self.items = []

    def from_array(self, items):
        """
        Bottom-up heap construction from sequence of k,v tuples.

        O(n)
        """
        for i, v in enumerate(items):
            self.items.append(HeapNode(v[0], v[1], i))

        if len(self.items) > 1:
            self.__heapify(len(self.items) - 1)

        return self.items

    def add(self, key, value):
        """
        Add to heap and ensure heap property is maintained.

        O(log N)

        :return:
        """
        token = HeapNode(key, value, len(self.items))
        self.items.append(token)
        self.__bubble_up(len(self.items)-1)

        return token

    def update(self, locator, new_key, new_val):
        j = locator.location
        assert 0 <= j < len(self.items) and self.items[j] is locator,\
            "Invalid locator provided"
        locator.key = new_key
        locator.val = new_val
        self.__bubble(j)

        return new_key, new_val

    def remove(self, locator):
        j = locator.location
        assert 0 <= j < len(self.items) and self.items[j] is locator,\
            "Invalid locator provided"

        if j == len(self.items) - 1:
            tmp = self.items.pop()
        else:
            self.__swap(j, -1)
            tmp = self.items.pop()
            self.__bubble(j)

        return tmp.key, tmp.val

    def remove_min(self):
        """
        O(log N)

        :return:
        """
        assert len(self.items) > 0, "Empty heap."

        min_tmp = self.items[0]
        self.__swap(0, -1)
        self.items.pop()
        self.__bubble_down(0, len(self.items)-1)

        return min_tmp.key, min_tmp.val

    def peek_min(self):
        assert len(self.items) > 0, "Empty heap."

        return self.items[0].key, self.items[0].val

    def is_empty(self):
        return len(self.items) == 0

    def __heapify(self, end_idx):
        """
        Bottom up construction. Similar to heapq.heapify.

        O(n)
        """
        start_idx = (end_idx-1)//2

        for idx in range(start_idx, -1, -1):
            self.__bubble_down(idx, end_idx)

    def __bubble(self, index):
        parent = (index - 1)//2

        if index > 0 and self.items[index] < self.items[parent]:
            self.__bubble_up(index)
        else:
            self.__bubble_down(index, len(self.items) - 1)

    def __bubble_up(self, child):
        """
        O(log N): proportional to height of tree
        """
        while child >= 0:

            parent = (child - 1) // 2

            if parent >= 0 and self.items[parent] > self.items[child]:
                self.__swap(parent, child)

            # Repeat
            child = parent

    def __bubble_down(self, start, end):
        """
        O(log N): proportional to height of tree
        """

        while start < end:

            min_idx = start
            lc = 2 * start + 1
            rc = 2 * start + 2

            if lc <= end and self.items[lc] < self.items[min_idx]:
                min_idx = lc

            if rc <= end and self.items[rc] < self.items[min_idx]:
                min_idx = rc

            if min_idx != start:
                self.__swap(start, min_idx)

                start = min_idx
            else:  # invariant reestablished
                break

    def __swap(self, i, j):
        self.items[i].location = j
        self.items[j].location = i

        self.items[i], self.items[j] = self.items[j], self.items[i]
