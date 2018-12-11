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

def test_add()-> None:

    x = SimplePrefixTree()
    x.add('ab', 0.5, ['a', 'b'])
    assert str(x) == \
           "[] (0.5)\n  ['a'] (0.5)\n    ['a', 'b'] (0.5)\n      ab (0.5)\n"

    y = SimplePrefixTree()
    y.add('hello', 0.3, ['h','e','l','l','o'])
    assert str(y) == "[] (0.3)\n  ['h'] (0.3)\n    ['h', 'e'] (0.3)\n      " + \
           "['h', 'e', 'l'] (0.3)\n        ['h', 'e', 'l', 'l'] (0.3)\n    " + \
           "      ['h', 'e', 'l', 'l', 'o'] (0.3)\n            hello (0.3)\n"

def test_add_on()-> None:

    x = SimplePrefixTree('sum')
    x.add('ab', 0.5, ['a', 'b'])
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

    y = SimplePrefixTree('sum')
    y.add('abc', 0.2, ['a', 'b', 'c'])
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

    s = SimplePrefixTree('sum')
    s.insert('a', 0.1, [])
    assert str(s) == '[] (0.1)\n  a (0.1)\n'
    assert len(s) == 1

    # Inserting one value with a length-one prefix [x] into a new prefix tree
    # should result in a tree with three node: two internal nodes with prefixes
    # [] and [x], and then a leaf containing the inserted value.

    s = SimplePrefixTree('sum')
    s.insert('a', 0.1, ['a'])
    assert str(s) == "[] (0.1)\n  ['a'] (0.1)\n    a (0.1)\n"
    assert len(s) == 1

    # Inserting one value with a length-n prefix [x_1, ..., x_n] into a new
    # prefix tree should result in a tree with (n+2) nodes: internal nodes with
    # prefixes [], [x_1], [x_1, x_2], etc., and then a leaf containing the
    # inserted value.

    s = SimplePrefixTree('sum')
    prefix = ['a','b','c']
    s.insert('a', 0.1, prefix)
    assert len(s) == 1
    assert s.subtrees[0].subtrees[0].subtrees[0].subtrees[0].value == 'a'
    # shows 5 nodes, len prefix plus 2

    s = SimplePrefixTree('average')
    s.insert('a', 0.1, [])
    assert str(s) == '[] (0.1)\n  a (0.1)\n'
    assert len(s) == 1

    # Inserting one value with a length-one prefix [x] into a new prefix tree
    # should result in a tree with three node: two internal nodes with prefixes
    # [] and [x], and then a leaf containing the inserted value.

    s = SimplePrefixTree('average')
    s.insert('a', 0.1, ['a'])
    assert str(s) == "[] (0.1)\n  ['a'] (0.1)\n    a (0.1)\n"
    assert len(s) == 1

    # Inserting one value with a length-n prefix [x_1, ..., x_n] into a new
    # prefix tree should result in a tree with (n+2) nodes: internal nodes with
    # prefixes [], [x_1], [x_1, x_2], etc., and then a leaf containing the
    # inserted value.

    s = SimplePrefixTree('average')
    prefix = ['a', 'b', 'c']
    s.insert('a', 0.1, prefix)
    assert len(s) == 1
    assert s.subtrees[0].subtrees[0].subtrees[0].subtrees[0].value == 'a'
    # shows 5 nodes, len prefix plus 2

    s = SimplePrefixTree('average')
    s.insert('car', 1.0, ['c', 'a', 'r'])
    assert str(s) == "[] (1.0)\n  ['c'] (1.0)\n    ['c', 'a'] (1.0)\n      ['c', 'a', 'r'] (1.0)\n        car (1.0)\n"

    s.insert('cat', 2.0, ['c', 'a', 't'])
    assert str(s) == "[] (1.5)\n  ['c'] (1.5)\n    ['c', 'a'] (1.5)\n      ['c', 'a', 't'] (2.0)\n        cat (2.0)\n      ['c', 'a', 'r'] (1.0)\n        car (1.0)\n"

    s.insert('care', 3.0, ['c', 'a', 'r', 'e'])
    assert str(s) == "[] (2.0)\n  ['c'] (2.0)\n    ['c', 'a'] (2.0)\n      ['c', 'a', 't'] (2.0)\n        cat (2.0)\n      ['c', 'a', 'r'] (2.0)\n        ['c', 'a', 'r', 'e'] (3.0)\n          care (3.0)\n        car (1.0)\n"

