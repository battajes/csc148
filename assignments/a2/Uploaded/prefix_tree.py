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

    def __init__(self, weight_type: str) -> None:
        """Initialize an empty simple prefix tree.

        Precondition: weight_type == 'sum' or weight_type == 'average'.

        The given <weight_type> value specifies how the aggregate weight
        of non-leaf trees should be calculated (see the assignment handout
        for details).
        """
        self.value = []
        self.weight = 0.0
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
            new_tree.weight = float(weight)
            # new attribute needs testing
            new_tree.num_leaves += 1

            # need to find proper location here relative to values in list.
            # if list is empty, append.
            # if not insert appropriately.
            # if self.subtrees == []:
            if not self.subtrees:
                i = -1
                self.subtrees.append(new_tree)
                self.subtrees[i].add(value, weight, prefix, c + 1)
            else:
                i = self.find_place(weight)
                self.subtrees.insert(i, new_tree)
                self.subtrees[i].add(value, weight, prefix, c + 1)

            if c == 1:
                # didn't assign these on the way in, so do it on the way out.
                # this line was not giving the songbook tree a sum weight of 25
                # self.weight = weight
                self.agg_weight(weight)
                # this was already included in agg_weight, added one too many.
                # self.num_leaves += 1
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
        last_tree.weight = float(weight)
        self.subtrees[i].subtrees.insert(j, last_tree)

    def agg_weight(self, weight: float, new_leaves: int = 1) -> None:
        """ Aggregate new weight with self.weight.
            Sum or average, depending on weight type of self.
        """
        if self._weight_type == 'sum':
            self.weight += weight
        elif self._weight_type == 'average':
            self.weight = (self.weight * self.num_leaves + weight) / \
                          (self.num_leaves + new_leaves)
        # this does not work when adding weight to a pre-existing leaf.
        self.num_leaves += new_leaves

    def move_left(self, i: int) -> int:
        """
        When values are added, the weights can be out of order.  A parent tree
        may have a new aggregate weight making the list of subtrees which it
        resides in, unordered by non-increasing weight. I have to find a way to
        move such subtrees to the right position.

        Since weights will only increase with aggregation, only need to check
        if new weight is larger than weight of tree before it in list.  If so
        switch places of trees.  Since list starts at left, this is called
        move_left().

        Returns new index after move is complete.  If index is unchanged,
        returns original index.
        """

        if len(self.subtrees) > 1:
            while i > 0 and self.subtrees[i].weight > self.subtrees[i-1].weight:
                self.subtrees[i-1], self.subtrees[i] = self.subtrees[i], \
                                                       self.subtrees[i-1]
                i -= 1
        return i

    def already_leaf(self, i: int, value: Any, w: float) -> Tuple[int, bool]:
        """
        Checks if there is already a leaf for the value to be added.  If so,
        adds to value of leaf, adjusts position of leaf based on weight, and
        returns True, to indicate that a leaf gained weight.
        """

        try:
            j = self.subtrees[i].subtree_vals().index(value)
        except ValueError:
            j = -1

        if j < 0:
            self.add_leaf(value, w, i, 0)
            # new addition
            self.subtrees[i].agg_weight(w)
            i = self.move_left(i)
            return i, False
        else:
            # this is the case if a leaf is being reinforced.
            self.subtrees[i].subtrees[j].weight += w
            # new addition
            self.subtrees[i].weight += w
            i = self.move_left(i)
            return i, True

    def not_found(self, i: int,
                  w: float, c: int, past_leaf: bool) -> Tuple[int, bool]:
        """ Continues to look for prefix.  If found through recursion, will
        update weights of parent trees.
        """

        if past_leaf:
            # self.subtrees[i].weight += w
            self.subtrees[i].agg_weight(w, 0)
            # added
            i = self.move_left(i)
        else:
            self.subtrees[i].agg_weight(w)
            i = self.move_left(i)

        if c == 1:
            # add weight since new prefix matches deeper prefix.

            if past_leaf:
                self.agg_weight(w, 0)
            else:
                self.agg_weight(w)

        return i, past_leaf

    def add_on(self, value: Any, w: float, prefix: List, c: int = 1) -> bool:
        """ Adds new internal nodes to the SimplePrefixTree assuming the tree
        already has values stored within it.  If the node to be inserted already
        exists, the existing node's weight is updated instead. When a new node
        needs to be created, self.add() is called.

        Returns True if the item added on is already a leaf.  Returns False if
        the leaf was not inserted yet.
        """
        past_leaf = False
        if c <= len(prefix):

            # if prefix[:c] in self.subtrees:
            try:
                i = self.subtree_vals().index(prefix[:c])
            except ValueError:
                i = -1

            if i >= 0:
                if c == len(prefix):

                    i, past_leaf = self.already_leaf(i, value, w)
                    return past_leaf

                else:
                    # add weight to subtree since its prefix matches new prefix.
                    past_leaf = self.subtrees[i].add_on(value, w, prefix, c + 1)

                    i, past_leaf = self.not_found(i, w, c, past_leaf)

            else:
                self.add(value, w, prefix, c)

        return past_leaf

    def autocomplete(self, prefix: List,
                     limit: Optional[int] = None) -> List[Tuple[Any, float]]:
        """Return up to <limit> matches for the given prefix.

        The return value is a list of tuples (value, weight), and must be
        ordered in non-increasing weight. (You can decide how to break ties.)

        If limit is None, return *every* match for the given prefix.

        Precondition: limit is None or limit > 0.
        """

        if self.is_empty():
            return []
        else:
            match = self.find_match(prefix)
            if match is not None:
                return match.find_leaves(prefix, limit)[0]
            else:
                return []

    def find_match(self, prefix: List,
                   c: int = 1) -> Optional[SimplePrefixTree]:
        """ Checks if given prefix is in the SimplePrefixTree. Returns
        SimplePrefixTree starting with prefix.  If prefix is not in tree,
        returns None.
        """
        if c <= len(prefix):

            i = 0
            while i < len(self.subtrees):
                if self.subtrees[i].value == prefix[:c] and c < len(prefix):
                    match = self.subtrees[i].find_match(prefix, c + 1)
                    return match
                elif self.subtrees[i].value == prefix[:c] and c == len(prefix):
                    match = self.subtrees[i]
                    return match
                i += 1
            return None
        else:
            return self

    def find_leaves(self, prefix: List,
                    limit: Optional[int] = None,
                    found: int = 0) -> Tuple[List[Tuple[Any, float]], int]:
        """ Finds all leaves in the SimplePrefixTree and returns a list of
        tuples containing the value and weight of each leaf.  The returned list
        is in order of non-increasing weight."""

        leaves = []

        if self.is_empty():
            return [], 0
        elif self.is_leaf():
            if not at_lim(limit, found):
                leaves.extend([(self.value, self.weight)])
                found += 1
            else:
                return [], 0

        else:
            for subtree in self.subtrees:
                if not at_lim(limit, found):
                    pair = subtree.find_leaves(prefix, limit, found)
                    leaves.extend(pair[0])
                    found = pair[1]

                else:
                    leaves.sort(reverse=True, key=take_weight)
                    return leaves, found
        leaves.sort(reverse=True, key=take_weight)
        return leaves, found

    def remove(self, prefix: List) -> None:
        """Remove all values that match the given prefix.
        """

        if len(prefix) == 0:
            self.subtrees = []
            self.weight = 0
        else:
            ex_weight, ex_leaves = self.remove_match(prefix)
            # check that this doesn't cause any bugs
            if ex_leaves > 0:
                self.remove_weight(ex_weight, ex_leaves)

    def remove_leaf_weight(self, i: int, ex_weight: float,
                           ex_leaves: int)-> Tuple[float, int]:
        """ Takes away the weight contributed by leaves to parent trees.
        """
        self.subtrees[i].remove_weight(ex_weight, ex_leaves)
        if not self.subtrees[i].subtrees:
            del self.subtrees[i]
        return ex_weight, ex_leaves

    def remove_match(self, prefix: List, c: int = 1) -> Tuple[float, int]:
        """ Checks if given prefix is in the SimplePrefixTree and removes Tree.
        Returns weight and number of leaves of removed prefix.
        If not in tree, returns (-1, -1).
        """
        if c <= len(prefix):

            i = 0
            while i < len(self.subtrees):
                if self.subtrees[i].value == prefix[:c] and c < len(prefix):
                    ex_weight, ex_leaves = \
                        self.subtrees[i].remove_match(prefix, c + 1)
                    if ex_leaves > 0:
                        ex_weight, ex_leaves = \
                            self.remove_leaf_weight(i, ex_weight, ex_leaves)
                        return ex_weight, ex_leaves
                elif c == len(prefix) and self.subtrees[i].value == prefix[:c]:
                    weight, leaves = self.subtrees[i].weight, \
                                     self.subtrees[i].num_leaves
                    del self.subtrees[i]
                    return weight, leaves
                i += 1
            return -1, -1
        else:
            return -1, -1

    def remove_weight(self, weight: float, leaves: int) -> None:
        """ Remove weight.
            Sum or average, depending on weight type of self.
        """
        if self._weight_type == 'sum':
            self.weight -= weight

        elif self._weight_type == 'average':
            try:
                leaf_mass = weight*leaves
                self.weight = (self.weight * self.num_leaves - leaf_mass) / \
                              (self.num_leaves - leaves)
            except ZeroDivisionError:
                if self.weight * self.num_leaves - weight == 0:
                    self.weight = 0
                    self.num_leaves = 0

        self.num_leaves -= leaves


