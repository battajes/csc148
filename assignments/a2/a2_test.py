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
#    assert (['a', 'b', 'c'] in x) == False
#    assert ([1, 2, 3] in x) == False

def test_add_nw()-> None:

    x = SimplePrefixTree()
    x.add_nw('ab', 0.5, ['a', 'b'])
    assert str(x) == \
           "[] (0.5)\n  ['a'] (0.5)\n    ['a', 'b'] (0.5)\n      ab (0.5)\n"

    y = SimplePrefixTree()
    y.add_nw('hello', 0.3, ['h','e','l','l','o'])
    assert str(y) == "[] (0.3)\n  ['h'] (0.3)\n    ['h', 'e'] (0.3)\n      " + \
           "['h', 'e', 'l'] (0.3)\n        ['h', 'e', 'l', 'l'] (0.3)\n    " + \
           "      ['h', 'e', 'l', 'l', 'o'] (0.3)\n            hello (0.3)\n"

def test_add_on()-> None:

    x = SimplePrefixTree()
    x.add_nw('ab', 0.5, ['a', 'b'])
    x.add_on('abc', 0.2, ['a', 'b', 'c'])

    assert x.weight == 0.7
    assert x.value == []
    assert x.subtrees[0].value == ['a']
    assert x.subtrees[0].weight == 0.7
    assert x.subtrees[0].subtrees[0].value == ['a', 'b']
    assert x.subtrees[0].subtrees[0].weight == 0.7
    assert x.subtrees[0].subtrees[0].subtrees[0].value == 'ab'
    assert x.subtrees[0].subtrees[0].subtrees[0].weight == 0.5
    assert x.subtrees[0].subtrees[0].subtrees[1].value == ['a', 'b', 'c']
    assert x.subtrees[0].subtrees[0].subtrees[1].weight == 0.2
    assert x.subtrees[0].subtrees[0].subtrees[1].subtrees[0].value == 'abc'
    assert x.subtrees[0].subtrees[0].subtrees[1].subtrees[0].weight == 0.2

    y = SimplePrefixTree()
    y.add_nw('abc', 0.2, ['a', 'b', 'c'])
    y.add_on('ab', 0.5, ['a', 'b'])

    assert y.weight == 0.7
    assert y.value == []
    assert y.subtrees[0].value == ['a']
    assert y.subtrees[0].weight == 0.7
    assert y.subtrees[0].subtrees[0].value == ['a', 'b']
    assert y.subtrees[0].subtrees[0].weight == 0.7
    assert y.subtrees[0].subtrees[0].subtrees[0].value == 'ab'
    assert y.subtrees[0].subtrees[0].subtrees[0].weight == 0.5
    assert y.subtrees[0].subtrees[0].subtrees[1].value == ['a', 'b', 'c']
    assert y.subtrees[0].subtrees[0].subtrees[1].weight == 0.2
    assert y.subtrees[0].subtrees[0].subtrees[1].subtrees[0].value == 'abc'
    assert y.subtrees[0].subtrees[0].subtrees[1].subtrees[0].weight == 0.2

def test_insert():
    # Inserting one value with an empty prefix [] into a new prefix tree should
    # result in a tree with two nodes: an internal node with an empty prefix [],
    # and then a leaf containing the inserted value. Note that __len__ should
    # return 1 in this case, since we only count inserted values for the
    # Autocompleter ADT.

    s = SimplePrefixTree()
    s.insert('a', 0.1, [])
    assert str(s) == '[] (0.1)\n  a (0.1)\n'
    assert len(s) == 1

    # Inserting one value with a length-one prefix [x] into a new prefix tree
    # should result in a tree with three node: two internal nodes with prefixes
    # [] and [x], and then a leaf containing the inserted value.

    s = SimplePrefixTree()
    s.insert('a', 0.1, ['a'])
    assert str(s) == "[] (0.1)\n  ['a'] (0.1)\n    a (0.1)\n"
    assert len(s) == 1

    # Inserting one value with a length-n prefix [x_1, ..., x_n] into a new
    # prefix tree should result in a tree with (n+2) nodes: internal nodes with
    # prefixes [], [x_1], [x_1, x_2], etc., and then a leaf containing the
    # inserted value.

    s = SimplePrefixTree()
    prefix = ['a','b','c']
    s.insert('a', 0.1, prefix)
    assert len(s) == 1
    assert s.subtrees[0].subtrees[0].subtrees[0].subtrees[0].value == 'a'
    # shows 5 nodes, len prefix plus 2

if __name__ == '__main__':
    import pytest
    pytest.main(['a2_test.py'])