def test_insert() -> None:

    # How many values in the prefix tree match the autocomplete prefix?
    # (0? 1? 10?)
    s = SimplePrefixTree('average')
    s.insert('car', 1.0, ['c', 'a', 'r'])
    s.insert('cat', 2.0, ['c', 'a', 't'])
    s.insert('care', 3.0, ['c', 'a', 'r', 'e'])
    assert len(s.autocomplete([])) == 3
    assert len(s.autocomplete(['c'])) == 3
    assert len(s.autocomplete(['c', 'a'])) == 3
    assert len(s.autocomplete(['c', 'a', 't'])) == 1
    assert len(s.autocomplete(['c', 'a', 'r'])) == 2

    # this string has no repeat words
    s = "at this point you should try inserting values into a prefix tree and then calling autocomplete to obtain some results here are suggestions of input properties conditions help design test cases"
    u = s.split()
    a = []
    x = SimplePrefixTree('sum')
    for word in u:
        for c in word:
            a.append(c)
        x.insert(word, 1.0, a)
        a = []
    assert len(x.autocomplete([])) == len(u)
    assert x.autocomplete(['t', 'o']) == [('to', 1.0)]
    assert len(x.autocomplete(['a'])) == 5
    assert x.autocomplete(['o']) == [('of', 1.0), ('obtain', 1.0)]
    assert x.autocomplete(['p', 'r']) == [('properties', 1.0), ('prefix', 1.0)]

    # same as above with average instead of sum
    # this string has no repeat words
    s = "at this point you should try inserting values into a prefix tree and then calling autocomplete to obtain some results here are suggestions of input properties conditions help design test cases"
    u = s.split()
    a = []
    x = SimplePrefixTree('average')
    for word in u:
        for c in word:
            a.append(c)
        x.insert(word, 1.0, a)
        a = []
    assert len(x.autocomplete([])) == len(u)
    assert x.autocomplete(['t', 'o']) == [('to', 1.0)]
    assert len(x.autocomplete(['a'])) == 5
    assert x.autocomplete(['o']) == [('of', 1.0), ('obtain', 1.0)]
    assert x.autocomplete(['p', 'r']) == [('properties', 1.0), ('prefix', 1.0)]

    # What is the relationship between the number of matches and the limit
    # argument? (less than? equal to? greater than?)

    # this string has no repeat words
    s = "at this point you should try inserting values into a prefix tree and then calling autocomplete to obtain some results here are suggestions of input properties conditions help design test cases"
    u = s.split()
    a = []
    x = SimplePrefixTree('sum')
    for word in u:
        for c in word:
            a.append(c)
        x.insert(word, 1.0, a)
        a = []
    assert len(x.autocomplete([], 5)) == 5
    assert x.autocomplete(['t', 'o'], 2) == [('to', 1.0)]
    assert len(x.autocomplete(['a'], 3)) == 3  # there are 5 a words
    assert x.autocomplete(['o'], 0) == []  # same as len() == 0
    assert len(x.autocomplete(['p', 'r'], 2)) == 2

    # If there are more matches than the specified limit, try different
    # combinations of input weights to check that you’re returning the right
    # matches.

    # this string has no repeat words
    s = "at this point you should try inserting values into a prefix tree and then calling autocomplete to obtain some results here are suggestions of input properties conditions help design test cases"
    u = s.split()
    a = []
    x = SimplePrefixTree('sum')
    w = 1.0
    for word in u:
        for c in word:
            a.append(c)
        x.insert(word, w, a)
        a = []
        w += 1.0
    assert len(x.autocomplete([], 5)) == 5
    assert len(x.autocomplete(['t', 'o'], 2)) == 1
    assert len(x.autocomplete(['a'], 3)) == 3  # there are 5 a words
    assert x.autocomplete(['o'], 0) == []  # same as len() == 0
    assert len(x.autocomplete(['p', 'r'], 2)) == 2

    # same as above but with average
    # this string has no repeat words
    s = "at this point you should try inserting values into a prefix tree and then calling autocomplete to obtain some results here are suggestions of input properties conditions help design test cases"
    u = s.split()
    a = []
    x = SimplePrefixTree('average')
    w = 1.0
    for word in u:
        for c in word:
            a.append(c)
        x.insert(word, w, a)
        a = []
        w += 1.0
    assert len(x.autocomplete([], 5)) == 5
    assert len(x.autocomplete(['t', 'o'], 2)) == 1
    assert len(x.autocomplete(['a'], 3)) == 3  # there are 5 a words
    assert x.autocomplete(['o'], 0) == []  # same as len() == 0
    assert len(x.autocomplete(['p', 'r'], 2)) == 2


def test_remove() -> None:

    x = SimplePrefixTree('average')
    x.insert('car', 20, ['c', 'a', 'r'])
    x.insert('cat', 10, ['c', 'a', 't'])
    x.insert('care', 5, ['c', 'a', 'r', 'e'])
    assert x.weight == 11.666666666666666
    x.remove(['c', 'a', 'r', 'e'])
    assert x.weight == 15.0
    x.remove(['c', 'a', 't'])
    assert x.weight == 20.0
    x.remove(['c', 'a'])
    assert x.weight == 0


if __name__ == '__main__':
    import pytest
    pytest.main(['a2_test.py'])
