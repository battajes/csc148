"""CSC148 Lab 11: More on sorting

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This file contains a mutating implementation of mergesort,
and a skeleton implementation of Timsort that you will work through
during this lab.
"""
from typing import Optional, List, Tuple


###############################################################################
# Introduction: mutating version of mergesort
###############################################################################
def mergesort2(lst: list,
               start: int = 0,
               end: Optional[int] = None) -> None:
    """Sort the items in lst[start:end] in non-decreasing order.

    Note: this is a *mutating, in-place* version of mergesort,
    meaning it does not return a new list, but instead sorts the input list.

    When we divide the list into halves, we don't create new lists for each
    half; instead, we simulate this by passing additional parameters (start
    and end) to represent the part of the list we're currently recursing on.
    """
    if end is None:
        end = len(lst)

    if start < end - 1:
        mid = (start + end) // 2
        mergesort2(lst, start, mid)
        mergesort2(lst, mid, end)
        _merge(lst, start, mid, end)


def _merge(lst: list, start: int, mid: int, end: int) -> None:
    """Sort the items in lst[start:end] in non-decreasing order.

    Precondition: lst[start:mid] and lst[mid:end] are sorted.
    """
    result = []
    left = start
    right = mid
    while left < mid and right < end:
        if lst[left] < lst[right]:
            result.append(lst[left])
            left += 1
        else:
            result.append(lst[right])
            right += 1

    # This replaces lst[start:end] with the correct sorted version.
    lst[start:end] = result + lst[left:mid] + lst[right:end]


###############################################################################
# Task 1: Finding runs
###############################################################################
def find_runs(lst: list) -> List[Tuple[int, int]]:
    """Return a list of tuples indexing the runs of lst.

    Precondition: lst is non-empty.

    >>> find_runs([1, 4, 7, 10, 2, 5, 3, -1])
    [(0, 4), (4, 6), (6, 7), (7, 8)]
    >>> find_runs([0, 1, 2, 3, 4, 5])
    [(0, 6)]
    >>> find_runs([10, 4, -2, 1])
    [(0, 1), (1, 2), (2, 4)]
    """
    runs = []

    # Keep track of the start and end points of a run.
    run_start = 0
    run_end = 1
    while run_end < len(lst):
        # How can you tell if a run should continue?
        #   (When you do, update run_end.)
        if lst[run_end] >= lst[run_end - 1]:
            run_end += 1

        # How can you tell if a run is over?
        #   (When you do, update runs, run_start, and run_end.)
        else:
            runs.append((run_start, run_end))
            run_start = run_end
            run_end = run_start + 1

    if lst:
        runs.append((run_start, run_end))

    return runs


###############################################################################
# Task 2: Merging runs
###############################################################################
def timsort(lst: list) -> None:
    """Sort <lst> in place.

    >>> lst = []
    >>> timsort(lst)
    >>> lst
    []
    >>> lst = [1]
    >>> timsort(lst)
    >>> lst
    [1]
    >>> lst = [1, 4, 7, 10, 2, 5, 3, -1]
    >>> timsort(lst)
    >>> lst
    [-1, 1, 2, 3, 4, 5, 7, 10]
    """
    runs = find_runs3(lst)

    # Treat runs as a stack and repeatedly merge the top two runs
    while len(runs) > 1:
        run2, run1 = runs.pop(), runs.pop()
        _merge2(lst, run1[0], run1[1], run2[1])
        runs.append((run1[0], run2[1]))

    # When the loop ends, the only run should be the whole list.

