
import pytest

from algolib.model.trees.bst import BinarySearchTree


def test_add(bst_2):

    root = BinarySearchTree(4)
    n1 = BinarySearchTree(1)
    n2 = BinarySearchTree(2)
    n3 = BinarySearchTree(3)
    n5 = BinarySearchTree(5)
    n6 = BinarySearchTree(6)
    n7 = BinarySearchTree(7)
    n8 = BinarySearchTree(8)

    root.left = n2
    root.right = n6
    n2.left = n1
    n2.right = n3
    n6.left = n5
    n6.right = n7
    n7.right = n8

    assert root == bst_2.add(8)


def test_add_iterative(bst_3):

    root = BinarySearchTree(4)
    n1 = BinarySearchTree(1)
    n2 = BinarySearchTree(2)
    n3 = BinarySearchTree(3)
    n5 = BinarySearchTree(5)
    n6 = BinarySearchTree(6)
    n7 = BinarySearchTree(7)
    n8 = BinarySearchTree(8)

    root.left = n2
    root.right = n6
    n2.left = n1
    n2.right = n3
    n6.left = n5
    n6.right = n7
    n7.right = n8

    assert root == bst_3.add_iterative(8)


def test_create(bst_1):
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
    #n7.right = BinarySearchTree(8)

    assert bst_1 == root


def test_create2(bst_1):
    root = BinarySearchTree(4)
    root.add_all(2, 6, 1, 3, 5, 7)
    assert bst_1 == root


def test_isbst(bst_1):
    assert BinarySearchTree.is_bst(bst_1)


def test_delete():
    # Rooted at 4: [1, 2, 3, 4, 5, 6, 7, 8]
    bst_4 = BinarySearchTree(4)
    n1 = BinarySearchTree(1)
    n2 = BinarySearchTree(2)
    n3 = BinarySearchTree(3)
    n5 = BinarySearchTree(5)
    n6 = BinarySearchTree(6)
    n7 = BinarySearchTree(7)
    n8 = BinarySearchTree(8)

    bst_4.left = n2
    bst_4.right = n6
    n2.parent = bst_4
    n6.parent = bst_4

    n2.left = n1
    n2.right = n3
    n1.parent = n2
    n3.parent = n2

    n6.left = n5
    n6.right = n7
    n5.parent = n6
    n7.parent = n6
    n7.right = n8
    n8.parent = n7

    bst_4.remove(6)

    assert bst_4.right.value == 7


