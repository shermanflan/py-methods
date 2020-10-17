from collections import defaultdict


class Node(object):
    """Singly/Doubly linked"""

    def __init__(self, data):
        super().__init__()
        self.data = data
        self.prev = None
        self.next = None

    def __str__(self):  # like ToString
        return str(self.data)


# TODO:
# Opt1: Adding and maintaining self.tail would make append more efficient.
# Opt2: Adding and maintaining self.count would make size() more efficient.
# Opt4: Create a doubly linked list class.
class LinkedList(object):
    """Wrapper for node"""
    def __init__(self, data):
        self.head = Node(data)
        self.tail = self.head  # todo
        self.length = 1

    # TODO: Add test case
    def get(self, pos):
        """

        :param pos: 0-based index
        :return:
        """
        assert 0 <= pos < self.length, "Out of bounds"

        i, cur = 0, self.head

        while i < pos and cur:
            cur = cur.next
            i += 1

        return cur

    def insert(self, data):
        newHead = Node(data)
        newHead.next = self.head
        self.head = newHead
        self.length += 1

    # TODO: Add test case
    def insert_at(self, data, pos):
        """

        :param data:
        :param pos: 0-indexed
        :return:
        """
        assert data
        assert 0 <= pos < self.length, "Out of bounds"

        if pos == 0:
            self.insert(data)
            return

        i, cur = 0, self.head

        while i < pos - 1 and cur:
            cur = cur.next
            i += 1

        if cur:
            data.next = cur.next
            cur.next = data

        self.length += 1

    def append(self, data):
        end = Node(data)

        return self._append_node(end)

    def _append_node(self, data):
        tmp = self.head

        while tmp.next:
            tmp = tmp.next

        tmp.next = data
        self.length += 1
        return tmp.next

    # Opt1: Adding and tracking a prev variable simplifies logic
    def delete(self, data):
        assert data

        if self.head.data == data:
            self.head = self.head.next

        tmp = self.head

        while tmp.next:
            if tmp.next.data == data:
                tmp.next = tmp.next.next
                break

            tmp = tmp.next

        self.length -= 1

    def delete_at(self, pos):
        """

        :param pos: 0-indexed
        :return:
        """
        cur = self.head
        i = 0

        while i < pos - 1 and cur:
            cur = cur.next
            i += 1

        if not cur and i < pos - 1:
            raise Exception("Linked list bounds exceeded.")

        tmp = cur.next
        cur.next = cur.next.next
        tmp.next = None

        return tmp

    @staticmethod
    def find_middle(ll):
        """ In one pass """
        start = ll.head
        startplus2 = ll.head

        while startplus2 and startplus2.next:
            start = start.next
            startplus2 = startplus2.next.next

        return start

    # TODO: Recursive
    def nth_to_last(self, n):
        assert n >= 0, "nth position must be >= 0"

        if self.head is None:
            return None

        pos1, pos2 = self.head, None
        i, cur = 0, self.head

        while i < n and cur:
            cur = cur.next
            i += 1

        if i < n:
            raise Exception("nth position longer than list")

        pos2 = cur

        while pos2.next:
            pos1 = pos1.next
            pos2 = pos2.next

        return pos1

    def is_cycle(self):
        turtle = self.head
        hare = self.head

        while hare and hare.next:
            turtle = turtle.next
            hare = hare.next.next

            if turtle == hare:
                return True

        return False

    def find_cycle_start(self):
        turtle = self.head
        hare = self.head

        while hare and hare.next:
            turtle = turtle.next
            hare = hare.next.next

            if turtle == hare:  # found cycle
                break

        if hare and hare.next:  # let's find start
            turtle = self.head

            while True:
                turtle = turtle.next
                hare = hare.next
                if turtle == hare:
                    return turtle

        return None

    # TODO: Recursively
    @staticmethod
    def reverse(ll):
        """ In one pass, no stack
            See: https://www.geeksforgeeks.org/reverse-a-linked-list/
        """

        prev, curr, nxt = None, ll.head, None

        while curr:
            # Save next
            nxt = curr.next

            # Point to previous (initially None)
            curr.next = prev

            # Move forward
            prev = curr
            curr = nxt

        return prev

    @staticmethod
    def distinct(ll):
        """
        Deduplicate in one pass, sorted or unsorted.
        """
        prev, curr = None, ll.head
        dups = set()

        while curr:
            if curr.data in dups:  # seen before
                prev.next = curr.next  # delete
            else:
                dups.add(curr.data)
                prev = curr  # will be initialized here

            curr = prev.next

        return ll

    @staticmethod
    def to_list(node):
        tmp = node
        result = []

        while tmp:
            result.append(tmp.data)

            tmp = tmp.next

        return result

    def __iter__(self):
        cur = self.head

        while cur:
            yield cur
            cur = cur.next

    def __str__(self):  # like ToString
        tmp = self.head
        s = ''

        if self.isCycle():
            return 'Cycle detected!'

        while tmp != None:
            s += str(tmp) + ' => '
            tmp = tmp.next

        return s + 'Null'
