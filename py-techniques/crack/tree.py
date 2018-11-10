import math
from collections import deque

class NTreeNode(object):
    """
    Tree is a graph without cycles.
    Binary Search Tree: for each node, left children < node < right children (no dups)
    Complete Binary Tree: every level filled, except possibly the last (filled left to right)
    Full Binary Tree: every node has 0 or 2 children
    Perfect Binary Tree: complete and full binary tree.
    In order Binary Traveral: left child, node, right child
    Pre-order Binary Traversal: node, left child, right child
    Post-order Binary Traversal: left child, right child, node
    Min-heap/priority queue: Complete binary tree where each node is less than its children
    Trie: An n-ary tree where each node stores a single character.
    """
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.children = []

# To Do: Try both iterative and recursive algos.
class BSTNode(object):
    """ Data structure for binary trees. """

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.left = None
        self.right = None

    def __repr__(self):
        return str(self.name)

    @staticmethod
    def add(root, val):
        ''' Find leaf insertion point. Assume insertion value is unqiue.
        '''
        if not root: # empty
            root = BSTNode(val)
        else:
            if val < root.name:
                if root.left:
                    BSTNode.add(root.left, val)
                else: # found leaf
                    root.left = BSTNode(val)
            else:
                if root.right:
                    BSTNode.add(root.right, val)
                else: # found leaf
                    root.right = BSTNode(val)

    # To Do: Remove operation
    # To Do: Balancing operation

    def preOrder(self):
        ''' Form of DFS
            Can be used to get the prefix expression of an expression tree.
            Can be used to copy the tree (top down)
        '''
        print(self.name)

        if self.left:
            self.left.preOrder()
        
        if self.right:
            self.right.preOrder()

    def preOrderI(self):
        """ Use stack. Right node is added before left to maintain pre order
        """
        stack = []

        stack.append(self)

        while stack:
            node = stack.pop()

            print(node.name)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)

        return

    def inOrder(self):
        """ Form of DFS
        """
        if self.left:
            self.left.inOrder()

        print(self.name)
        
        if self.right:
            self.right.inOrder()

    def inOrderI(self):
        """ Form of DFS
            Iterative implementation uses stack.
        """
        # Set current to root of binary tree 
        stack, cur = [], self 
      
        while True: 
          
            # Reach the left most Node of the current Node 
            if cur: 
              
                # Place node on the stack  
                stack.append(cur) 
                cur = cur.left  
          
            # BackTrack from the empty subtree and visit the Node 
            # at the top of the stack; however, if the stack is  
            # empty you are done 
            else: 
                if stack: 
                    cur = stack.pop() 
                    print(cur.name) 
          
                    # We have visited the node and its left  
                    # subtree. Now, it's right subtree's turn 
                    cur = cur.right  
  
                else: 
                    break

    def postOrder(self):
        ''' Form of DFS
            Can model a dependency graph, postfix expression of an expression tree.
            Can be used to delete the tree (bottom up)
        '''
        if self.left:
            self.left.postOrder()
        
        if self.right:
            self.right.postOrder()

        print(self.name)

    def postOrderI(self):
        """ Uses 2 stacks. There is also a single stack soln.
        """
        stack1, stack2 = [], []

        stack1.append(self)

        # This takes a simillar form as preOrderI.
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
            print(node)

    def find(self, val):
        if val == self.name:
            return val
        elif val < self.val:
            return self.left.find(val)
        
        return self.right.find(val)

    @staticmethod
    def createBST(arr):
        ''' Given a sorted array (asc), build a minimal BST. '''
        if not arr: # base case
            return

        mp = len(arr)//2
        root = BSTNode(arr[mp])
        root.left = BSTNode.createBST(arr[:mp])
        root.right = BSTNode.createBST(arr[mp+1:])
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
            return BSTNode.isBST(root.left, lo, root.name) and BSTNode.isBST(root.right, root.name, hi)
        else:
            return False