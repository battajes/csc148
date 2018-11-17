"""CSC148 Assignment 2: Autocompleter classes

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This file contains the design of a public interface (Autocompleter) and two
implementation of this interface, SimplePrefixTree and CompressedPrefixTree.
You'll complete both of these subclasses over the course of this assignment.

As usual, be sure not to change any parts of the given *public interface* in the
starter code---and this includes the instance attributes, which we will be
testing directly! You may, however, add new private attributes, methods, and
top-level functions to this file.
"""
from __future__ import annotations
from typing import Any, List, Optional, Tuple


################################################################################
# The Autocompleter ADT
################################################################################
class Autocompleter:
    """An abstract class representing the Autocompleter Abstract Data Type.
    """
    def __len__(self) -> int:
        """Return the number of values stored in this Autocompleter.

        === Representation Invariants ===
        - (EMPTY TREE):
        If self.weight == 0, then self.value == [] and self.subtrees == [].
        This represents an empty simple prefix tree.

        """
        raise NotImplementedError

    def insert(self, value: Any, weight: float, prefix: List) -> None:
        """Insert the given value into this Autocompleter.

        The value is inserted with the given weight, and is associated with
        the prefix sequence <prefix>.

        If the value has already been inserted into this prefix tree
        (compare values using ==), then the given weight should be *added* to
        the existing weight of this value.

        Preconditions:
            weight > 0
            The given value is either:
                1) not in this Autocompleter
                2) was previously inserted with the SAME prefix sequence
        """
        raise NotImplementedError

    def autocomplete(self, prefix: List,
                     limit: Optional[int] = None) -> List[Tuple[Any, float]]:
        """Return up to <limit> matches for the given prefix.

        The return value is a list of tuples (value, weight), and must be
        ordered in non-increasing weight. (You can decide how to break ties.)

        If limit is None, return *every* match for the given prefix.

        Precondition: limit is None or limit > 0.
        """
        raise NotImplementedError

    def remove(self, prefix: List) -> None:
        """Remove all values that match the given prefix.
        """
        raise NotImplementedError


