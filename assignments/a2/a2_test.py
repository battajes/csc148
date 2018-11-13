"""A2 tests
"""

from prefix_tree import SimplePrefixTree


def test_len() -> None:
    """
    """
    x = SimplePrefixTree('Sum')
    y = SimplePrefixTree('Sum')
    y.value = 3
    y.weight = 1
    x.subtrees = [y]
    x.weight = 1

    assert len(x) == 1

    x = SimplePrefixTree('Sum')
    y = SimplePrefixTree('Sum')
    z = SimplePrefixTree('Sum')
    z.value = 'a'
    z.weight = 1
    y.subtrees = [z]
    y.weight = 1
    y.value = ['a']
    x.subtrees = [y]
    x.weight = 1
    x.value = []

    assert len(x) == 1

    x = SimplePrefixTree('Sum')
    y = SimplePrefixTree('Sum')
    z = SimplePrefixTree('Sum')
    z.value = 'a'
    z.weight = 1
    y.subtrees = [z]
    y.weight = 1
    y.value = ['a']
    x.subtrees = [y]
    x.weight = 1
    x.value = []

    assert len(x) == 1


def test_contains()-> None:

    x = SimplePrefixTree('Sum')
    y = SimplePrefixTree('Sum')
    z = SimplePrefixTree('Sum')
    z.value = 'a'
    z.weight = 1
    y.subtrees = [z]
    y.weight = 1
    y.value = ['a']
    x.subtrees = [y]
    x.weight = 1
    x.value = []

    assert (['a'] in x) == True
    assert ([] in x) == True
    assert (['b'] in x) == False
    assert ([1] in x) == False
    assert (['a', 'b', 'c'] in x) == False
#    assert ([1, 2, 3] in x) == False

if __name__ == '__main__':
    import pytest
    pytest.main(['a2_test.py'])
