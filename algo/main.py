"""
Sorting:
    - Quick Select (Hoare)
Trees:
    - Implement 1 example of a self-balancing trees (AVL, Red-Black, etc)
    - cartesian tree
    - Segment tree
    - Binary indexed tree (Fenwick tree)
Heaps:
    - Use min and max heap to return the median efficiently (support insert/delete)
    - segment trees
Graphs:
    - Find Eulerian path, cycle
    - Find k-nearest neighbors (friends of friends)
    - Find shortest path
        - weighted, undirected graph: dijkstra's algo
    - maximum flow / minimum cut
        - Ford-Fulkerson
    - maximum bipartite matching
    - Transitive closure:
        - Floyd-Warshall
    - range minimum query
    - Disjoint Set Union / Union Find
        - Find connected components in graph
Canonical problems to know
- Know regex (sub, match)
- Calculator - using stack, trees/postfix
- Implement checkers, chess
- Implement an LRU/Circular Buffer
- Implement a hash table, hash function
- Find # of 0/1 islands in a matrix: connected graphs, bfs
- Basic python file i/o (opening a file, reading a file...)
Dynamic programming
- Knapsack Problem: (NP-Hard)
    - 0-1: Dynamic programming algorithm O(n*W) - "pseudo-polynomial"
- ZigZag
Special math to know
- Understand the math behind hashing, and how to build an efficient hash
- How number bases work
- Rotate a matrix
- Formulas for summing infinite series
- Know bit manipulation
    - especially 2's complement
        - https://www.youtube.com/watch?v=4qH4unVtJkE
    - palindrome
        - https://www.geeksforgeeks.org/check-binary-representation-number-palindrome/
    - fractions to binary
        - https://andybargh.com/binary-fractions/
- Rules of logarithms
"""
from algolib.model.graphs.sparse import *
from algolib.apply.search.bfs import *
from algolib.apply.graph.topo_sort import *
from algolib.model.heap import *
from algolib.apply.graph.dijkstra import *


if __name__ == '__main__':

    flights = Graph(directed=False)

    f_0 = flights.add_vertex('0')
    f_1 = flights.add_vertex('1')
    f_2 = flights.add_vertex('2')

    # {'1': 0 = > 1, '2': 1 = > 2}
    flights.add_edge(f_0, f_1, weight=6)
    flights.add_edge(f_0, f_2, weight=6)
    flights.add_edge(f_1, f_2, weight=1)

    cloud = shortest_path(flights, flights["0"])
    tree = build_shortest_path_tree(flights, flights["0"], cloud)

    print(tree)
