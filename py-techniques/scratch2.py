from collections import deque

class Node(object):

    def __init__(self, val):
        super().__init__()
        self.val = val
        self.visited = False
        self.left = None
        self.right = None

    def __str__(self):
        return f'{self.val}'

def buildTree(indexes):
    root = Node(1)
    tr = deque(indexes)
    todo = deque()
    todo.append(root)

    while todo:
        n = todo.popleft()
        cN = tr.popleft()
        n.left = Node(cN[0]) if cN[0] != -1 else None
        n.right = Node(cN[1]) if cN[1] != -1 else None

        if n.left:
            todo.append(n.left)
        if n.right:
            todo.append(n.right)

    return root

def inOrderTraversal(node):
    return inOrderRecurse(node, [])

def inOrderRecurse(node, l):

    if node.left:
        inOrderRecurse(node.left, l)

    l.append(node.val)

    if node.right:
        inOrderRecurse(node.right, l)

    return l

def printTree(node):
    offset = 0
    level = 0
    todo = deque()
    todo.append(node)
    printQ = []

    while todo:
        tmp = [n for n in todo]
        todo.clear()
        printQ.append([n.val for n in tmp])
        #print(f'Q: {printQ}')

        for n in tmp:
            if n.left:
                todo.append(n.left)
            elif n.val != -1:
                todo.append(Node(-1))
            if n.right:
                todo.append(n.right)
            elif n.val != -1:
                todo.append(Node(-1))
    
    for l, nodes in enumerate(printQ[0:-1]):
        print(f'{l} {nodes}')

def swapNodes(indexes, queries):
    pass

n = 11 #int(input())

indexes = []

tree = [(2 , 3)
        , (4 , -1)
        , (5 , -1)
        , (6 , -1)
        , (7 , 8)
        , (-1 , 9)
        , (-1 , -1)
        , (10 , 11)
        , (-1 , -1)
        , (-1 , -1)
        , (-1 , -1)]

for i in range(n):
    indexes.append(list(tree[i]))

node = buildTree(indexes)

print(f'IOT: {inOrderTraversal(node)}')
printTree(node)

#result = swapNodes(indexes, [2, 4])