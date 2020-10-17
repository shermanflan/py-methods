from algolib.model.graphs.sparse import *
from algolib.model.linkedlist import LinkedList
from algolib.model.trees.bst import BinarySearchTree

import pytest


"""
BST
"""


@pytest.fixture(scope="function")
def bst_1():
    arr = [1, 2, 3, 4, 5, 6, 7]
    return BinarySearchTree.create_bst(arr)


@pytest.fixture(scope="session")
def bst_2():
    arr = [1, 2, 3, 4, 5, 6, 7]
    return BinarySearchTree.create_bst(arr)


@pytest.fixture(scope="session")
def bst_3():
    arr = [1, 2, 3, 4, 5, 6, 7]
    return BinarySearchTree.create_bst(arr)


@pytest.fixture(scope="function")
def bst_4():
    root = BinarySearchTree(4)
    n1 = BinarySearchTree(1)
    n2 = BinarySearchTree(2)
    n3 = BinarySearchTree(3)
    n5 = BinarySearchTree(5)
    n6 = BinarySearchTree(6)
    n7 = BinarySearchTree(7)

    root.left = n2
    root.right = n6
    n2.left = n1
    n2.right = n3
    n6.left = n5
    n6.right = n7
    n7.right = BinarySearchTree(8)

    return root


"""
Lists
"""


@pytest.fixture(scope="session")
def ll():
    ll = LinkedList(1)
    ll.append(2)
    ll.append(3)
    ll.append(4)
    ll.append(5)
    ll.append(6)
    ll.append(7)
    ll.append(8)
    ll.append(9)

    return ll


@pytest.fixture(scope="session")
def ll2():
    ll = LinkedList(1)
    ll.append(2)
    ll.append(3)
    ll.append(4)
    ll.append(5)

    return ll


@pytest.fixture(scope="function")
def ll_cycle():

    ll = LinkedList(1)
    ll.append(2)
    ll.append(3)
    tmp = ll.append(4)
    ll.append(5)
    ll.append(6)
    ll.append(7)
    ll.append(8)
    n9 = ll.append(9)

    n9.next = tmp

    return ll


@pytest.fixture(scope="session")
def ll_reverse():
    ll = LinkedList(1)
    ll.append(2)
    ll.append(3)
    ll.append(4)
    ll.append(5)

    return ll


@pytest.fixture(scope="session")
def ll_distinct2():
    ll = LinkedList(1)
    ll.append(2)
    ll.append(1)
    ll.append(2)
    ll.append(1)

    return ll


"""
Graphs
"""


@pytest.fixture(scope="session")
def g():

    graph_test = Graph(directed=True)

    n_s = graph_test.add_vertex("s")
    n_7 = graph_test.add_vertex(7)
    n_8 = graph_test.add_vertex(8)
    n_9 = graph_test.add_vertex(9)
    n_t = graph_test.add_vertex("t")

    graph_test.add_edge(n_s, n_8)
    graph_test.add_edge(n_7, n_9)
    graph_test.add_edge(n_8, n_7)
    graph_test.add_edge(n_9, n_t)

    return graph_test


@pytest.fixture(scope="session")
def g2():

    graph_test2 = Graph(directed=True)

    n_0 = graph_test2.add_vertex('s')
    n_1 = graph_test2.add_vertex(1)
    n_2 = graph_test2.add_vertex(2)
    n_3 = graph_test2.add_vertex(3)
    n_4 = graph_test2.add_vertex(4)
    n_5 = graph_test2.add_vertex(5)

    graph_test2.add_edge(n_0, n_1, weight=6)
    graph_test2.add_edge(n_0, n_2, weight=8)
    graph_test2.add_edge(n_0, n_3, weight=18)
    graph_test2.add_edge(n_1, n_4, weight=11)
    graph_test2.add_edge(n_2, n_3, weight=9)
    graph_test2.add_edge(n_4, n_5, weight=3)
    graph_test2.add_edge(n_5, n_3, weight=4)
    graph_test2.add_edge(n_5, n_2, weight=7)

    return graph_test2


