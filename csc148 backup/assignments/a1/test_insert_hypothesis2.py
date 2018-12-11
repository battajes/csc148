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

from algorithms import PushyPassenger, RandomAlgorithm, ShortSighted, RandomArrivals, FileArrivals
from simulation import Simulation

# Note: you'll need to implement insert_after in a file called
# 'insert.py' for this import to work.
# Check the "Testing" slides for the docstring for insert_after.

@given(integers(), integers())
def test_random_arrival_generator_zero(max_floor: int, num_per_round: int) -> None:
    """Test the random arrival generator for two rounds: 0 and 5.

    Note that this test just checks that the range of possible values
    for the random people are correct.
    """

    random_generator = RandomArrivals(max_floor, num_per_round)

    for round_num in [0, 5]:
        arrivals = random_generator.generate(round_num)
        all_people = []
        for floor, people in arrivals.items():
            # Check that the floor is in the correct range.
            assert 1 <= floor <= max_floor

            all_people.extend(people)

        # Check that the right number of people were generated.
        assert num_per_round == len(all_people)

        for p in all_people:
            # Check floor boundaries
            assert 1 <= p.start <= max_floor
            assert 1 <= p.target <= max_floor

            # Check that the start and target floors are different.
            assert p.start != p.target
#
# if __name__ == '__main__':
#     import pytest
#     pytest.main(['test_random_arrival_generator_zero'])
