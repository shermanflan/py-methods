
"""
Trees:
    - Implement 1 example of a self-balancing trees (AVL, Red-Black, etc)
    - cartesian tree

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

Canonical problems to know
- Know regex (sub, match)
- Basic UNIX utility commands (grep, sed, etc.)
- Calculator - using stack, trees/postfix
- Implement an LRU/Circular Buffer
- Know how to build a lexer/parser (CFG/RegEx)
- Implement a hash table, hash function
- TSP (NP-Hard): no known polynomial time algorithm
- Find # of 0/1 islands in a matrix: connected graphs, bfs
- Basic python file i/o (opening a file, reading a file...)

Dynamic programming
- Knapsack Problem: (NP-Hard)
    - Conceptually like shopping spree where the cart is the knapsack
    and maximizing total value is the goal.
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

    pass