@pytest.fixture(scope="session")
def g3():
    graph_test3 = Graph(directed=True)

    n_0 = graph_test3.add_vertex(0)
    n_1 = graph_test3.add_vertex(1)
    n_2 = graph_test3.add_vertex(2)
    n_3 = graph_test3.add_vertex(3)
    n_4 = graph_test3.add_vertex(4)

    graph_test3.add_edge(n_0, n_1, weight=2)
    graph_test3.add_edge(n_0, n_4, weight=4)
    graph_test3.add_edge(n_1, n_2, weight=3)
    graph_test3.add_edge(n_2, n_3, weight=5)
    graph_test3.add_edge(n_2, n_4, weight=1)
    graph_test3.add_edge(n_3, n_0, weight=8)
    graph_test3.add_edge(n_4, n_3, weight=7)

    return graph_test3


@pytest.fixture(scope="session")
def g4():
    graph_test4 = Graph(directed=False)

    n_0 = graph_test4.add_vertex(0)
    n_1 = graph_test4.add_vertex(1)
    n_2 = graph_test4.add_vertex(2)
    n_3 = graph_test4.add_vertex(3)
    n_4 = graph_test4.add_vertex(4)

    graph_test4.add_edge(n_0, n_1, weight=2)
    graph_test4.add_edge(n_0, n_4, weight=4)
    graph_test4.add_edge(n_1, n_2, weight=3)
    graph_test4.add_edge(n_2, n_3, weight=5)
    graph_test4.add_edge(n_2, n_4, weight=1)
    graph_test4.add_edge(n_3, n_0, weight=8)
    graph_test4.add_edge(n_4, n_3, weight=7)

    return graph_test4


@pytest.fixture(scope="session")
def g5():
    graph_test5 = Graph(directed=False)

    n_0 = graph_test5.add_vertex(0)
    n_1 = graph_test5.add_vertex(1)
    n_2 = graph_test5.add_vertex(2)
    n_3 = graph_test5.add_vertex(3)
    n_4 = graph_test5.add_vertex(4)

    graph_test5.add_edge(n_0, n_1, weight=1)
    graph_test5.add_edge(n_0, n_2, weight=1)
    graph_test5.add_edge(n_1, n_3, weight=1)
    graph_test5.add_edge(n_2, n_4, weight=1)

    return graph_test5


@pytest.fixture(scope="function")
def flights():
    flights = Graph(directed=False)

    f_bos = flights.add_vertex('BOS')
    f_jfk = flights.add_vertex('JFK')
    f_ord = flights.add_vertex('ORD')
    f_mia = flights.add_vertex('MIA')
    f_dfw = flights.add_vertex('DFW')
    f_lax = flights.add_vertex('LAX')
    f_sfo = flights.add_vertex('SFO')
    f_pvd = flights.add_vertex('PVD')
    f_bwi = flights.add_vertex('BWI')

    flights.add_edge(f_bos, f_jfk, weight=187)
    flights.add_edge(f_bos, f_mia, weight=1258)
    flights.add_edge(f_bos, f_ord, weight=867)
    flights.add_edge(f_bos, f_sfo, weight=2704)

    flights.add_edge(f_pvd, f_ord, weight=849)
    flights.add_edge(f_pvd, f_jfk, weight=144)

    flights.add_edge(f_jfk, f_ord, weight=740)
    flights.add_edge(f_jfk, f_mia, weight=1090)

    flights.add_edge(f_bwi, f_ord, weight=621)
    flights.add_edge(f_bwi, f_mia, weight=946)
    flights.add_edge(f_bwi, f_jfk, weight=184)

    flights.add_edge(f_ord, f_sfo, weight=1846)
    flights.add_edge(f_ord, f_dfw, weight=802)

    flights.add_edge(f_mia, f_dfw, weight=1121)
    flights.add_edge(f_mia, f_lax, weight=2342)

    flights.add_edge(f_dfw, f_lax, weight=1235)
    flights.add_edge(f_dfw, f_sfo, weight=1464)
    flights.add_edge(f_dfw, f_jfk, weight=1391)

    flights.add_edge(f_lax, f_sfo, weight=337)

    return flights
