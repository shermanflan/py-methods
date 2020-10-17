import math
from collections import deque, defaultdict

"""
Tree is a graph without cycles.
Binary Search Tree: for each node, left children < node < right children (no dups)
Complete Binary Tree: every level filled, except possibly the last (filled left to right)
Full Binary Tree: every node has 0 or 2 children
Perfect Binary Tree: complete and full binary trees.

In order Binary Traversal: left child, node, right child
Pre-order Binary Traversal: node, left child, right child
Post-order Binary Traversal: left child, right child, node
"""


# TODO: insert, remove operations
# TODO: Balancing operation
class BinaryTree:

    def __init__(self, value=None):
        self.value = value
        self.parent = None
        self.left = None
        self.right = None
        self.height = 0

    def __repr__(self):
        return str(self.value)

    def __eq__(self, other):
        assert isinstance(other, BinaryTree)

        if (self and not other) or (not self and other):
            return False
        if not self and not other:
            return True
        if self.value != other.value:
            return False

        return self.left == other.left and self.right == other.right

    def is_balanced(self):
        """
        Check if tree is balanced.
        The heights of two sub trees of any node doesn't differ by more than 1
        """
        return self.__is_balanced(self)

    def get_height(self):
        return self.__get_height(self)

    def pre_order(self):
        """
        Form of DFS
        Can be used to get the prefix expression of an expression tree.
        Can be used to copy the trees (top down)
        """
        print(self.value)

        if self.left:
            self.left.pre_order()

        if self.right:
            self.right.pre_order()

    def pre_order_iterative(self):
        """
        Use stack. Right node is added before left to maintain pre order
        """
        stack = [self]

        while stack:
            node = stack.pop()

            print(node.value)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)

        return

    def in_order(self):
        """
        """
        if self.left:
            self.left.in_order()

        print(self.value)

        if self.right:
            self.right.in_order()

    def in_order_iterative(self, results):
        """
        Iterative implementation uses stack.
        """
        # Set current to root of binary trees
        stack, cur = [], self

        while True:

            # Reach the left most Node of the current Node
            if cur:
                while cur:
                    # Place node on the stack
                    stack.append(cur)
                    cur = cur.left

            # BackTrack from the empty subtree and visit the Node
            # at the top of the stack; however, if the stack is
            # empty you are done
            else:
                if stack:
                    cur = stack.pop()  # left
                    # print(cur.value)
                    results.append(cur.value)

                    # We have visited the node and its left
                    # subtree. Now, it's right subtree's turn
                    cur = cur.right
                else:
                    break

    def post_order(self):
        """
        Can model a dependency graph, postfix expression of an expression trees.
        Can be used to delete the trees (bottom up)
        :return:
        """
        if self.left:
            self.left.post_order()

        if self.right:
            self.right.post_order()

        print(self.value)

    def post_order_iterative(self):
        """
        Uses 2 stacks. There is also a single stack solution.
        """
        stack1, stack2 = [self], []

        # This takes a similar form as pre_order_iterative.
        while stack1:
            node = stack1.pop()
            stack2.append(node)

            # Left before right (reversed postorder)
            if node.left:
                stack1.append(node.left)
            if node.right:
                stack1.append(node.right)

        while stack2:
            node = stack2.pop()
            print(node.value)

    def create_level_lists(self):
        """
        Create a list for each level in the tree.
        """
        dist, level = {}, defaultdict(list)
        queue = [self]

        dist[self.value] = 0

        while queue:

            cur_node = queue.pop()
            level[dist[cur_node.value]].append(cur_node.value)

            if cur_node.right:
                rc = cur_node.right
                dist[rc.value] = dist[cur_node.value] + 1
                queue.append(rc)

            if cur_node.left:
                lc = cur_node.left
                dist[lc.value] = dist[cur_node.value] + 1
                queue.append(lc)

        return [v for v in level.values()]

    def find_path(self, root, path, target):
        """
        Finds the path from root node to given root of the tree.
        Stores the path in a list path[], returns true if path
        exists otherwise false.

        This uses backtracking to construct the path instead of
        building a complete predecessor dictionary.
        """
        if root is None:
            return False

        # Store this node is path vector. The node will be
        # removed if not in path from root to target
        path.append(root.value)

        # See if the target is same as root's value
        if root.value == target:
            return True

        # Check if target is found in left or right sub-tree
        if self.find_path(root.left, path, target) or \
                self.find_path(root.right, path, target):
            return True

        # Backtrack
        # If not present in subtree rooted with root, remove
        # root from path and return False
        path.pop()
        return False

    def lowest_common_ancestor(self, root, node1, node2):
        """
        This assumes both nodes exist in the binary tree. This
        is very IMPORTANT.
        """
        return self.__lca(root, node1, node2)

    def __lca(self, root, node1, node2):
        if root is None:
            return None

        # If either n1 or n2 matches with root's key, report
        # the presence by returning root (Note that if a key is
        # ancestor of other, then the ancestor key becomes LCA
        if root is node1 or root is node2:
            return root

        # Can either node be reached from LC or RC
        left_node = self.__lca(root.left, node1, node2)
        right_node = self.__lca(root.right, node1, node2)

        # If so, then this is the common ancestor.
        # B/c this is the first time they are both reachable.
        if left_node is not None and right_node is not None:
            return root

        # Otherwise, keep looking in the appropriate branch.
        return left_node if left_node is not None else right_node

    def __is_balanced(self, node):
        if not node:
            return True

        l_height = node.left.height if node.left else 0
        r_height = node.right.height if node.right else 0

        if abs(l_height - r_height) > 1:
            return False

        return self.__is_balanced(node.left) and self.__is_balanced(node.right)

    def __get_height(self, node):

        if not node:
            return 0

        lc = self.__get_height(node.left)
        rc = self.__get_height(node.right)

        node.height = max(lc, rc) + 1

        return node.height