################################################################################
# SimplePrefixTree (Tasks 1-3)
################################################################################
class SimplePrefixTree(Autocompleter):
    """A simple prefix tree.

    This class follows the implementation described on the assignment handout.
    Note that we've made the attributes public because we will be accessing them
    directly for testing purposes.

    === Attributes ===
    value:
        The value stored at the root of this prefix tree, or [] if this
        prefix tree is empty.
    weight:
        The weight of this prefix tree. If this tree is a leaf, this attribute
        stores the weight of the value stored in the leaf. If this tree is
        not a leaf and non-empty, this attribute stores the *aggregate weight*
        of the leaf weights in this tree.
    subtrees:
        A list of subtrees of this prefix tree.

    === Representation invariants ===
    - self.weight >= 0

    - (EMPTY TREE):
        If self.weight == 0, then self.value == [] and self.subtrees == [].
        This represents an empty simple prefix tree.
    - (LEAF):
        If self.subtrees == [] and self.weight > 0, this tree is a leaf.
        (self.value is a value that was inserted into this tree.)
    - (NON-EMPTY, NON-LEAF):
        If len(self.subtrees) > 0, then self.value is a list (*common prefix*),
        and self.weight > 0 (*aggregate weight*).

    - ("prefixes grow by 1")
      If len(self.subtrees) > 0, and subtree in self.subtrees, and subtree
      is non-empty and not a leaf, then

          subtree.value == self.value + [x], for some element x

    - self.subtrees does not contain any empty prefix trees.
    - self.subtrees is *sorted* in non-increasing order of their weights.
      (You can break ties any way you like.)
      Note that this applies to both leaves and non-leaf subtrees:
      both can appear in the same self.subtrees list, and both have a `weight`
      attribute.
    """
    value: Any
    weight: float
    subtrees: List[SimplePrefixTree]
    _weight_type: str

    def __init__(self, weight_type: str ='sum') -> None:
        """Initialize an empty simple prefix tree.

        Precondition: weight_type == 'sum' or weight_type == 'average'.

        The given <weight_type> value specifies how the aggregate weight
        of non-leaf trees should be calculated (see the assignment handout
        for details).
        """
        self.value = []
        self.weight = 0
        self.subtrees = []
        self._weight_type = weight_type

    def is_empty(self) -> bool:
        """Return whether this simple prefix tree is empty."""
        return self.weight == 0.0

    def is_leaf(self) -> bool:
        """Return whether this simple prefix tree is a leaf."""
        return self.weight > 0 and self.subtrees == []

    def __str__(self) -> str:
        """Return a string representation of this tree.

        You may find this method helpful for debugging.
        """
        return self._str_indented()

    def _str_indented(self, depth: int = 0) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            s = '  ' * depth + f'{self.value} ({self.weight})\n'
            for subtree in self.subtrees:
                s += subtree._str_indented(depth + 1)
            return s

    def __contains__(self, prefix: List[Any])-> bool:
        """ Returns True if the SimplePrefixTree contains the given item.

        """
        if self.is_empty():
            return False
        elif self.value == prefix:
            return True
        else:
            index = 1
            contains = False
            for subtree in self.subtrees:
                contains = subtree.__contains__(prefix[:index])
                index += 1
        return contains

    def sub_vals(self) -> List:
        items = []
        for subtree in self.subtrees:
            items.append(subtree.value)
        return items

    def __len__(self) -> int:
        """Return the number of values stored in this Autocompleter.

        === Representation Invariants ===
        - (EMPTY TREE):
        If self.weight == 0, then self.value == [] and self.subtrees == [].
        This represents an empty simple prefix tree.

        """
        if self.is_empty():
            return 0
        elif self.is_leaf():
            return 1
        else:
            size = 0
            for subtree in self.subtrees:
                size += subtree.__len__()  # could also do len(subtree) here
            return size

    # def add_new(self, value: Any, weight: float, prefix: List)-> None:
    #     """Insert a given value to new SimplePrefixTree
    #
    #     - (EMPTY TREE):
    #     If self.weight == 0, then self.value == [] and self.subtrees == [].
    #     This represents an empty simple prefix tree.
    #
    #     """
    #
    #     prefix = ['a', 'b']
    #     weight = 1.5
    #     value = 'ab'
    #
    #     self.subtrees.append(prefix[0])
    #     new = SimplePrefixTree('Sum')
    #
    #     # if prefix == []:
    #     #     self.value = []
    #
    #     for i in range(len(prefix)):
    #         pass

    def insert(self, value: Any, weight: float, prefix: List) -> None:
        """Insert the given value into this Autocompleter.

        The value is inserted with the given weight, and is associated with
        the prefix sequence <prefix>.

        If the value has already been inserted into this prefix tree
        (compare values using ==), then the given weight should be *added* to
        the existing weight of this value.

        Preconditions:
            weight > 0
            The given value is either:
                1) not in this Autocompleter
                2) was previously inserted with the SAME prefix sequence
        """

        if self.is_empty():
            # self._add_new()
            pass
        elif not self.__contains__(value):
            # value is new, and new prefix tree will be added in right place
            # add to existing, add_on()
            pass
        else:
            # value already exists in tree
            # *merge* with existing weight (depending on weight_type)
            pass


            # template:
            # def __len__(self):
            #     if self.is_empty():  # tree is empty
            #         return 0
            #     elif self._subtrees == []:  # tree is a single item
            #         return 1
            #     else:  # tree has at least one subtree
            #         size = 1  # count the root
            #         for subtree in self._subtrees:
            #             size += subtree.__len__()
            #         return size
            # def f(self) -> ...:
            #     if self.is_empty():  # tree is empty
            #         ...
            #     elif self._subtrees == []:  # tree is a single value
            #         ...
            #     else:  # tree has at least one subtree
            #         ...
            #         for subtree in self._subtrees:
            #             ...
            #             subtree.f()...
            #         ...

    def add_new(self, value: Any, weight: float, prefix: List, count: int=1) -> None:
        if count <= len(prefix):
            new_tree = SimplePrefixTree(self._weight_type)
            new_tree.value = prefix[:count]
            new_tree.weight = weight

            self.subtrees.append(new_tree)
            self.subtrees[-1].add_new(value, weight, prefix, count + 1)

            if count == 1:
                self.weight += weight
            elif count == len(prefix):
                last_tree = SimplePrefixTree(self._weight_type)
                last_tree.value = value
                last_tree.weight = weight
                self.subtrees[-1].subtrees.append(last_tree)

        # x = SimplePrefixTree(self._weight_type)
        # # exercise with [1 , 2, 3]
        # prefix = [1, 2, 3]
        # x2 = SimplePrefixTree(self._weight_type)
        # x2.value = prefix[:1]
        #
        # x3 = SimplePrefixTree(self._weight_type)
        # x3.value = prefix[:2]
        #
        # x4 = SimplePrefixTree(self._weight_type)
        # x4.value = prefix[:3]
        #
        # x3.subtrees.append(x4)
        # x2.subtrees.append(x3)
        # x.subtrees.append(x2)

    def add_on(self, value: Any, weight: float, prefix: List, count: int=1) -> None:
        if count <= len(prefix):

            # if prefix[:count] in self.subtrees:
            i = binary_search(self.sub_vals(), prefix[:count])
            if i < 0:

                new_tree = SimplePrefixTree(self._weight_type)
                new_tree.value = prefix[:count]
                new_tree.weight = weight

                self.subtrees.append(new_tree)

                self.subtrees[-1].add_new(value, weight, prefix, count + 1)

                if count == 1:
                    self.weight += weight
                elif count == len(prefix):
                    last_tree = SimplePrefixTree(self._weight_type)
                    last_tree.value = value
                    last_tree.weight = weight
                    self.subtrees[-1].subtrees.append(last_tree)
            else:
                if count == len(prefix):
                    # then we are at last prefix before value. Just have to
                    # check if the value is here somehow
                else:
                    self.subtrees[i].add_on(value, weight, prefix, count + 1)


    def autocomplete(self, prefix: List,
                     limit: Optional[int] = None) -> List[Tuple[Any, float]]:
        """Return up to <limit> matches for the given prefix.

        The return value is a list of tuples (value, weight), and must be
        ordered in non-increasing weight. (You can decide how to break ties.)

        If limit is None, return *every* match for the given prefix.

        Precondition: limit is None or limit > 0.
        """
        raise NotImplementedError

    def remove(self, prefix: List) -> None:
        """Remove all values that match the given prefix.
        """
        raise NotImplementedError


