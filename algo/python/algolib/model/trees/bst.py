from collections import deque
import math

from algolib.model.trees.tree import BinaryTree

"""
Use a binary search trees to store dynamic sets when:

1. You must traverse the model in ascending (or descending) order.

2. The model set size is unknown, and the implementation must be able to
handle any possible size that will fit in memory.

3. The model set is highly dynamic, and there will be many insertions
and deletions during the collection’s lifetime.
"""


class BinarySearchTree(BinaryTree):
    """
    SEARCH-004
    A BST ensures the following property:
    If k is the key for inner node n, then all keys in n.left <= k and
    all keys in n.right >= k.

    To achieve O(log n), you must balance the trees to avoid a skewed trees
    that has a few branches that are much longer than the other branches.

    Average: O(log n)
    Worst: O(log n)
    Best: O(log n)
    """
    # TODO: Create self.root, use composition with BinaryTree.
    def __init__(self, value):
        super().__init__(value)

    def add_all(self, *argsv):
        for e in argsv:
            self.add(e)

    def add(self, value):
        """
        Inserts into the proper place via recursion.

        :param value: the value to insert
        :return: None
        """
        self.__insert(self, value)

        return self

    def remove(self, value):
        return self.__remove(self, value)

    def add_iterative(self, value):

        cur, new_node = self, BinarySearchTree(value)

        while cur:

            if value <= cur.value:
                if cur.left:
                    cur = cur.left
                else:
                    new_node.parent = cur
                    cur.left = new_node
                    return self
            if value > cur.value:
                if cur.right:
                    cur = cur.right
                else:
                    new_node.parent = cur
                    cur.right = new_node
                    return self

        raise Exception("Unknown error.")

    @staticmethod
    def is_bst(root):
        """
        Check if a trees is a binary search trees. Uses recursive
        min, max ranges.

        :param root:
        :return:
        """
        def is_bounded(node, lo=-math.inf, hi=math.inf):

            if not node:
                return True

            if lo <= node.value <= hi:
                return is_bounded(node.left, lo, node.value) and \
                       is_bounded(node.right, node.value, hi)
            else:
                return False

        return is_bounded(root)

    @staticmethod
    def create_bst(arr):
        """
        Given a sorted array (asc), build a BST.

        Time: O(n)
        Space: O(n) in the case of skewed binary trees.
        Slicing the array is expensive. It is better to pass
        the left and right bounds into recursive calls instead.

        :param arr:
        :return:
        """
        def convert(left, right):

            if left > right:
                return None

            mid = (left + right) // 2
            node = BinarySearchTree(arr[mid])
            node.left = convert(left, mid - 1)
            node.right = convert(mid + 1, right)

            return node

        return convert(0, len(arr) - 1)

    def __insert(self, root, value):
        """
        Recursively finds the right place to add the value.

        :param root:
        :param value: new value to add
        :return: None
        """
        if value <= root.value:
            if root.left:
                self.__insert(root.left, value)
            else:
                new_node = BinarySearchTree(value)
                new_node.parent = root
                root.left = new_node
        else:
            if root.right:
                self.__insert(root.right, value)
            else:
                new_node = BinarySearchTree(value)
                new_node.parent = root
                root.right = BinarySearchTree(value)

    def __remove(self, root, key):

        queue = deque()
        queue.append(root)

        while queue:

            cur = queue.popleft()

            if cur.value == key:
                break
            if cur.left:
                queue.append(cur.left)
            if cur.right:
                queue.append(cur.right)

        if not cur or cur.value != key:
            return False  # does not exist

        # Case 1: No children so just delete node
        if cur.parent and not cur.left and not cur.right:
            if cur is cur.parent.left:
                cur.parent.left = None
            else:
                cur.parent.right = None
            cur.parent = None
        # Single node case
        elif not cur.left and not cur.right:
            raise NotImplementedError("Need to refactor")

        # Case 2: Node has just one child so skip over node
        # (like linked list delete)
        if cur.parent and (not cur.left or not cur.right):
            if cur is cur.parent.left:
                cur.parent.left = cur.left if cur.left else cur.right
            else:
                cur.parent.right = cur.left if cur.left else cur.right

            cur.parent = None
        elif not cur.left or not cur.right:  # root with child case
            raise NotImplementedError("Need to refactor")

        # Case 3: Node has 2 children.
        if cur.left and cur.right:
            # Find min in right subtree. This is the next consecutive value.
            min_node = self.__min_node(cur.right)

            # Replace with found min (by value)
            cur.value = min_node.value

            # Delete the duplicate in the right tree
            self.__remove(cur.right, min_node.value)

        return True

    def __min_node(self, root):
        cur_node = root

        # Min is left-most node.
        while cur_node.left:
            cur_node = cur_node.left

        return cur_node

    def __contains__(self, item):
        """
        Iteratively checks for existence.

        :param item: the value to search
        :return: True or False
        """
        node = self

        while node:

            if item < node.value:
                node = node.left
            elif item > node.value:
                node = node.right
            else:
                return True

        return False
