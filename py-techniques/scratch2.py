from collections import deque
from crack import stack as st
from crack import queue as q
from crack import graph as g
from crack import tree as t
from crack import linkedlist as ll
import time
import math

def printBST(root):
    if not root:
        return
    
    printBST(root.left)

    print(f'{root}, {root.level}')
    
    printBST(root.right)


a1 = [ 1, 2, 3, 4, 5, 6, 7 ]
#bst1 = t.BTreeNode.createBST(a1)

n1 = t.BTreeNode(1)
n2 = t.BTreeNode(2)
n3 = t.BTreeNode(3)
n4 = t.BTreeNode(4)
n5 = t.BTreeNode(5)
n6 = t.BTreeNode(6)
n7 = t.BTreeNode(7)

n4.left = n2
n4.right = n6
n2.parent = n4
n2.left = n1
n2.right = n3
n1.parent = n2
n3.parent = n2
n6.parent = n4
n6.left = n5
n6.right = n7
n5.parent = n6
n7.parent = n6

printBST(n4)
