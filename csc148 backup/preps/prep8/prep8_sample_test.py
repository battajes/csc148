"""CSC148 Prep 8: Trees
"""

from hypothesis import given
from hypothesis.strategies import integers, lists

from prep8 import Tree

def test_num_positives() -> None:
    """
    """

    t1 = Tree(17, [])
    assert t1.num_positives() == 1

    t2 = Tree(-10, [])
    assert t2.num_positives() == 0

    t3 = Tree(1, [Tree(-2, []), Tree(10, []), Tree(-30, [])])
    assert t3.num_positives() == 2

    t4 = Tree(None, [])
    assert t4.num_positives() == 0

    t5 = Tree(1, [Tree(-2, [Tree(10, [])]), Tree(-30, [Tree(10, [])])])
    assert t5.num_positives() == 3

    t6 = Tree(1, [Tree(-2, []), Tree(10, []), Tree(-30, []), Tree(10, [])])
    assert t6.num_positives() == 3

    t7 = Tree(0, [])
    assert t7.num_positives() == 0

def test_maximum() -> None:
    """
    """
    t1 = Tree(17, [])
    assert t1.maximum() == 17

    t2 = Tree(None, [])
    assert t2.maximum() == 0

    t3 = Tree(1, [Tree(-2, []), Tree(10, []), Tree(-30, [])])
    assert t3.maximum() == 10

    t4 = Tree(-10, [])
    assert t4.maximum() == -10

    t5 = Tree(1, [Tree(-2, [Tree(10, [])]), Tree(-30, [Tree(10, [])])])
    assert t5.maximum() == 10

    t6 = Tree(1, [Tree(-2, []), Tree(10, []), Tree(-30, []), Tree(10, [])])
    assert t6.maximum() == 10

def test_height() -> None:
    """
    """
    t1 = Tree(17, [])
    assert t1.height() == 1

    t2 = Tree(1, [Tree(-2, []), Tree(10, []), Tree(-30, [])])
    assert t2.height() == 2

    t3 = Tree(1, [Tree(-2, [Tree(-3, [])]), Tree(10, []), Tree(-30, [])])
    assert t3.height() == 3

    t4 = Tree(1, [Tree(-2, [Tree(10, [])]), Tree(-30, [Tree(10, [])])])
    assert t4.height() == 3

    t5 = Tree(1, [Tree(-2, []), Tree(10, []), Tree(-30, []), Tree(10, [])])
    assert t5.height() == 2

    t6 = Tree(None, [])
    assert t6.height() == 0

    t7 = Tree(1, [Tree(-2, [Tree(10, [Tree(-30, [Tree(10, [Tree(10, [Tree(10, [])])])])])])])
    assert t7.height() == 7

    t8 = Tree(1, [Tree(-2, [
        Tree(10, [Tree(-30, [Tree(10, [Tree(10, [Tree(10, [])])])])])]),
                  Tree(10, [Tree(10, [Tree(10, [])])]),
                  Tree(10, [Tree(10, [Tree(10, [Tree(10, [])])])])])
    assert t8.height() == 7

def test_contains() -> None:
    """
    """
    t = Tree(1, [Tree(-2, []), Tree(10, []), Tree(-30, [])])
    assert t.__contains__(-30) == True
    assert t.__contains__(148) == False

    t1 = Tree(1, [Tree(-2, [
        Tree(10, [Tree(-30, [Tree(10, [Tree(10, [Tree(10, [])])])])])])])
    assert t1.__contains__(10) == True
    assert t1.__contains__(12) == False

    t3 = Tree(1, [Tree(-2, [Tree(-3, [])]), Tree(10, []), Tree(-30, [])])
    assert t3.__contains__(-3) == True
    assert t3.__contains__(129) == False

    t4 = Tree(1, [Tree(-2, [Tree(10, [])]), Tree(-30, [Tree(10, [])])])
    assert t4.__contains__(10) == True
    assert t4.__contains__(435) == False

    t5 = Tree(None, [])
    assert t5.__contains__(4) == False
    assert t5.__contains__(None) == False


if __name__ == '__main__':
    import pytest
    pytest.main(['prep8_sample_test.py'])
