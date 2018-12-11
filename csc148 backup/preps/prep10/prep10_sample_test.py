"""CSC148 Prep 10: Expression Trees
"""

from prep10 import BoolOp, Bool, Num, Compare


def test_compare_evaluate() -> None:
    """
    """

    expr = BoolOp('and', [Bool(True), Bool(True), Bool(False)])
    assert expr.evaluate() == False

    expr = BoolOp('and', [Bool(True), Bool(True), Bool(False),
                         Bool(True), Bool(True), Bool(False),
                         Bool(True), Bool(True), Bool(False),
                         Bool(True), Bool(True), Bool(False),
                         Bool(True), Bool(True), Bool(False)])
    assert expr.evaluate() == False

    expr = BoolOp('and', [Bool(False), Bool(True), Bool(False),
                         Bool(False), Bool(True), Bool(False),
                         Bool(False), Bool(True), Bool(False),
                         Bool(False), Bool(True), Bool(False),
                         Bool(False), Bool(True), Bool(False)])
    assert expr.evaluate() == False

    expr = BoolOp('and', [Bool(True), Bool(False), Bool(False),
                         Bool(False), Bool(False), Bool(False),
                         Bool(False), Bool(False), Bool(False),
                         Bool(False), Bool(False), Bool(False),
                         Bool(False), Bool(False), Bool(False)])
    assert expr.evaluate() == False

    expr = BoolOp('and', [Bool(False), Bool(False), Bool(False),
                         Bool(False), Bool(False), Bool(False),
                         Bool(False), Bool(False), Bool(False),
                         Bool(False), Bool(False), Bool(False),
                         Bool(False), Bool(False), Bool(False)])
    assert expr.evaluate() == False

    expr = BoolOp('and', [Bool(True), Bool(True), Bool(True),
                          Bool(True), Bool(True), Bool(True),
                          Bool(True), Bool(True), Bool(True),
                          Bool(True), Bool(True), Bool(True)])
    assert expr.evaluate() == True

    expr = BoolOp('and', [Bool(False), Bool(True), Bool(True),
                          Bool(True), Bool(True), Bool(True),
                          Bool(True), Bool(True), Bool(True),
                          Bool(True), Bool(True), Bool(True)])
    assert expr.evaluate() == False

    expr = BoolOp('and', [Bool(True), Bool(True), Bool(True),
                          Bool(True), Bool(True), Bool(True),
                          Bool(True), Bool(False), Bool(True),
                          Bool(True), Bool(True), Bool(True)])
    assert expr.evaluate() == False

    expr = BoolOp('or', [Bool(True), Bool(True), Bool(False)])
    assert expr.evaluate() == True

    expr = BoolOp('or', [Bool(True), Bool(True), Bool(False),
                         Bool(True), Bool(True), Bool(False),
                         Bool(True), Bool(True), Bool(False),
                         Bool(True), Bool(True), Bool(False),
                         Bool(True), Bool(True), Bool(False)])
    assert expr.evaluate() == True

    expr = BoolOp('or', [Bool(False), Bool(True), Bool(False),
                         Bool(False), Bool(True), Bool(False),
                         Bool(False), Bool(True), Bool(False),
                         Bool(False), Bool(True), Bool(False),
                         Bool(False), Bool(True), Bool(False)])
    assert expr.evaluate() == True

    expr = BoolOp('or', [Bool(True), Bool(False), Bool(False),
                         Bool(False), Bool(False), Bool(False),
                         Bool(False), Bool(False), Bool(False),
                         Bool(False), Bool(False), Bool(False),
                         Bool(False), Bool(False), Bool(False)])
    assert expr.evaluate() == True

    expr = BoolOp('or', [Bool(False), Bool(False), Bool(False),
                         Bool(False), Bool(False), Bool(False),
                         Bool(False), Bool(True), Bool(False),
                         Bool(False), Bool(False), Bool(False),
                         Bool(False), Bool(False), Bool(False)])
    assert expr.evaluate() == True

    expr = BoolOp('or', [Bool(False), Bool(False), Bool(False),
                         Bool(False), Bool(False), Bool(False),
                         Bool(False), Bool(False), Bool(False),
                         Bool(False), Bool(False), Bool(False),
                         Bool(False), Bool(False), Bool(False)])
    assert expr.evaluate() == False