###############################################################################
# Task 3: Descending runs
###############################################################################
def find_runs2(lst: list) -> List[Tuple[int, int]]:
    """Return a list of tuples indexing the runs of lst.

    Now, a run can be either ascending or descending!

    Precondition: lst is non-empty.

    First set of doctests, just for finding descending runs.
    >>> find_runs2([5, 4, 3, 2, 1])
    [(0, 5)]
    >>> find_runs2([1, 4, 7, 10, 2, 5, 3, -1])
    [(0, 4), (4, 6), (6, 8)]
    >>> find_runs2([0, 1, 2, 3, 4, 5])
    [(0, 6)]
    >>> find_runs2([10, 4, -2, 1])
    [(0, 3), (3, 4)]

    The second set of doctests, to check that descending runs are reversed.
    >>> lst1 = [5, 4, 3, 2, 1]
    >>> find_runs2(lst1)
    [(0, 5)]
    >>> lst1  # The entire run is reversed
    [1, 2, 3, 4, 5]
    >>> lst2 = [1, 4, 7, 10, 2, 5, 3, -1]
    >>> find_runs2(lst2)
    [(0, 4), (4, 6), (6, 8)]
    >>> lst2  # The -1 and 3 are switched
    [1, 4, 7, 10, 2, 5, -1, 3]
    """
    # Hint: this is very similar to find_runs, except
    # you'll need to keep track of whether the "current run"
    # is ascending or descending.
    runs = []

    # Keep track of the start and end points of a run.
    run_start = 0
    run_end = 1
    new_run = True
    ascending = True

    while run_end < len(lst):
        # How can you tell if a run should continue?
        #   (When you do, update run_end.)
        if new_run:
            if lst[run_end] > lst[run_end - 1]:
                ascending = True
            else:
                ascending = False

        if lst[run_end] > lst[run_end - 1] and ascending:
            run_end += 1
            new_run = False
        elif lst[run_end] < lst[run_end - 1] and ascending:
            runs.append((run_start, run_end))
            run_start = run_end
            run_end = run_start + 1
            new_run = True
        elif lst[run_end] < lst[run_end - 1] and not ascending:
            run_end += 1
            new_run = False
        elif lst[run_end] > lst[run_end -1] and not ascending:
            # end descending run, add to runs, start new run.
            runs.append((run_start, run_end))
            run_start = run_end
            run_end = run_start + 1
            new_run = True
            reverse_run(lst, run_start, run_end)

    if lst:
        runs.append((run_start, run_end))
        if not ascending:
            reverse_run(lst, run_start, run_end)

    return runs


def reverse_run(lst: list, start: int, end: int) -> None:
    """
    Reverses the order of elements between start and end in lst.
    >>> lst =[1,2,3,4,5,6,7,8,9,10]
    >>> reverse_run(lst,1,8)
    >>> lst
    [1, 8, 7, 6, 5, 4, 3, 2, 9, 10]
    """
    shrtlst = lst[start:end]
    mid = len(shrtlst) // 2

    for i in range(mid):
        shrtlst[i], shrtlst[-(i+1)] = shrtlst[-(i+1)], shrtlst[i]

    for i in range(len(shrtlst)):
        lst[i + start] = shrtlst[i]

    # lst = lst[:start] + shrtlst + lst[end:]
    # lst[start:end] = shrtlist


###############################################################################
# Task 4: Minimum run length
###############################################################################
MIN_RUN = 64


def find_runs3(lst: list) -> List[Tuple[int, int]]:
    """Same as find_runs2, but each run (except the last one)
    must be of length >= MIN_RUN.

    Precondition: lst is non-empty
    """

    # Hint: this is very similar to find_runs, except
    # you'll need to keep track of whether the "current run"
    # is ascending or descending.
    runs = []

    # Keep track of the start and end points of a run.
    run_start = 0
    run_end = 1
    new_run = True
    ascending = True

    while run_end < len(lst):
        # How can you tell if a run should continue?
        #   (When you do, update run_end.)
        if new_run:
            if lst[run_end] > lst[run_end - 1]:
                ascending = True
            else:
                ascending = False

        if lst[run_end] > lst[run_end - 1] and ascending:
            run_end += 1
            new_run = False
        elif lst[run_end] < lst[run_end - 1] and ascending:

            # found a run (that has ended)
            while (run_end - run_start) < 64 and run_end < len(lst):
                run_end += 1
                insertion_sort(lst, run_start, run_end)

            runs.append((run_start, run_end))
            run_start = run_end
            run_end = run_start + 1
            new_run = True
        elif lst[run_end] < lst[run_end - 1] and not ascending:
            run_end += 1
            new_run = False
        elif lst[run_end] > lst[run_end - 1] and not ascending:

            # found a run (that has ended)
            while (run_end - run_start) < 64 and run_end < len(lst):
                run_end += 1
                insertion_sort(lst, run_start, run_end)

            runs.append((run_start, run_end))
            run_start = run_end
            run_end = run_start + 1
            new_run = True
            # reverse_run(lst, run_start, run_end)

    if lst and run_start < len(lst):
        runs.append((run_start, run_end))
        if not ascending:
            reverse_run(lst, run_start, run_end)

    return runs


