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
from typing import Any, List, Optional, Union


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


class LinkedListL:
    """A linked list implementation of the List ADT.
    """
    # === Private Attributes ===
    # _first:
    #     The first node in the linked list, or None if the list is empty.
    # length:
    #     The length of the list.
    # === Representation Invariants ===
    # length: the length of the list is equal to the number of Nodes in the list.
    #
    _first: Optional[_Node]
    _length: int

    def __init__(self, items: list) -> None:
        """Initialize a new linked list containing the given items.

        The first node in the linked list contains the first item
        in <items>.
        """
        self._length = 0

        self._first = None
        for item in items:
            curr = self._first
            if curr is None:
                new_node = _Node(item)
                self._first = new_node
                self._length += 1
            else:
                while curr.next is not None:
                    curr = curr.next

                # After the loop, curr is the last node in the LinkedList.
                # assert curr is not None and curr.next is None
                new_node = _Node(item)
                curr.next = new_node
                self._length += 1

    # ------------------------------------------------------------------------
    # Methods from lecture/readings
    # ------------------------------------------------------------------------
    def is_empty(self) -> bool:
        """Return whether this linked list is empty.

        >>> LinkedListL([]).is_empty()
        True
        >>> LinkedListL([1, 2, 3]).is_empty()
        False
        """
        return self._first is None

    def __str__(self) -> str:
        """Return a string representation of this list in the form
        '[item1 -> item2 -> ... -> item-n]'.

        >>> str(LinkedListL([1, 2, 3]))
        '[1 -> 2 -> 3]'
        >>> str(LinkedListL([]))
        '[]'
        """
        items = []
        curr = self._first
        while curr is not None:
            items.append(str(curr.item))
            curr = curr.next
        return '[' + ' -> '.join(items) + ']'

    def __getitem__(self, index: Union[int, slice]) -> Union[Any, LinkedListL]:
        """Return the item at position <index> in this list.

        Raise IndexError if <index> is >= the length of this list.
        Now includes:
        - negative indices
        - slices with positive numbers with steps

        >>> x = LinkedListL([1, 2, 3])
        >>> x[1]
        2
        >>> x[-1]
        3
        >>> x[-2]
        2
        >>> x[-3]
        1
        >>> x[-4]
        Traceback (most recent call last):
        IndexError
        >>> str(x[0:1])
        '[1]'
        >>> str(x[0:2])
        '[1 -> 2]'
        >>> str(x[0:3])
        '[1 -> 2 -> 3]'
        >>> str(x[4:6])
        '[]'
        >>> str(x[0:10])
        '[1 -> 2 -> 3]'
        >>> str(x[0:3:2])
        '[1 -> 3]'
        >>> str(x[-3:-1])
        '[1 -> 2]'
        >>> str(x[-1:-3])
        '[]'
        >>> str(x[-1:3])
        '[]'
        >>> str(x[-3:])
        '[1 -> 2 -> 3]'
        """
        if isinstance(index, slice):
            if index.start is None:
                new_start = 0
            else:
                new_start = index.start
            if index.stop is None:
                new_stop = self._length + 1
            else:
                new_stop = index.stop
            index2 = slice(new_start, new_stop, index.step)

            if index2.start < 0:
                if (index2.stop > 0 and index.stop is not None) or (
                        index2.stop < 0 and index2.start >= index2.stop):
                    return LinkedListL([])
                elif index2.stop < 0 and index2.start < index2.stop:
                    new_start = self._length + index2.start
                    new_stop = self._length + index2.stop
                    if new_start < 0:
                        new_start = 0
                    if new_stop < 0:
                        new_stop = 0
                    new_index = slice(new_start, new_stop, index2.step)
                else:
                    new_index = index2
            else:
                new_index = slice(index2.start, index2.stop, index2.step)

            if new_index.start > self._length:
                return []
            else:
                curr = self._first
                curr_index = 0
                items = []

                while curr is not None and curr_index < new_index.stop:
                    if new_index.step is None:
                        if curr_index in range(new_index.start, new_index.stop):
                            items.extend([curr.item])
                        curr = curr.next
                        curr_index += 1
                    else:
                        if curr_index in range(new_index.start, new_index.stop,
                                               new_index.step):
                            items.extend([curr.item])
                        curr = curr.next
                        curr_index += 1

                return LinkedListL(items)

        elif isinstance(index, int):
            curr = self._first
            curr_index = 0
            if index < 0:
                index = self._length + index
                if index < 0:
                    raise IndexError

            while curr is not None and curr_index < index:
                curr = curr.next
                curr_index += 1

            assert curr is None or curr_index == index

            if curr is None:
                raise IndexError
            else:
                return curr.item

        # elif isinstance(index, int) and index < 0:
        #
        #     if self._length + index < 0:
        #         raise IndexError
        #     else:
        #         curr = self._first
        #         curr_index = 0
        #         reverse_index = self._length + index
        #
        #         while curr is not None and curr_index < reverse_index:
        #             curr = curr.next
        #             curr_index += 1
        #
        #         return curr.item

    def insert(self, index: int, item: Any) -> None:
        """Insert a the given item at the given index in this list.

        Raise IndexError if index > len(self) or index < 0.
        Note that adding to the end of the list is okay.

        >>> lst = LinkedListL([1, 2, 10, 200])
        >>> lst.insert(2, 300)
        >>> str(lst)
        '[1 -> 2 -> 300 -> 10 -> 200]'
        >>> lst.insert(5, -1)
        >>> str(lst)
        '[1 -> 2 -> 300 -> 10 -> 200 -> -1]'
        >>> lst.insert(100, 2)
        Traceback (most recent call last):
        IndexError
        """
        # Create new node containing the item
        new_node = _Node(item)

        if index == 0:
            self._first, new_node.next = new_node, self._first
            self._length += 1
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
                self._length += 1

    # midterm prep
    def pop(self, index: int) -> Any:
        """Remove and return node at position <index>.

        Precondition: index >= 0.

        Raise IndexError if index >= len(self).

        >>> lst = LinkedListL([1, 2, 10, 200])
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
            self._length -= 1
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
                self._length -= 1
            else:
                removed = curr.next.item
                curr.next = curr.next.next
                self._length -= 1
        return removed

    # ------------------------------------------------------------------------
    # Lab Task 1
    # ------------------------------------------------------------------------
    # TODO: implement this method
    def __len__(self) -> int:
        """Return the number of elements in this list.

        >>> lst = LinkedListL([])
        >>> len(lst)              # Equivalent to lst.__len__()
        0
        >>> lst = LinkedListL([1, 2, 3])
        >>> len(lst)
        3
        """
        return self._length


    # TODO: implement this method
    def count(self, item: Any) -> int:
        """Return the number of times <item> occurs in this list.

        Use == to compare items.

        >>> lst = LinkedListL([1, 2, 1, 3, 2, 1])
        >>> lst.count(1)
        3
        >>> lst.count(2)
        2
        >>> lst.count(3)
        1
        """
        i = 0
        curr = self._first
        while curr is not None:
            if curr.item == item:
                i += 1
            curr = curr.next
        return i


    # TODO: implement this method
    def index(self, item: Any) -> int:
        """Return the index of the first occurrence of <item> in this list.

        Raise ValueError if the <item> is not present.

        Use == to compare items.

        >>> lst = LinkedListL([1, 2, 1, 3, 2, 1])
        >>> lst.index(1)
        0
        >>> lst.index(3)
        3
        >>> lst.index(148)
        Traceback (most recent call last):
        ValueError
        """
        i = 0
        j = -1
        curr = self._first
        while curr is not None:
            if curr.item == item and j == -1:
                j = i
            i += 1
            curr = curr.next
        if j == -1:
            raise ValueError
        return j


    # TODO: implement this method
    def __setitem__(self, index: int, item: Any) -> None:
        """Store item at position <index> in this list.

        Raise IndexError if index >= len(self).

        >>> lst = LinkedListL([1, 2, 3])
        >>> lst[0] = 100  # Equivalent to lst.__setitem__(0, 100)
        >>> lst[1] = 200
        >>> lst[2] = 300
        >>> str(lst)
        '[100 -> 200 -> 300]'
        >>> lst[6] = 150
        Traceback (most recent call last):
        IndexError
        """

        if index > self._length:
            raise IndexError
        else:
            i = 0
            curr = self._first

            while curr is not None:
                if i == index:
                    curr.item = item
                curr = curr.next
                i += 1

if __name__ == '__main__':
    # import python_ta
    # python_ta.check_all()
    import doctest
    doctest.testmod()
