from collections import deque

class Graph(object):
    """
    Can be directed or undirected.
    Can have cycles or not (acyclic).
    Can be connected, in which all nodes are connected, or not.
    """
    def __init__(self, *args):
        super().__init__()
        self.nodes = list(args)
    
    def reset(self):
        for n in self.nodes:
            n.visited = False

class GraphNode(object):
    """
    """
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.children = []
        self.visited = False

    def __repr__(self):
        return f'{str(self.name)}'

def DFS(root):
    """
    Depth first search: start at node, then traverse each branch before moving on to the neighbor.
    """
    if not root:
        return
    root.visited = True
    print(root)

    for n in root.children:
        if not n.visited:
            DFS(n)

def BFS(root):
    """
    Breadth first search: start at node, then traverse each neighbor before moving on to the children.
    Generally better for finding a path between nodes.
    """
    q = deque()
    root.visited = True

    q.append(root)

    while q:
        r = q.popleft()
        print(r)

        for c in r.children:
            if not c.visited:
                c.visited = True
                q.append(c)