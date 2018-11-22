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
    _weight_type:
        A str describing the method used to aggregate weights of nodes in
        the given tree.
    num_leaves:
        An int recording the number of leaves in the given tree. This saves time
        counting leaves using len() each time an average weight needs to be
        calculated.

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
    num_leaves: int

    def __init__(self, weight_type: str = 'average') -> None:
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
        self.num_leaves = 0

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
        Incomplete implementation, as this may not be necessary for the project.
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

    def subtree_vals(self) -> List:
        """ Returns a list of values of the trees in the list self.subtrees.
                """
        items = []
        for subtree in self.subtrees:
            items.append(subtree.value)
        return items

    def get_weights(self) -> List:
        """ Returns a list of weights of the trees in the list self.subtrees.
        """
        items = []
        for subtree in self.subtrees:
            items.append(subtree.weight)
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
            self.add(value, weight, prefix)
        else:
            self.add_on(value, weight, prefix)

    def add(self, value: Any, weight: float, prefix: List, c: int = 1) -> None:
        """ Adds new internal nodes to a SimplePrefixTree that is empty, or
        that does not already contain these nodes.

        === Representation Invariants ===
        - the nodes to be created do not exist in the SimplePrefixTree

        """

        if c <= len(prefix):
            new_tree = SimplePrefixTree(self._weight_type)
            new_tree.value = prefix[:c]
            new_tree.weight = weight
            # new attribute needs testing
            new_tree.num_leaves += 1

            # need to find proper location here relative to values in list.
            # if list is empty, append.
            # if not insert appropriately.
            if self.subtrees == []:
                i = -1
                self.subtrees.append(new_tree)
                self.subtrees[i].add(value, weight, prefix, c + 1)
            else:
                i = self.find_place(weight)
                self.subtrees.insert(i, new_tree)
                self.subtrees[i].add(value, weight, prefix, c + 1)

            if c == 1:
                # didn't assign these on the way in, so do it on the way out.
                self.weight = weight
                self.num_leaves += 1
            if c == len(prefix):
                # i value found from find_place().
                self.add_leaf(value, weight, i, 0)

        elif len(prefix) == 0:
            # change add_leaf to work here. It goes too deep.
            last_tree = SimplePrefixTree(self._weight_type)
            last_tree.value = value
            last_tree.weight = weight
            self.subtrees.append(last_tree)
            self.weight = weight
            self.num_leaves += 1

    def find_place(self, weight: float)-> int:
        """ Returns the index where the next given value should be inserted in
        a list of subtrees.  Finds the index so that after insertion the list
         will remain sorted by weight in non-increasing order.

         === Representation Invariant ===
         - assumes the subtree list is already sorted by weight in
         non-increasing order.

         """

        place = 0
        i = 0
        values = self.get_weights()

        if weight >= values[0]:
            pass
        else:
            while i < len(values):
                if weight < values[i]:
                    place += 1
                else:
                    break
                i += 1
        return place

    def add_leaf(self, value: Any, weight: float, i: int, j: int)-> None:
        """ Adds final non-prefix value to the SimplePrefixTree as a leaf.
        """

        last_tree = SimplePrefixTree(self._weight_type)
        last_tree.value = value
        last_tree.weight = weight
        self.subtrees[i].subtrees.insert(j, last_tree)

    def agg_weight(self, weight: int) -> None:
        """ Aggregate new weight with self.weight.
            Sum or average, depending on weight type of self.
        """
        if self._weight_type == 'sum':
            self.weight += weight
        elif self._weight_type == 'average':
            self.weight = (self.weight * self.num_leaves + weight)/ \
                          (self.num_leaves + 1)
        self.num_leaves += 1

    def add_on(self, value: Any, w: float, prefix: List, c: int = 1) -> None:
        """ Adds new internal nodes to the SimplePrefixTree assuming the tree
        already has values stored within it.  If the node to be inserted already
        exists, the existing node's weight is updated instead. When a new node
        needs to be created, self.add() is called.
        """

        if c <= len(prefix):

            # if prefix[:c] in self.subtrees:
            # replace with a binary search eventually
            try:
                i = self.subtree_vals().index(prefix[:c])
            except ValueError:
                i = -1

            if i >= 0:
                if c == 1:
                    # add weight to root since new prefix matches deeper prefix.
                    self.agg_weight(w)

                if c == len(prefix):
                    # this case is not used if tree contains ('ab', ['a', 'b']
                    # and ('abc', ['a','b','c'] is added.
                    # then we are at last prefix before value. Just have to
                    # check if the value is here somehow
                    # j = binary_search(self.subtree_vals(), prefix[:c])
                    try:
                        j = self.subtrees[i].subtree_vals().index(value)
                    except ValueError:
                        j = -1

                    if j < 0:
                        self.add_leaf(value, w, i, 0)
                    else:
                        self.subtrees[i].subtrees[j].agg_weight(w)

                    self.subtrees[i].agg_weight(w)

                else:
                    # add weight to subtree since its prefix matches new prefix.
                    self.subtrees[i].agg_weight(w)
                    self.subtrees[i].add_on(value, w, prefix, c + 1)
            else:
                self.add(value, w, prefix, c)

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
x
    >>> binary_search([2, 3, 5, 7], 2)
    0
    >>> binary_search([2, 3, 5, 5], 5)
    25
    >>> binary_search(['a', 'b', 'c'], 'b')
    1
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
