import math
from collections import deque

class Graph:
    def __init__(self):
        super().__init__()
        self.storage = {}

    def add_vertex(self, id):
        if id in self.storage:
            return False
        self.storage[id] = []
        return True

    def remove_vertex(self, id):
        if id not in self.storage:
            return False
        del self.storage[id]

        # Also, remove references to id
        for k in self.storage.keys():
            if id in self.storage[k]:
                self.storage[k].remove(id)

        return True

    def add_edge(self, id1, id2, directed=True):
        if id1 not in self.storage or id2 not in self.storage:
            return False
        self.storage[id1].append(id2)

        if not directed:
            self.add_edge(id2, id1, directed=True)

        return True

    def remove_edge(self, id1, id2):
        if id1 not in self.storage:
            return False
        self.storage[id1].remove(id2)
        return True

    def is_vertex(self, id):
        if id in self.storage:
            return True
        return False

    def neighbors(self, id):
        if id in self.storage:
            return self.storage[id]

    def bfs(self, id):
        if not self.is_vertex(id):
            raise Exception(f'Invalid vertix: {id}')

        visited = set()
        q = deque()
        q.append(id)
        visited.add(id)

        while q:
            cur = q.popleft()
            print(cur)

            for n in self.neighbors(cur):
                if n not in visited:
                    q.append(n)
                    visited.add(n)

    def dfsIPre(self, id):
        """
        Iterative implementation (pre-order)
        """
        if not self.is_vertex(id):
            raise Exception(f'Invalid vertix: {id}')
        
        stack = []
        visited = set()

        stack.append(id)
        visited.add(id)

        while stack:
            cur = stack.pop()
            print(cur) # pre-order

            for n in self.neighbors(cur):
                if n not in visited:
                    stack.append(n) # like invoking a function recursively
                    visited.add(n)

    def dfsIPost(self, id):
        """
        Iterative implementation (post-order)
        """
        if not self.is_vertex(id):
            raise Exception(f'Invalid vertix: {id}')
        
        stack, results, visited = [], [], {}

        stack.append(id)
        visited[id] = 'pre' # visited but not processed

        while stack:

            cur = stack[-1] # peek

            if visited[cur] == 'pre':
                for n in self.neighbors(cur):
                    if n not in visited:
                        stack.append(n) # like invoking a function recursively
                        visited[n] = 'pre'
                visited[cur] = 'post' # fully processed
            else:
                cur = stack.pop()
                results.append(cur) # post-order

        return results

    def dfsR(self, id):
        """
        Recursive implementation
        """
        if not self.is_vertex(id):
            raise Exception(f'Invalid vertix: {id}')

        visited = set()

        def traverse(node):

            visited.add(node)
            print(node) # pre-order

            for n in self.neighbors(node):
                if n not in visited:
                    traverse(n)

            #print(node) # post-order

        traverse(id)

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    graph = Graph()
    graph.add_vertex(5)
    graph.add_vertex(10)
    graph.add_vertex(15)
    graph.add_vertex(20)
    graph.add_vertex(25)
    graph.add_edge(5, 10, directed=False)
    graph.add_edge(5, 15, directed=False)
    graph.add_edge(5, 20, directed=False)
    graph.add_edge(15, 25, directed=False)

    #graph.dfsIPre(20)
    print('===================')
    print(graph.dfsIPost(20))
    #graph.dfsR(20)