def insertion_sort(lst: list, start: int, end: int) -> None:
    """Sort the items in lst[start:end] in non-decreasing order.
    """
    for i in range(start + 1, end):
        num = lst[i]
        left = start
        right = i
        while right - left > 1:
            mid = (left + right) // 2
            if num < lst[mid]:
                right = mid
            else:
                left = mid + 1

        # insert
        if lst[left] > num:
            lst[left + 1:i + 1] = lst[left:i]
            lst[left] = num
        else:
            lst[right+1:i+1] = lst[right:i]
            lst[right] = num


###############################################################################
# Task 5: Optimizing merge
###############################################################################
def _merge2(lst: list, start: int, mid: int, end: int) -> None:
    """Sort the items in lst[start:end] in non-decreasing order.

    Precondition: lst[start:mid] and lst[mid:end] are sorted.
    """

    part_a = lst[start:mid]
    left = start
    right = mid
    while left < end and right < end:
        if part_a[0] < lst[right]:
            lst[left] = part_a.pop(0)
            left += 1
        else:
            lst[left] = lst[right]
            right += 1
            left += 1

    if part_a:
        lst[-len(part_a):] = part_a[:]


###############################################################################
# Task 6: Limiting the 'runs' stack
###############################################################################
def timsort2(lst: list) -> None:
    """Sort the given list using the version of timsort from Task 6.

    >>> lst = []
    >>> timsort(lst)
    >>> lst
    []
    >>> lst = [1]
    >>> timsort(lst)
    >>> lst
    [1]
    >>> lst = [1, 4, 7, 10, 2, 5, 3, -1]
    >>> timsort(lst)
    >>> lst
    [-1, 1, 2, 3, 4, 5, 7, 10]
    """
    runs = find_runs4(lst)

    # Treat runs as a stack and repeatedly merge the top two runs
    while len(runs) > 1:
        run2, run1 = runs.pop(), runs.pop()
        _merge2(lst, run1[0], run1[1], run2[1])
        runs.append((run1[0], run2[1]))

    # When the loop ends, the only run should be the whole list.

def find_runs4(lst: list) -> List[Tuple[int, int]]:
    """Each time a run is pushed onto the stack, and the stack has size >= 3:
    Let A, B, and C be the lengths of the three top-most runs on the stack
    (so C is the length of the rightmost run found so far). Check these two
    properties:

    B > C
    A > B + C

    If these two properties hold, keep going and add a new run to the stack.

    If these properties don’t hold, do a merge instead:

    If B <= C, merge B and C.
    If A <= B + C, merge the shorter of A and C with B. Continue merging until
    the properties hold (or until there’s only one run on the stack).

    Precondition: lst is non-empty
    """

    # Hint: this is very similar to find_runs, except
    # you'll need to keep track of whether the "current run"
    # is ascending or descending.
    runs = []

    # Keep track of the start and end points of a run.
    run_start = 0
    run_end = 1
    new_run = True
    ascending = True

    while run_end < len(lst):
        # How can you tell if a run should continue?
        #   (When you do, update run_end.)
        if new_run:
            if lst[run_end] > lst[run_end - 1]:
                ascending = True
            else:
                ascending = False

        if lst[run_end] > lst[run_end - 1] and ascending:
            run_end += 1
            new_run = False
        elif lst[run_end] < lst[run_end - 1] and ascending:

            # found a run (that has ended)
            while (run_end - run_start) < 64 and run_end < len(lst):
                run_end += 1
                insertion_sort(lst, run_start, run_end)

            runs.append((run_start, run_end))
            limit_stack(runs, lst)

            run_start = run_end
            run_end = run_start + 1
            new_run = True

        elif lst[run_end] < lst[run_end - 1] and not ascending:
            run_end += 1
            new_run = False
        elif lst[run_end] > lst[run_end - 1] and not ascending:

            # found a run (that has ended)
            while (run_end - run_start) < 64 and run_end < len(lst):
                run_end += 1
                insertion_sort(lst, run_start, run_end)

            runs.append((run_start, run_end))
            limit_stack(runs, lst)

            run_start = run_end
            run_end = run_start + 1
            new_run = True
            # reverse_run(lst, run_start, run_end)

    if lst and run_start < len(lst):
        runs.append((run_start, run_end))
        limit_stack(runs, lst)
        if not ascending:
            reverse_run(lst, run_start, run_end)

    return runs


