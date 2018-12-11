"""Testing: a basic example

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains a few simple unit tests for insert_after.
Note that in order to run this file on your own computer,
you need to have followed our CSC148 Software Guide and installed
all of the Python requirements for the course, including pytest.
"""
from typing import List
from hypothesis import given
from hypothesis.strategies import integers, lists

# Note: you'll need to implement insert_after in a file called
# 'insert.py' for this import to work.
# Check the "Testing" slides for the docstring for insert_after.
from insert import insert_after


@given(lists(integers()), integers(), integers())
def test_returns_none(lst: List[int], n1: int, n2: int) -> None:
    """Test that insert_after always returns None.
    """
    assert insert_after(lst, n1, n2) is None


@given(lists(integers()), integers(), integers())
def test_new_item_count(lst: List[int], n1: int, n2: int) -> None:
    """Test that the correct number of items is added.
    """
    num_n1_occurrences = lst.count(n1)
    original_length = len(lst)
    insert_after(lst, n1, n2)

    final_length = len(lst)

    assert final_length - original_length == num_n1_occurrences


if __name__ == '__main__':
    import pytest
    pytest.main(['test_insert_hypothesis.py'])
