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
        self.value = None
        self.neighbors = []
        self.state = NodeState.UNDISCOVERED

    def __repr__(self):
        return f'{self.name}|{self.value}'

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
        self.bipartite = False
        self.time = 0 # global ts
        self.ancestors = []

    def __repr__(self):
        res = ''
        for k, v in self.vertex.items():
            res += f"{k}: {', '.join(map(str, v.neighbors))}\n"

        return res

    def reset(self):
        self.nvertices = 0
        self.nedges = 0
        self.directed = False
        self.bipartite = False
        self.time = 0
        self.ancestors = []

        for k, v in self.vertex.items():
            v.state = NodeState.UNDISCOVERED
            v.value = None

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

        if v2 in self.vertex:
            node2 = self.vertex[v2]
        else:
            node2 = edgenode(v2)
            self.vertex[v2] = node2
        
        node1.neighbors.append(node2)
        self.degree[v1] += 1

        # Also, add v2 to v1 edge.
        if not directed: 
            self.insertedge(v2, v1, True)

    def bfs(self, key):
        """
        Standard breadth first search is useful in shortest path problems.
        """
        if key not in self.vertex:
            raise Exception('Invalid vertex.')

        root = self.vertex[key]
        if root.state != NodeState.UNDISCOVERED: # already searched
            return

        root.state = NodeState.DISCOVERED
        q = deque()
        q.append(root)

        while q:
            node = q.popleft()
            # Process early
            self.processearly(node)

            for child in node.neighbors:
                if child.state != NodeState.PROCESSED:
                    # Process edge here (e.g. weight, color, etc.)
                    self.processedge(node, child)
                if child.state == NodeState.UNDISCOVERED:
                    q.append(child)
                    child.state = NodeState.DISCOVERED

            # Or, process late
            self.processlate(node)
            node.state = NodeState.PROCESSED

    def dfs(self, key):
        """
        """
        if key not in self.vertex:
            raise Exception('Invalid vertex: {key}')

        node = self.vertex[key]
        node.state = NodeState.DISCOVERED
        node.value = (self.time, None) # entry, exit
        self.processearly(node)

        self.time += 1
        for c in node.neighbors:
            self.processedge(node, c)
            if c.state == NodeState.UNDISCOVERED:
                self.dfs(c.name)
                self.processedge(node, c)
            elif c.state != NodeState.PROCESSED:
                self.processedge(node, c)
        
        node.state = NodeState.PROCESSED
        node.value = (node.value[0], self.time) # entry, exit
        self.processlate(node)
        self.time += 1

    def processearly(self, n):
        #self.nvertices += 1 # some action
        #print(f'V: {n}')
        pass

    def processedge(self, p, c):
        self.nedges += 1 # some action

        # 2-coloring
        #self.color(p, c)

    def processlate(self, n):
        # some action
        print(f'V: {n}')

    def countconnected(self):
        """
        Count connected components in a graph.
        """
        self.reset()
        count = 0

        for k, v in self.vertex.items():
            if v.state == NodeState.UNDISCOVERED:
                self.bfs(k)
                count += 1

        return count

    def color(self, p, c):
        if p.value == c.value:
            self.bipartite = False

        if p.value == 'White':
            c.value = 'Black' 
        elif p.value == 'Black':
            c.value = 'White'
        else:
            c.value = 'Uncolored'

    def twocolor(self):
        """
        Returns True if the graph can be colored with 2 colors.
        A bipartite graph is split in two colors where adjacent nodes
        cannot have the same color.
        """
        self.reset()
        self.bipartite = True
        
        # Initialize
        for k, v in self.vertex.items():
            v.value = 'Uncolored'

        for k, v in self.vertex.items():
            if v.state == NodeState.UNDISCOVERED:
                v.value = 'White'
                self.bfs(k)
        
        return self.bipartite

if __name__ == '__main__':

    with open(r"C:\Users\rguzman\Desktop\TMP\graphtest.txt", "r", encoding="utf-8") as f:
        g = graph()
        g.directed = False

        #g.vertex['F'] = edgenode('F') # unconnected

        n, m = map(int, f.readline().rstrip().split())

        for i in range(m):
            ln = f.readline().rstrip()
            
            # Skip comments
            if ln[0] == '#': continue

            v1, v2 = ln.split()
            g.insertedge(v1, v2, g.directed)

        #print(g)
        #g.bfs('A')
        g.reset()
        g.dfs('A')
        #print(g.countconnected())
        #print(g.twocolor())