def limit_stack(runs: list, lst: list) -> None:
    """Merges runs if there are 3 or more runs in lst.
    """
    if len(runs) >= 3:

        c, b, a = runs[-1][1] - runs[-1][0], \
                  runs[-2][1] - runs[-2][0], \
                  runs[-3][1] - runs[-3][0]

        while (b <= c or a <= b + c) and len(runs) > 1:
            if b <= c:
                _merge2(lst, runs[-2][0], runs[-2][1], runs[-1][1])
                runs[-2] = (runs[-2][0], runs[-1][1])
                runs.pop()

                # now there are 2 runs, when starting with 3
                # need to figure out what to do when there are 2, as there will
                # be an index error below
                if len(runs) >= 3:
                    c, b, a = runs[-1][1] - runs[-1][0], \
                              runs[-2][1] - runs[-2][0], \
                              runs[-3][1] - runs[-3][0]
                else:
                    # merge so len(run) == 1, ending while loop
                    _merge2(lst, runs[-2][0], runs[-2][1], runs[-1][1])
                    runs[-2] = (runs[-2][0], runs[-1][1])
                    runs.pop()
                    # doesn't matter what c, b, a are since len(runs) == 1

            if a <= b + c and len(runs) > 1:
                if a < c:
                    _merge2(lst, runs[-3][0], runs[-3][1], runs[-2][1])
                    runs[-3] = (runs[-3][0], runs[-2][1])
                    del(runs[-2])

                else:
                    _merge2(lst, runs[-2][0], runs[-2][1], runs[-1][1])
                    runs[-2] = (runs[-2][0], runs[-1][1])
                    runs.pop()

                if len(runs) >= 3:
                    c, b, a = runs[-1][1] - runs[-1][0], \
                              runs[-2][1] - runs[-2][0], \
                              runs[-3][1] - runs[-3][0]
                else:
                    # merge so len(run) == 1, ending while loop
                    _merge2(lst, runs[-2][0], runs[-2][1], runs[-1][1])
                    runs[-2] = (runs[-2][0], runs[-1][1])
                    runs.pop()
                    # doesn't matter what c, b, a are since len(runs) == 1


        # c, b, a = runs.pop(), runs.pop(), runs.pop()
        # if len(b) > len(c) and len(a) > len(b) + len(c):
        #     runs.append(a)
        #     runs.append(b)
        #     runs.append(c)
        #     # returns runs to original state
        # else:
            # while len(b) <= len(c) or len(a) <= len(b) + len(c):
            #     if len(b) <= len(c):
            #         _merge2(lst, b[0], b[1], c[1])
            #         d = (b[0], c[1])
            #         runs.append(a)
            #         runs.append(d)
            #     elif len(a) <= len(b) + len(c):
            #         if len(a) < len(c):
            #             _merge2(lst, a[0], a[1], b[1])
            #             d = (a[0], b[1])
            #
            #             runs.append(d)
            #         else:
            #             _merge2(lst, b[0], b[1], c[1])
            #             d = (b[0], c[1])
            #             runs.append(d)
