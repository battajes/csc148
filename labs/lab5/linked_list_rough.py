"""Lab 5: Linked List Exercises

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains the code for a linked list implementation with two classes,
LinkedList and _Node.

All of the code from lecture is here, as well as some exercises to work on.
"""
from __future__ import annotations
from typing import Any, List, Optional


class _Node:
    """A node in a linked list.

    Note that this is considered a "private class", one which is only meant
    to be used in this module by the LinkedList class, but not by client code.

    === Attributes ===
    item:
        The data stored in this node.
    next:
        The next node in the list, or None if there are no more nodes.
    """
    item: Any
    next: Optional[_Node]

    def __init__(self, item: Any) -> None:
        """Initialize a new node storing <item>, with no next node.
        """
        self.item = item
        self.next = None  # Initially pointing to nothing


class LinkedList:
    """A linked list implementation of the List ADT.
    """
    # === Private Attributes ===
    # _first:
    #     The first node in the linked list, or None if the list is empty.
    _first: Optional[_Node]

    def __init__(self, items: List) -> None:
        """Initialize a new linked list containing the given items.

        The first node in the linked list contains the first item
        in <items>.

        >>> lst = LinkedList([1, 2, 1])
        >>> lst._first.item
        1
        >>> lst._first.next.item
        2
        >>> lst._first.next.next.item
        1
        """

        self._first = None
        for item in items:
            curr = self._first
            if curr is None:
                new_node = _Node(item)
                self._first = new_node
            else:
                while curr.next is not None:
                    curr = curr.next

                # After the loop, curr is the last node in the LinkedList.
                # assert curr is not None and curr.next is None
                new_node = _Node(item)
                curr.next = new_node

    # ------------------------------------------------------------------------
    # Methods from lecture/readings
    # ------------------------------------------------------------------------
    def is_empty(self) -> bool:
        """Return whether this linked list is empty.

        # >>> LinkedList([]).is_empty()
        # True
        # >>> LinkedList([1, 2, 3]).is_empty()
        # False
        """
        return self._first is None

    def __str__(self) -> str:
        """Return a string representation of this list in the form
        '[item1 -> item2 -> ... -> item-n]'.

        # >>> str(LinkedList([1, 2, 3]))
        # '[1 -> 2 -> 3]'
        # >>> str(LinkedList([]))
        # '[]'
        """
        items = []
        curr = self._first
        while curr is not None:
            items.append(str(curr.item))
            curr = curr.next
        return '[' + ' -> '.join(items) + ']'

    def __getitem__(self, index: int) -> Any:
        """Return the item at position <index> in this list.

        Raise IndexError if <index> is >= the length of this list.
        """
        curr = self._first
        curr_index = 0

        while curr is not None and curr_index < index:
            curr = curr.next
            curr_index += 1

        assert curr is None or curr_index == index

        if curr is None:
            raise IndexError
        else:
            return curr.item

    def insert(self, index: int, item: Any) -> None:
        """Insert a the given item at the given index in this list.

        Raise IndexError if index > len(self) or index < 0.
        Note that adding to the end of the list is okay.

        # >>> lst = LinkedList([1, 2, 10, 200])
        # >>> lst.insert(2, 300)
        # >>> str(lst)
        # '[1 -> 2 -> 300 -> 10 -> 200]'
        # >>> lst.insert(5, -1)
        # >>> str(lst)
        # '[1 -> 2 -> 300 -> 10 -> 200 -> -1]'
        # >>> lst.insert(100, 2)
        # Traceback (most recent call last):
        # IndexError
        """
        # Create new node containing the item
        new_node = _Node(item)

        if index == 0:
            self._first, new_node.next = new_node, self._first
            # same as:
            # new_node.next = self._first
            # self._first = new_node
        else:
            # Iterate to (index-1)-th node.
            curr = self._first
            curr_index = 0
            while curr is not None and curr_index < index - 1:
                curr = curr.next
                curr_index += 1

            if curr is None:
                raise IndexError
            else:
                # Update links to insert new node
                curr.next, new_node.next = new_node, curr.next
                # same as:
                # new_node.next = curr.next
                # curr.next = new_node

    # ------------------------------------------------------------------------
    # Midterm Prep
    # ------------------------------------------------------------------------
    # insert and pop using both index-1, and prev, curr = curr, curr.next
    def pop(self, index: int) -> Any:
        """Remove and return node at position <index>.

        Precondition: index >= 0.

        Raise IndexError if index >= len(self).

        >>> lst = LinkedList([1, 2, 10, 200])
        >>> lst.pop(2)
        10
        >>> lst.pop(0)
        1
        >>> lst.pop(4)
        Traceback (most recent call last):
        ...
        IndexError
        """
        # Warning: the following is pseudo-code, not valid Python code!

        # 1. If the list is empty, you know that index is out of bounds...

        if self.is_empty():
            raise IndexError
        elif index == 0:
            removed = self._first.item
            self._first = self._first.next
        else:
            curr_index = 0
            curr = self._first

            while curr is not None and curr_index < index-1:
                curr = curr.next
                curr_index += 1

            if curr is None or curr.next is None:
                raise IndexError
            elif curr.next.next is None:
                removed = curr.next.item
                curr.next = None
            else:
                removed = curr.next.item
                curr.next = curr.next.next
        return removed

    def pop2(self, index: int) -> Any:
        """Remove and return node at position <index>.

        Precondition: index >= 0.

        Raise IndexError if index >= len(self).

        >>> lst = LinkedList([1, 2, 10, 200])
        >>> lst.pop(2)
        10
        >>> lst.pop(0)
        1
        """
        # Warning: the following is pseudo-code, not valid Python code!

        # 1. If the list is empty, you know that index is out of bounds...

        if self.is_empty():
            raise IndexError
        elif index == 0:
            removed = self._first.item
            self._first = self._first.next
        else:
            curr_index = 0
            curr = self._first

            while curr is not None and curr_index < index-1:
                curr = curr.next
                curr_index += 1
            if curr.next is not None:
                if curr.next.next is not None:
                    removed = curr.next.item
                    curr.next = curr.next.next
                else:
                    removed = curr.next.item
                    curr.next = None
        return removed

    # ------------------------------------------------------------------------
    # Lab Task 1
    # ------------------------------------------------------------------------
    def __len__(self) -> int:
        """Return the number of elements in this list.

        >>> lst = LinkedList([])
        >>> len(lst)              # Equivalent to lst.__len__()
        0
        >>> lst = LinkedList([1, 2, 3])
        >>> len(lst)
        3
        """
        curr_index = 0
        curr = self._first
        while curr is not None:
            curr_index+=1
            curr = curr.next
        return curr_index

    # TODO: implement this method
    def count(self, item: Any) -> int:
        """Return the number of times <item> occurs in this list.

        Use == to compare items.

        >>> lst = LinkedList([1, 2, 1, 3, 2, 1])
        >>> lst.count(1)
        3
        >>> lst.count(2)
        2
        >>> lst.count(3)
        1
        """
        num_found = 0
        curr = self._first
        while curr is not None:
            if curr.item == item:
                num_found += 1
            curr = curr.next
        return num_found

    # TODO: implement this method
    def index(self, item: Any) -> int:
        """Return the index of the first occurrence of <item> in this list.

        Raise ValueError if the <item> is not present.

        Use == to compare items.

        >>> lst = LinkedList([1, 2, 1, 3, 2, 1])
        >>> lst.index(1)
        0
        >>> lst.index(3)
        3
        >>> lst.index(148)
        Traceback (most recent call last):
        ValueError
        """

        curr_index = 0
        index_found = -1
        curr = self._first
        while curr is not None:
            if curr.item == item and index_found == -1:
                index_found = curr_index
            curr = curr.next
            curr_index +=1

        if index_found < 0:
            raise ValueError
        else:
            return index_found


    # TODO: implement this method
    def __setitem__(self, index: int, item: Any) -> None:
        """Store item at position <index> in this list.

        Raise IndexError if index >= len(self).

        >>> lst = LinkedList([1, 2, 3])
        >>> lst[0] = 100  # Equivalent to lst.__setitem__(0, 100)
        >>> lst[1] = 200
        >>> lst[2] = 300
        >>> str(lst)
        '[100 -> 200 -> 300]'
        """
        if index < len(self):

            curr_index = 0
            curr = self._first

            while curr is not None:
                if curr_index == index:
                    curr.item = item
                curr = curr.next
                curr_index += 1
        else:
            raise IndexError

if __name__ == '__main__':
    # import python_ta
    # python_ta.check_all()
    import doctest
    doctest.testmod()
