from collections import defaultdict, deque
from enum import Enum

class NodeState(Enum):
    UNDISCOVERED = 1
    DISCOVERED = 2
    PROCESSED = 4

class edgenode(object):
    """
    Adjacency lists (vs Adjaceny Matrices) are the right data structure
    for most applications.
    """
    def __init__(self, label):
        super().__init__()
        self.name = label
        self.neighbors = []
        self.state = NodeState.UNDISCOVERED

    def __repr__(self):
        return f'{self.name}'

class graph(object):
    """
    """
    def __init__(self):
        super().__init__()
        self.vertex = {}
        self.degree = defaultdict(int) # out-degree of each vertex
        self.nvertices = 0
        self.nedges = 0
        self.directed = False

    def __repr__(self):
        res = ''
        for k, v in self.vertex.items():
            res += f"{k}: {','.join(map(str, v.neighbors))}\n"

        return res

    def insertedge(self, v1, v2, directed=True):
        """
        From v1 to v2.
        """
        node1, node2 = None, None
        if v1 in self.vertex:
            node1 = self.vertex[v1]
        else:
            node1 = edgenode(v1)
            self.vertex[v1] = node1
            self.nvertices += 1

        if v2 in self.vertex:
            node2 = self.vertex[v2]
        else:
            node2 = edgenode(v2)
            self.vertex[v2] = node2
            self.nvertices += 1
        
        node1.neighbors.append(node2)
        self.degree[v1] += 1
        self.nedges += 1

        # Also, add v2 to v1 edge.
        if not directed: 
            self.insertedge(v2, v1, True)

    def bfs(self, v):
        """
        Standard breadth first search is useful in shortest path problems.
        """
        if v not in self.vertex:
            raise Error('Invalid vertex.')

        root = self.vertex[v]
        root.state = NodeState.DISCOVERED
        q = deque()
        q.append(root)

        while q:
            node = q.popleft()
            print(f'BFS: {node}') # Process early

            for child in node.neighbors:
                if child.state == NodeState.UNDISCOVERED:
                    q.append(child)
                    child.state = NodeState.DISCOVERED

            # Or, process late
            node.state = NodeState.PROCESSED

if __name__ == '__main__':

    with open(r"C:\Users\ricardogu\Desktop\TMP\graphtest.txt", "r", encoding="utf-8") as f:
        g = graph()
        g.directed = False

        n, m = map(int, f.readline().rstrip().split())

        for i in range(m):
            v1, v2 = f.readline().rstrip().split()
            g.insertedge(v1, v2, g.directed)

        print(g)
        print(f'V: {g.nvertices}')
        print(f'E: {g.nedges}')
        print(f'out-D: {g.degree}')
        g.bfs('A')