################################################################################
# CompressedPrefixTree (Task 6)
################################################################################
class CompressedPrefixTree(Autocompleter):
    """A compressed prefix tree implementation.

    While this class has the same public interface as SimplePrefixTree,
    (including the initializer!) this version follows the implementation
    described on Task 6 of the assignment handout, which reduces the number of
    tree objects used to store values in the tree.

    === Attributes ===
    value:
        The value stored at the root of this prefix tree, or [] if this
        prefix tree is empty.
    weight:
        The weight of this prefix tree. If this tree is a leaf, this attribute
        stores the weight of the value stored in the leaf. If this tree is
        not a leaf and non-empty, this attribute stores the *aggregate weight*
        of the leaf weights in this tree.
    subtrees:
        A list of subtrees of this prefix tree.

    === Representation invariants ===
    - self.weight >= 0

    - (EMPTY TREE):
        If self.weight == 0, then self.value == [] and self.subtrees == [].
        This represents an empty simple prefix tree.
    - (LEAF):
        If self.subtrees == [] and self.weight > 0, this tree is a leaf.
        (self.value is a value that was inserted into this tree.)
    - (NON-EMPTY, NON-LEAF):
        If len(self.subtrees) > 0, then self.value is a list (*common prefix*),
        and self.weight > 0 (*aggregate weight*).

    - **NEW**
      This tree does not contain any compressible internal values.
      (See the assignment handout for a definition of "compressible".)

    - self.subtrees does not contain any empty prefix trees.
    - self.subtrees is *sorted* in non-increasing order of their weights.
      (You can break ties any way you like.)
      Note that this applies to both leaves and non-leaf subtrees:
      both can appear in the same self.subtrees list, and both have a `weight`
      attribute.
    """
    value: Optional[Any]
    weight: float
    subtrees: List[CompressedPrefixTree]

    def __len__(self) -> int:
        """Return the number of values stored in this Autocompleter.

        === Representation Invariants ===
        - (EMPTY TREE):
        If self.weight == 0, then self.value == [] and self.subtrees == [].
        This represents an empty simple prefix tree.

        """
        raise NotImplementedError

    def insert(self, value: Any, weight: float, prefix: List) -> None:
        """Insert the given value into this Autocompleter.

        The value is inserted with the given weight, and is associated with
        the prefix sequence <prefix>.

        If the value has already been inserted into this prefix tree
        (compare values using ==), then the given weight should be *added* to
        the existing weight of this value.

        Preconditions:
            weight > 0
            The given value is either:
                1) not in this Autocompleter
                2) was previously inserted with the SAME prefix sequence
        """
        raise NotImplementedError

def binary_search(l: list, v: Any) -> int:
    """ Return the index of the first occurrence of v in L, or return -1
    if v is not in L.

    Precondition: L is sorted from smallest to largest and all the items
    in L can be compared to v.

    >>> binary_search([2, 3, 5, 7], 2)
    0
    >>> binary_search([2, 3, 5, 5], 5)
    2
    >>> binary_search([2, 3, 5, 7], 8)
    -1
    """

    b = 0
    e = len(l) - 1

    while b <= e:
        m = (b + e) // 2
        if l[m] < v:
            b = m + 1
        else:
            e = m - 1

    if b == len(l) or l[b] != 1:
        return -1
    else:
        return b

if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-nested-blocks': 4
    })
