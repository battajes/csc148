"""Trees (Code from lecture)

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains the code for a general tree implementation.
"""
from __future__ import annotations
from typing import Any, List, Optional, Tuple, Union


class Tree:
    """A recursive tree data structure.

    Note the relationship between this class and RecursiveList; the only major
    difference is that _rest has been replaced by _subtrees to handle multiple
    recursive sub-parts.
    """
    # === Private Attributes ===
    # The item stored at this tree's root, or None if the tree is empty.
    _root: Optional[Any]
    # The list of all subtrees of this tree.
    _subtrees: List[Tree]

    # === Representation Invariants ===
    # - If self._root is None then self._subtrees is an empty list.
    #   This setting of attributes represents an empty tree.
    #
    #   Note: self._subtrees may be empty when self._root is not None.
    #   This setting of attributes represents a tree consisting of just one
    #   node.
    #
    # - (NEW) self._subtrees does not contain any empty trees.

    def __init__(self, root: Optional[Any], subtrees: List[Tree]) -> None:
        """Initialize a new Tree with the given root value and subtrees.

        If <root> is None, the tree is empty.
        Precondition: if <root> is None, then <subtrees> is empty.
        """
        self._root = root
        self._subtrees = subtrees

    def is_empty(self) -> bool:
        """Return whether this tree is empty.

        >>> t1 = Tree(None, [])
        >>> t1.is_empty()
        True
        >>> t2 = Tree(3, [])
        >>> t2.is_empty()
        False
        """
        return self._root is None

    def __len__(self) -> int:
        """Return the number of items contained in this tree.

        >>> t1 = Tree(None, [])
        >>> len(t1)
        0
        >>> t2 = Tree(3, [Tree(4, []), Tree(1, [])])
        >>> len(t2)
        3
        """
        if self.is_empty():
            return 0
        else:
            size = 1  # count the root
            for subtree in self._subtrees:
                size += subtree.__len__()  # could also do len(subtree) here
            return size

    def count(self, item: Any) -> int:
        """Return the number of occurrences of <item> in this tree.
        >>> t = Tree(3, [Tree(4, []), Tree(1, [])])
        >>> t.count(3)
        1
        >>> t.count(100)
        0
        """
        if self.is_empty():
            return 0
        else:
            num = 0
            if self._root == item:
                num += 1
            for subtree in self._subtrees:
                num += subtree.count(item)
            return num

    def __str__(self) -> str:
        """Return a string representation of this tree.

        For each node, its item is printed before any of its
        descendants' items. The output is nicely indented.

        You may find this method helpful for debugging.
        """
        # First version is commented out. This had the problem that it doesn't
        # distinguish between different levels in the tree, and just prints out
        # every item on a new line.
        # if self.is_empty():
        #     return ''
        # else:
        #     s = f'{self._root}\n'
        #     for subtree in self._subtrees:
        #         s += str(subtree)  # equivalent to subtree.__str__()
        #     return s
        #
        # Instead, we call a recursive helper method.
        return self._str_indented()

    def _str_indented(self, depth: int = 0) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            s = '  ' * depth + str(self._root) + '\n'
            for subtree in self._subtrees:
                # Note that the 'depth' argument to the recursive call is
                # modified.
                s += subtree._str_indented(depth + 1)
            return s

    def leaves(self) -> List:
        """Return a list of all of the leaf items in the tree.

        >>> Tree(None, []).leaves()
        []
        >>> t = Tree(1, [Tree(2, []), Tree(5, [])])
        >>> t.leaves()
        [2, 5]
        >>> lt = Tree(2, [Tree(4, []), Tree(5, [])])
        >>> rt = Tree(3, [Tree(6, []), Tree(7, [])])
        >>> t = Tree(1, [lt, rt])
        >>> t.leaves()
        [4, 5, 6, 7]
        """
        if self.is_empty():
            return []
        elif self._subtrees == []:
            return [self._root]
        else:
            # (This concatenates a bunch of lists together.)
            # (Should look familiar from a nested list function!)
            result = []
            for subtree in self._subtrees:
                result.extend(subtree.leaves())
            return result

    def average(self) -> float:
        """Return the average of all the values in this tree.

        Return 0.0 if this tree is empty.

        Precondition: this is a tree of numbers.
        """
        if self.is_empty():
            return 0.0
        else:
            data = self._average_helper()
            return data[0] / data[1]

            # Python tip: can also use *unpacking assignment* to
            # store the returned values from self._average_helper:
            # total, count = self._average_helper()
            # return total / count

    def _average_helper(self) -> Tuple[int, int]:
        """Return a tuple (x,y) where:

        x is the sum of the values in this tree, and
        y is the size of this tree.
        """
        if self.is_empty():
            return 0, 0
        elif self._subtrees == []:  # This case is actually redundant.
            return self._root, 1
        else:
            running_sum = self._root
            running_size = 1

            for subtree in self._subtrees:
                data = subtree._average_helper()

                running_sum += data[0]
                running_size += data[1]

            return running_sum, running_size

    # -------------------------------------------------------------------------
    # Mutating methods
    # -------------------------------------------------------------------------
    def delete_item(self, item: Any) -> bool:
        """Delete *one* occurrence of the given item from this tree.

        Return True if <item> was deleted, and False otherwise.
        Do not modify this tree if it does not contain <item>.

        **NOTE**
        This code is incomplete in one subtle way: it leaves empty trees
        in the list self._subtrees! This might cause some unexpected behaviour
        in some other tree methods. We'll discuss this more on Friday's lecture.
        """
        if self.is_empty():
            # The item is not in the tree.
            return False
        elif self._root == item:
            # We've found the item: now delete it.
            self._delete_root()
            return True
        else:
            # Loop through each subtree, and stop the first time
            # the item is deleted. (This is why a boolean is returned!)
            for subtree in self._subtrees:
                deleted = subtree.delete_item(item)
                if deleted and subtree.is_empty():
                    # WARNING: in general don't mutate a list as you're iterating through it!
                    # (But okay here because we're returning right away)
                    self._subtrees.remove(subtree)
                    return True
                elif deleted:  # subtree is not empty
                    return True
                else:
                    # No item was deleted. Continue onto the next subtree.
                    # Note that this branch is unnecessary; we've only shown
                    # it to write comments.
                    pass

            # If we don't return inside the loop, the item is not deleted
            # from any of the subtrees. In this case, the item does not
            # appear in this tree.
            return False

    def _delete_root(self) -> None:
        """Delete the root of this tree.

        Precondition: this tree is non-empty.
        """
        if self._subtrees == []:
            # This is a leaf. Deleting the root gives and empty tree.
            self._root = None
        else:
            # This tree has more than one value!
            # Can't just set self._root = None, need to REPLACE it.

            # Strategy 1: "Promote" a subtree.
            # 1. Remove the rightmost subtree.
            last_subtree = self._subtrees.pop()

            # 2. Update self._root
            self._root = last_subtree._root

            # 3. Update self._subtrees
            self._subtrees += last_subtree._subtrees

            # Strategy 2: Replace with a leaf.
            # 1. Extract the leftmost leaf (using another helper).
            # leaf = self._extract_leaf()
            #
            # 2. Update self._root. (Note that self._subtrees remains the same.)
            # self._root = leaf

    def _extract_leaf(self) -> Any:
        """Remove and return the leftmost leaf in a tree.

        Precondition: this tree is non-empty.
        """
        if self._subtrees == []:
            old_root = self._root
            self._root = None
            return old_root
        else:
            return self._subtrees[0]._extract_leaf()

    def to_nested_list(self) -> List:
        """Return the nested list representation of this tree."""
        if self.is_empty():
            return []
        elif self._subtrees == []:
            return [self._root]
        else:
            result = [self._root]
            for subtree in self._subtrees:
                result.append(subtree.to_nested_list())
            return result


def to_tree(obj: Union[int, List]) -> Optional[Tree]:
    """Return the Tree which <obj> represents.

    Return None if <obj> is not a valid representation of a tree.

    You may not access Tree attributes directly, since they're private.
    This function can be implemented only using the Tree initializer.

    Note that this version doesn't check for empty subtrees---can you see
    how to fix that?
    """
    if isinstance(obj, int):
        return None  # Invalid representation
    elif obj == []:
        return Tree(None, [])   # empty tree
    else:
        potential_root = obj[0]

        # 1. Check that <potential_root> is NOT a list.
        if isinstance(potential_root, list):
            return None

        potential_subtrees = obj[1:]
        subtrees = []
        for sublist in potential_subtrees:
            # 2. Check that <sublist> is a valid tree representation.
            subtree = to_tree(sublist)
            if subtree is None:
                return None
            else:
                subtrees.append(subtree)

        # If we've reached here, the nested list IS a valid representation!
        return Tree(potential_root, subtrees)