################################################################################
# CompressedPrefixTree (Task 6)
################################################################################
class CompressedPrefixTree(SimplePrefixTree):
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
    _weight_type: str
    num_leaves: int

    def add_leaf(self, value: Any, weight: float, i: int, j: int = 0) -> None:
        """ Adds final non-prefix value to the SimplePrefixTree as a leaf.
        """

        last_tree = CompressedPrefixTree(self._weight_type)
        last_tree.value = value
        last_tree.weight = float(weight)
        # was insert with j = -1, but wasn't working
        self.subtrees[i].subtrees.append(last_tree)

    def check_leaves(self, i: int, w: float,
                     value: List) -> Tuple[int, bool]:
        """
        Checks if there is a leaf, adds to it if so, adds if not makes it.
        """
        try:
            j = self.subtrees[i].subtree_vals().index(value)
        except ValueError:
            j = -1
        if j >= 0:
            self.subtrees[i].subtrees[j].weight += w
            past_leaf = True
            if past_leaf:
                pass
        else:
            self.add_leaf(value, w, i)
            self.subtrees[i].move_left(len(self.subtrees[i].subtrees) - 1)
            past_leaf = False
        if past_leaf:
            self.subtrees[i].weight += w
            i = self.move_left(i)
        else:
            self.subtrees[i].agg_weight(w)
            i = self.move_left(i)
        return i, past_leaf

    def add_on(self, value: Any, w: float, prefix: List, c: int = 1) -> bool:
        """ Adds values to a non-empty tree.
        Returns True if a leaf was reinforced, False if leaf was added.
        """
        # had to add this i to make pyTA shut up
        similarity, past_leaf, i = 0, False, 0

        for i in range(len(self.subtrees)):
            if isinstance(self.subtrees[i].value, list):
                similarity = compare_prefix(prefix[c-1:],
                                            self.subtrees[i].value[c-1:])
                if similarity > 0:
                    break
        # added part after 'and' since inserting ab after abc got past this.
        if similarity == len(prefix) + (-c + 1) and \
                len(self.subtrees[i].value) == len(prefix):

            i, past_leaf = self.check_leaves(i, w, value)

        elif 0 < similarity and \
                similarity + 1 == len(self.subtrees[i].value) + (-c + 1):
            # new node before existing node
            new_tree = CompressedPrefixTree(self._weight_type)
            new_tree.weight = w
            new_tree.value = prefix[:similarity + c - 1]

            # add new tree at end of list, add leaf to new tree
            self.subtrees.append(new_tree)
            j = len(self.subtrees) - 1

            # was len(value)
            if len(prefix) == similarity:
                self.add_leaf(value, w, j)
            else:
                self.subtrees[j].add(value, w, prefix)
            self.subtrees[j].num_leaves += 1

            # move old tree down a level (copy, then delete original)
            self.subtrees[j].subtrees.append(self.subtrees[i])
            k = self.subtrees[j].move_left(1)
            self.subtrees.pop(i)
            j -= 1

            # need to update weight of new tree first
            # does leaf mass just work for 'average' and not for 'sum'?
            if self._weight_type == 'average':
                leaf_mass = self.subtrees[j].subtrees[k].weight * \
                            self.subtrees[j].subtrees[k].num_leaves
            else:
                leaf_mass = self.subtrees[j].subtrees[k].weight
            self.subtrees[j].agg_weight(leaf_mass,
                                        self.subtrees[j].subtrees[k].num_leaves)
            self.move_left(j)

        elif 0 < similarity < len(self.subtrees[i].value) + (-c + 1):
            # 0 < similarity(cat, car) < len(car)
            # new node before existing node
            new_tree = CompressedPrefixTree(self._weight_type)
            new_tree.value = prefix[:similarity + c - 1]
            # new_tree.value = prefix[:similarity]

            # add the new subtree
            new_tree.add(value, w, prefix)
            # do this before appending while its easy to access.
            # have to pass number of leaves in old tree!
            if self._weight_type == 'average':
                leaf_mass = self.subtrees[i].weight*self.subtrees[i].num_leaves
                new_tree.agg_weight(leaf_mass, self.subtrees[i].num_leaves)
            else:
                new_tree.agg_weight(self.subtrees[i].weight)

            # add the old subtree by moving it down one level
            new_tree.subtrees.append(self.subtrees[i])
            new_tree.move_left(len(new_tree.subtrees) - 1)
            self.subtrees[i] = new_tree
            i = self.move_left(i)

        elif isinstance(self.subtrees[i].value, list) and \
                similarity == len(self.subtrees[i].value) + (-c + 1):
            # new node after existing node
            past_leaf = self.subtrees[i].add_on(value, w, prefix,
                                                c + similarity)
            # past_leaf = self.subtrees[i].add_on(value, w, prefix, c + 1)
            i = self.move_left(i)

        else:
            # there are no similar elements in the two prefixes.
            self.add(value, w, prefix, c + 1)
            i = self.move_left(len(self.subtrees)-1)

        if c == 1:
            self.move_left(i)

        if past_leaf:
            self.agg_weight(w, 0)
        else:
            self.agg_weight(w)
        return past_leaf

    def add(self, value: Any, weight: float, prefix: List, c: int = 1) -> None:
        """ Adds new internal nodes to a SimplePrefixTree that is empty, or
        that does not already contain these nodes.

        === Representation Invariants ===
        - the nodes to be created do not exist in the SimplePrefixTree

        """
        new_tree = CompressedPrefixTree(self._weight_type)
        new_tree.value = prefix
        new_tree.weight = float(weight)
        new_tree.num_leaves += 1

        self.subtrees.append(new_tree)
        # self.add_leaf(value, weight, -1, -1)
        self.add_leaf(value, weight, -1)
        if self.weight == 0:
            self.agg_weight(weight)
        # self.subtrees[0].agg_weight(weight)

    def remove_match(self, prefix: List, c: int = 1) -> Tuple[float, int]:
        """ Checks if given prefix is in the SimplePrefixTree and removes Tree.
        Returns weight and number of leaves of removed prefix.
        If not in tree, returns (-1, -1).
        """

        similarity, i = 0, 0
        while i < len(self.subtrees):
            similarity = compare_prefix(prefix[c-1:],
                                        self.subtrees[i].value[c-1:])

            if similarity > 0:
                break
            i += 1

        if 0 < similarity < len(prefix) + (-c + 1):
            # on the right track, recurse more
            ex_weight, ex_leaves = \
                self.subtrees[i].remove_match(prefix, c + 1)
            if ex_leaves > 0:
                self.subtrees[i].remove_weight(ex_weight, ex_leaves)
                if not self.subtrees[i].subtrees:
                    del self.subtrees[i]
                return ex_weight, ex_leaves
        elif similarity == len(prefix) + (-c + 1) and \
                len(self.subtrees[i].value) == len(prefix):
            # found prefix, now remove
            # elif c == len(prefix) and self.subtrees[i].value == prefix[:c]:
            weight, leaves = self.subtrees[i].weight, \
                             self.subtrees[i].num_leaves
            del self.subtrees[i]
            return weight, leaves

        # nothing found
        return -1, -1

    def find_match(self, prefix: List,
                   c: int = 1) -> Optional[SimplePrefixTree]:
        """ Checks if given prefix is in the SimplePrefixTree. Returns
        SimplePrefixTree starting with prefix.  If prefix is not in tree,
        returns None.
        """

        if len(prefix) == 0:
            return self

        similarity, i = 0, 0
        while i < len(self.subtrees):
            similarity = compare_prefix(prefix[c - 1:],
                                        self.subtrees[i].value[c - 1:])

            if similarity > 0:
                break
            i += 1

        # if 0 < similarity < len(self.subtrees[i].value) + (-c + 1):
        if 0 < similarity < len(prefix) + (-c + 1):
            # on the right track, recurse more
            # changed c + 1 to c + similarity, to exclude enough letters
            match = self.subtrees[i].find_match(prefix, c + similarity)
            return match
        elif similarity == len(prefix) + (-c + 1):
            # and len(self.subtrees[i].value) == len(prefix):
            match = self.subtrees[i]
            return match
        # elif similarity == len(prefix):
        #     match = self.subtrees[i]
        #     return match

        return None


def compare_prefix(prefix1: List[Any], prefix2: List[Any]) -> int:
    """ Compares prefix1 with prefix2, to see if prefix2 is a shorter prefix
    that applies to parent1 (is a prefix of).

    Stops at shortest prefix length.  Does not assume one is shorter.

    >>> compare_prefix(['h','i'],['h'])
    True
    """

    similarity = 0
    i = 0
    if isinstance(prefix2, list):
        while i < len(prefix2) and i < len(prefix1) and \
                prefix2[i] == prefix1[i]:
            similarity += 1
            i += 1
    return similarity


def take_weight(elem: Tuple[Any, int]) -> int:
    """ Returns the second value of the given tuple. Tuples passed to this
    function will contain a value of any type in the first element of the tuple,
    and a weight in the second element of the tuple.  This function returns the
    weight.
    """
    return elem[1]


def at_lim(limit: Optional[int], found: int) -> bool:
    """
    Used in autocomplete functions to check if the limit of leaf values to be
    returned has been reached.
    """

    if limit is None:
        lim = False
    else:
        if found >= limit:
            lim = True
        else:
            lim = False

    return lim


if __name__ == '__main__':

    import python_ta
    python_ta.check_all(config={
        'max-nested-blocks': 4
    })
