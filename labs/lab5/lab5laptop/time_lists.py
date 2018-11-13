"""CSC148 Lab 5: Linked Lists

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module description ===

This module runs timing experiments to determine how the time taken
to call `len` on a Python list vs. a LinkedList grows as the list size grows.
"""
from timeit import timeit
from linked_list import LinkedList
import matplotlib.pyplot as plt

NUM_TRIALS = 3000                        # The number of trials to run.
SIZES = [1000, 2000, 4000, 8000, 16000]  # The list sizes to try.


def profile_len(list_class: type, size: int) -> float:
    """Return the time taken to call len on a list of the given class and size.

    Precondition: list_class is either list or LinkedList.
    """
    # TODO: Create an instance of list_class containing <size> 0's.
    my_list = list_class([0]*size)
    a = [0, 0, 0]

    # TODO: call timeit appropriately to check the runtime of len on the list.
    # Look at the Lab 4 starter code if you don't remember how to use timeit:
    # https://www.teach.cs.toronto.edu/~csc148h/fall/labs/w4_ADTs/starter-code/timequeue.py
    test_time = timeit('len(my_list)', number=1, globals=locals())

    return test_time


if __name__ == '__main__':

    # Try both Python's list and our LinkedList
    for list_class in [list, LinkedList]:
        # Try each list size
        for s in SIZES:
            time = profile_len(list_class, s)
            print(f'[{list_class.__name__}] Size {s:>6}: {time}')



    # plt.plot(lists[0], lists[1], 'bs', lists[0], lists[2], 'g^')
    # plt.show()

    # results = (SIZES, list_tests, linked_tests)
    # return results