def test_bool_op_evaluate() -> None:
    """
    """

    expr = Compare(Num(1), [('<=', Num(2))])
    assert expr.evaluate() == True

    expr = Compare(Num(1), [('<', Num(2))])
    assert expr.evaluate() == True

    expr = Compare(Num(1), [('<=', Num(1))])
    assert expr.evaluate() == True

    expr = Compare(Num(1), [('<', Num(1))])
    assert expr.evaluate() == False

    expr = Compare(Num(1), [('<', Num(0.5))])
    assert expr.evaluate() == False

    expr = Compare(Num(1), [('<=', Num(0.5))])
    assert expr.evaluate() == False

    expr = Compare(Num(1), [('<=', Num(2)),
                            ('<', Num(4.5)),
                            ('<=', Num(4.5))])
    assert expr.evaluate() == True

    expr = Compare(Num(1), [('<=', Num(1)),
                            ('<', Num(4.5)),
                            ('<=', Num(4.5))])
    assert expr.evaluate() == True

    expr = Compare(Num(1), [('<=', Num(1)),
                            ('<=', Num(1)),
                            ('<=', Num(1))])
    assert expr.evaluate() == True

    expr = Compare(Num(1), [('<', Num(2)),
                            ('<', Num(3)),
                            ('<', Num(4))])
    assert expr.evaluate() == True

    expr = Compare(Num(1), [('<=', Num(1)),
                            ('<=', Num(1)),
                            ('<=', Num(2))])
    assert expr.evaluate() == True

    expr = Compare(Num(1), [('<=', Num(1)),
                            ('<=', Num(1)),
                            ('<=', Num(0.5))])
    assert expr.evaluate() == False

    expr = Compare(Num(1), [('<=', Num(1)),
                            ('<=', Num(0.5)),
                            ('<=', Num(1))])
    assert expr.evaluate() == False

    expr = Compare(Num(1), [('<=', Num(0.5)),
                            ('<=', Num(1)),
                            ('<=', Num(2))])
    assert expr.evaluate() == False

    expr = Compare(Num(0.5), [('<=', Num(1)),
                            ('<=', Num(1)),
                            ('<=', Num(2))])
    assert expr.evaluate() == True

    expr = Compare(Num(1), [('<', Num(1)),
                            ('<', Num(1)),
                            ('<', Num(1))])
    assert expr.evaluate() == False

    expr = Compare(Num(1), [('<', Num(2)),
                            ('<', Num(2)),
                            ('<', Num(4))])
    assert expr.evaluate() == False

    expr = Compare(Num(1), [('<', Num(2)),
                            ('<', Num(3)),
                            ('<', Num(3))])
    assert expr.evaluate() == False

    expr = Compare(Num(1), [('<', Num(2)),
                            ('<', Num(3)),
                            ('<', Num(4)),
                            ('<', Num(5)),
                            ('<', Num(6)),
                            ('<', Num(7)),
                            ('<', Num(8)),
                            ('<', Num(9))])
    assert expr.evaluate() == True

    expr = Compare(Num(1), [('<=', Num(2)),
                            ('<=', Num(3)),
                            ('<=', Num(4)),
                            ('<=', Num(5)),
                            ('<=', Num(6)),
                            ('<=', Num(7)),
                            ('<=', Num(8)),
                            ('<=', Num(9))])
    assert expr.evaluate() == True

    expr = Compare(Num(1), [('<', Num(2)),
                            ('<', Num(3)),
                            ('<', Num(4)),
                            ('<', Num(5)),
                            ('<', Num(5)),
                            ('<', Num(7)),
                            ('<', Num(8)),
                            ('<', Num(9))])
    assert expr.evaluate() == False

    expr = Compare(Num(1), [('<=', Num(2)),
                            ('<=', Num(3)),
                            ('<=', Num(4)),
                            ('<=', Num(3)),
                            ('<=', Num(6)),
                            ('<=', Num(7)),
                            ('<=', Num(8)),
                            ('<=', Num(9))])
    assert expr.evaluate() == False


if __name__ == '__main__':
    import pytest
    pytest.main(['prep10_sample_test.py'])
