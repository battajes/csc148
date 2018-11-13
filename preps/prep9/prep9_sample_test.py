"""CSC148 Prep 9: Binary Search Trees
"""

from prep9 import BinarySearchTree


def test_maximum() -> None:
    """
    """

    bst = BinarySearchTree(7)
    left = BinarySearchTree(3)
    left._left = BinarySearchTree(3)
    left._right = BinarySearchTree(5)
    right = BinarySearchTree(11)
    right._left = BinarySearchTree(9)
    right._right = BinarySearchTree(13)
    bst._left = left
    bst._right = right

    assert bst.maximum() == 13

    bst = BinarySearchTree(6)
    left = BinarySearchTree(3)
    left._left = BinarySearchTree(3)
    left._right = BinarySearchTree(5)
    right = BinarySearchTree(11)
    right._left = BinarySearchTree(9)
    bst._left = left
    bst._right = right

    assert bst.maximum() == 11

    bst = BinarySearchTree(5)
    right = BinarySearchTree(11)
    right._left = BinarySearchTree(9)
    bst._left = left
    bst._right = right

    assert bst.maximum() == 11

    bst = BinarySearchTree(6)
    left = BinarySearchTree(3)
    left._left = BinarySearchTree(3)
    left._right = BinarySearchTree(5)
    right = BinarySearchTree(11)
    right._left = BinarySearchTree(9)
    right._right = BinarySearchTree(13)
    right._right._right = BinarySearchTree(14)
    right._right._right._right = BinarySearchTree(15)
    right._right._right._right._right = BinarySearchTree(15)
    bst._left = left
    bst._right = right

    assert bst.maximum() == 15

def test_smaller() -> None:
    """
    """
    bst = BinarySearchTree(None)
    assert bst.smaller(1) == []
    assert bst.smaller(10) == []

    bst = BinarySearchTree(7)
    left = BinarySearchTree(3)
    left._left = BinarySearchTree(2)
    left._right = BinarySearchTree(5)
    right = BinarySearchTree(11)
    right._left = BinarySearchTree(9)
    right._right = BinarySearchTree(13)
    bst._left = left
    bst._right = right

    assert bst.smaller(-1) == []
    assert bst.smaller(0) == []
    assert bst.smaller(1) == []
    assert bst.smaller(3) == [2]
    assert bst.smaller(4) == [2, 3]
    assert bst.smaller(5) == [2, 3]
    assert bst.smaller(6) == [2, 3, 5]
    assert bst.smaller(7) == [2, 3, 5]
    assert bst.smaller(8) == [2, 3, 5, 7]
    assert bst.smaller(9) == [2, 3, 5, 7]
    assert bst.smaller(10) == [2, 3, 5, 7, 9]
    assert bst.smaller(11) == [2, 3, 5, 7, 9]
    assert bst.smaller(13) == [2, 3, 5, 7, 9, 11]
    assert bst.smaller(100) == [2, 3, 5, 7, 9, 11, 13]

    bst = BinarySearchTree(8)
    left = BinarySearchTree(3)
    left._left = BinarySearchTree(2)
    left._right = BinarySearchTree(5)
    right = BinarySearchTree(11)
    bst._left = left
    bst._right = right

    assert bst.smaller(3) == [2]
    assert bst.smaller(8) == [2, 3, 5]
    assert bst.smaller(9) == [2, 3, 5, 8]
    assert bst.smaller(11) == [2, 3, 5, 8]
    assert bst.smaller(12) == [2, 3, 5, 8, 11]

    bst = BinarySearchTree(-8)
    right = BinarySearchTree(-3)
    right._right = BinarySearchTree(-2)
    right._right._right = BinarySearchTree(2)
    right._left = BinarySearchTree(-5)
    left = BinarySearchTree(-11)
    bst._right = right
    bst._left = left

    assert bst.smaller(3) == [-11, -8, -5, -3, -2, 2]
    assert bst.smaller(-1) == [-11, -8, -5, -3, -2]
    assert bst.smaller(-2) == [-11, -8, -5, -3]
    assert bst.smaller(-3) == [-11, -8, -5]
    assert bst.smaller(-6) == [-11, -8]
    assert bst.smaller(-8) == [-11]
    assert bst.smaller(-9) == [-11]
    assert bst.smaller(-11) == []
    assert bst.smaller(-12) == []

if __name__ == '__main__':
    import pytest
    pytest.main(['prep9_sample_test.py'])
