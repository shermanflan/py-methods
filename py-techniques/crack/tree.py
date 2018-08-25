import math

class NTreeNode(object):
    """
    Tree is a graph without cycles.
    Binary Search Tree: for each node, left children <= node < right children
    Complete Binary Tree: every level filled, except possibly the last (filled left to right)
    Full Binary Tree: every node has 0 or 2 children
    Perfect Binary Tree: complete and full binary tree.
    In order Binary Traveral: left child, node, right child
    Pre-order Binary Traversal: node, left child, right child
    Post-order Binary Traversal: left child, right child, node
    Min-head: Complete binary tree where each node is less than its children
    Trie: An n-ary tree where each node stores a single character.
    """
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.children = []

class BTreeNode(object):
    """ Data structure for binary trees. """

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.left = None
        self.right = None
        self.level = None
        self.parent = None

    def __repr__(self):
        return str(self.name)

    @staticmethod
    def createBST(arr):
        ''' Given a sorted array (asc), build a minimal BST. '''
        if not arr: # base case
            return

        mp = len(arr)//2
        root = BTreeNode(arr[mp])
        root.left = BTreeNode.createBST(arr[:mp])
        root.right = BTreeNode.createBST(arr[mp+1:])
        return root

    @staticmethod
    def isBST(root, lo = -math.inf, hi = math.inf):
        ''' 
        Check if a tree is a binary search tree. Uses recursive
        min, max ranges.
        '''
        if not root:
            return True

        if lo < root.name < hi:
            return isBST(root.left, lo, root.name) and isBST(root.right, root.name, hi)
        else:
            return False