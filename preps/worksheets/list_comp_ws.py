from __future__ import annotations
from typing import List, Union

def sum_nested(obj:Union[int, List]) -> int:
    """Return the sum of the numbers in <obj> (or 0 if there are no numbers).
    >>> sum_nested([1, 2, 3, [4, [5, 6]]])
    21
    >>> sum_nested([])
    0
    >>> sum_nested(['a','b'])
    0
    >>> sum_nested(['a',['b', 'c']])
    0
    """
    if isinstance(obj, int):
        return obj
    elif isinstance(obj, list):
        sum_list = [sum_nested(sublist) for sublist in obj]
        s = sum(sum_list)
        return s
    else:
        return 0

def flatten(obj:Union[int, List]) -> List[int]:
    """Return a (non-nested) list of the integers in <obj>.
    >>> flatten([1, 2, 3, [4, [5, 6]]])
    [1, 2, 3, 4, 5, 6]
    """
    if isinstance(obj, int):
        return [obj]
    else:
        s = []
        s.extend([flatten(sublist) for sublist in obj])
        flattened = sum(s, [])
        return flattened

def flatten1(obj:Union[int, List]) -> List[int]:
    """Return a (non-nested) list of the integers in <obj>.
    >>> flatten1([1, 2, 3, [4, [5, 6]]])
    [1, 2, 3, 4, 5, 6]
    """
    if isinstance(obj, int):
        return [obj]
    else:
        s = []
        for sublist in obj:
            s.extend(flatten1(sublist))
        return s

def nested_list_contains(obj:Union[int, List], item: int) -> bool:
    """Searches for a number in a nested list. Returns True if the number is
    found in the list. Returns False if the number is not found.
    >>> nested_list_contains([1, 2, 3, [4, [5, 6]]], 5)
    True
    >>> nested_list_contains([1, 2, 3, [4, [5, 6]]], 7)
    False
    >>> nested_list_contains([],7)
    False
    >>> nested_list_contains([],7)
    False
    >>> nested_list_contains([[[]]],7)
    False
    """
    if isinstance(obj, int):
        if obj == item:
            return True
        else:
            return False
    else:
        s = []
        s.extend([nested_list_contains(sublist, item) for sublist in obj])
        return any(s)

def semi_homogenous(obj:Union[int, List]) -> bool:
    """Return whether the given nested list is semi-homogeneous.

    A single integer and empty list are semi-homogeneous.
    In general, a list is semi-homogeneous if and only if:
        - all of its sub-nested-lists are integers, or all of them are lists.
        - all of its sub-nested-lists are semi-homogeneous.
    >>> semi_homogenous([])
    True
    >>> semi_homogenous(1)
    True
    >>> semi_homogenous([1, [1, 3], [[1, 2],[[3]]]])
    False
    >>> semi_homogenous([1, 2, 3, 4])
    True
    >>> semi_homogenous([[],[],[[[]]],[[],[]]])
    True
    >>> semi_homogenous([1, [[]], [[1, 2],[[3]]]])
    False
    """
    if isinstance(obj, int):
        return True
    elif obj == []:
        return True
    else:
        first_type = type(obj[0])
        s = []
        s.extend([(semi_homogenous(sublist) and isinstance(sublist,first_type))
                  for sublist in obj])
        return all(s)

if __name__ == '__main__':
    import doctest  # import the doctest library
    doctest.testmod()  # run the tests
