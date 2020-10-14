from algolib.model.trees import tree

import pytest


@pytest.fixture(scope="session")
def tree_1():
    """
    Balanced
    """
    root = tree.BinaryTree(4)
    n1 = tree.BinaryTree(1)
    n2 = tree.BinaryTree(2)
    n3 = tree.BinaryTree(3)
    n5 = tree.BinaryTree(5)
    n6 = tree.BinaryTree(6)
    n7 = tree.BinaryTree(7)
    n8 = tree.BinaryTree(8)

    root.left = n2
    root.right = n6
    n2.left = n1
    n2.right = n3
    n6.left = n5
    n6.right = n7
    n7.right = n8

    return root


@pytest.fixture(scope="session")
def tree_2():
    """
    Unbalanced
    """
    root = tree.BinaryTree(4)
    n1 = tree.BinaryTree(1)
    n2 = tree.BinaryTree(2)
    n3 = tree.BinaryTree(3)
    n6 = tree.BinaryTree(6)
    n7 = tree.BinaryTree(7)
    n8 = tree.BinaryTree(8)

    root.left = n2
    root.right = n6
    n2.left = n1
    n2.right = n3
    n6.right = n7
    n7.right = n8

    return root


@pytest.fixture(scope="session")
def tree_3():
    """
    Unbalanced
    """
    root = tree.BinaryTree(5)
    n1 = tree.BinaryTree(1)
    n2 = tree.BinaryTree(2)
    n3 = tree.BinaryTree(3)
    n6 = tree.BinaryTree(6)
    n7 = tree.BinaryTree(7)
    n8 = tree.BinaryTree(8)

    root.left = n2
    root.right = n7
    n2.left = n1
    n2.right = n3
    n7.left = n6
    n7.right = n8

    return root


def test_get_height(tree_1, tree_2):
    """
    These methods set the height property on the tree nodes.
    """
    assert tree_1.get_height() == 4
    assert tree_2.get_height() == 4


def test_is_balanced(tree_1, tree_2):

    assert tree_1.is_balanced()
    assert not tree_2.is_balanced()


def test_in_order_iterative(tree_3):
    results = []
    tree_3.in_order_iterative(results)

    assert results == [1, 2, 3, 5, 6, 7, 8]


def test_create_level_lists(tree_3):
    results = tree_3.create_level_lists()

    assert results == [[5], [2, 7], [1, 3, 6, 8]]


def test_find_path(tree_3):
    path = []
    assert tree_3.find_path(tree_3, path, 3)
    assert path == [5, 2, 3]


def test_lowest_common_ancestor():
    root = tree.BinaryTree(5)
    n1 = tree.BinaryTree(1)
    n2 = tree.BinaryTree(2)
    n3 = tree.BinaryTree(3)
    n6 = tree.BinaryTree(6)
    n7 = tree.BinaryTree(7)
    n8 = tree.BinaryTree(8)

    root.left = n2
    root.right = n7
    n2.left = n1
    n2.right = n3
    n7.left = n6
    n7.right = n8

    assert root.lowest_common_ancestor(root, n6, n8) == n7

