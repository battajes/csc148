"""CSC148 Prep 11: Sorting
"""

from prep11 import mergesort, _merge, quicksort, _partition, mergesort3, merge3
from prep11 import kth_smallest

def test_kth_smallest() -> None:
    """
    """

    assert kth_smallest([10, 20, 30, 40], 2) == 30
    assert kth_smallest([20, 10, 30, 40], 2) == 30
    assert kth_smallest([30, 20, 10, 40], 2) == 30
    assert kth_smallest([40, 30, 20, 10], 2) == 30
    assert kth_smallest([10, 20, -4, 3], 0) == -4
    assert kth_smallest([10, 20, -4, 3], 2) == 10


def test_mergesort3() -> None:

    assert mergesort3([10, 2, 5, -6, 17, 10, -11, 1, 2 ,5, 9 ,-42, 53, 219, -4, 23, 0.5, 2.6, -1.9]) == [-42, -11, -6, -4, -1.9, 0.5, 1, 2, 2, 2.6, 5, 5, 9, 10, 10, 17, 23, 53, 219]
    assert mergesort3([10, 2, 5, -6, 17, 10]) == [-6, 2, 5, 10, 10, 17]
    assert mergesort3([2, 5, -6, 17, 10]) == [-6, 2, 5, 10, 17]
    assert mergesort3([5, -6, 17, 10]) == [-6, 5, 10, 17]
    assert mergesort3([-6, 17, 10]) == [-6, 10, 17]
    assert mergesort3([17, 10]) == [10, 17]
    assert mergesort3([10]) == [10]
    assert mergesort3([]) == []
    assert mergesort3([]) == []

if __name__ == '__main__':
    import pytest
    pytest.main(['prep11_sample_test.py'])
