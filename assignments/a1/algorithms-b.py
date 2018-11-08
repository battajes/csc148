"""CSC148 Assignment 1 - Algorithms

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module Description ===

This file contains two sets of algorithms: ones for generating new arrivals to
the simulation, and ones for making decisions about how elevators should move.

As with other files, you may not change any of the public behaviour (attributes,
methods) given in the starter code, but you can definitely add new attributes
and methods to complete your work here.

See the 'Arrival generation algorithms' and 'Elevator moving algorithsm'
sections of the assignment handout for a complete description of each algorithm
you are expected to implement in this file.
"""
import csv
from enum import Enum
import random
from typing import Dict, List, Optional

from entities import Person, Elevator


###############################################################################
# Arrival generation algorithms
###############################################################################
class ArrivalGenerator:
    """An algorithm for specifying arrivals at each round of the simulation.

    === Attributes ===
    max_floor: The maximum floor number for the building.
               Generated people should not have a starting or target floor
               beyond this floor.
    num_people: The number of people to generate, or None if this is left
                up to the algorithm itself.

    === Representation Invariants ===
    max_floor >= 2
    num_people is None or num_people >= 0
    """
    max_floor: int
    num_people: Optional[int]

    def __init__(self, max_floor: int, num_people: Optional[int]) -> None:
        """Initialize a new ArrivalGenerator.

        Preconditions:
            max_floor >= 2
            num_people is None or num_people >= 0
        """
        self.max_floor = max_floor
        self.num_people = num_people

    def generate(self, round_num: int) -> Dict[int, List[Person]]:
        """Return the new arrivals for the simulation at the given round.

        The returned dictionary maps floor number to the people who
        arrived starting at that floor.

        You can choose whether to include floors where no people arrived.
        """
        raise NotImplementedError


class RandomArrivals(ArrivalGenerator):
    """Generate a fixed number of random people each round.

    Generate 0 people if self.num_people is None.

    For our testing purposes, this class *must* have the same initializer header
    as ArrivalGenerator. So if you choose to to override the initializer, make
    sure to keep the header the same!

    Hint: look up the 'sample' function from random.
    """
    # people_map: Dict[int: List[Person]]

    def __init__(self, max_floor: int, num_people: Optional[int]) -> None:
        """Initialize a new ArrivalGenerator.
        Copied from above
        Preconditions:
            max_floor >= 2
            num_people is None or num_people >= 0
        """
        ArrivalGenerator.__init__(self, max_floor, num_people)
        self.people_map = dict.fromkeys(range(1, max_floor+1), [])
        # self.generate()
        # self.people_map = {}

    def floor(self) -> List[int]:
        """Returns pair of 2 random floors within building.
        """
        return random.sample(range(1, self.max_floor + 1), 2)

    def generate(self, round_num: int) -> Dict[int, List[Person]]:
        """Return the new arrivals for the simulation at the given round.

        The returned dictionary maps floor number to the people who
        arrived starting at that floor.

        You can choose whether to include floors where no people arrived.
        """
        for i in range(self.num_people):
            floors = self.floor()
            new_person = Person(floors[0], floors[1])
            self.people_map[floors[0]] = self.people_map[floors[0]]+[new_person]
        return self.people_map



class FileArrivals(ArrivalGenerator):
    """Generate arrivals from a CSV file.
    """

    # will see later if this needs to be sorted by floor, probably not?
    # people_rounds: Dict[int: List[Person]]

    def __init__(self, max_floor: int, filename: str) -> None:
        """Initialize a new FileArrivals algorithm from the given file.

        The num_people attribute of every FileArrivals instance is set to None,
        since the number of arrivals depends on the given file.

        Precondition:
            <filename> refers to a valid CSV file, following the specified
            format and restrictions from the assignment handout.
        """
        ArrivalGenerator.__init__(self, max_floor, None)
        # Might not be necessary to have an index for each floor.
        self.people_map = dict.fromkeys(range(1, max_floor + 1), [])
        self.rounds_map = {}
        self.filename = filename
        self.max_floor = max_floor

        # We've provided some of the "reading from csv files" boilerplate code
        # for you to help you get started.
        with open(self.filename) as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                round_num = int(line[0])
                temp_map = dict.fromkeys(range(1, max_floor + 1), [])
                for i in range(1, len(line)):
                    if i % 2 != 0:
                        temp_map[int(line[i])] = \
                            temp_map[int(line[i])] + \
                            [(Person(int(line[i]), int(line[i+1])))]
                self.rounds_map[round_num] = temp_map


    def generate(self, round_num: int) -> Dict[int, List[Person]]:
        """Return the new arrivals for the simulation at the given round.

                The returned dictionary maps floor number to the people who
                arrived starting at that floor.

                You can choose whether to include floors where no one arrived.
                """
        if round_num in self.rounds_map:
            return self.rounds_map[round_num]
        else:
            return dict.fromkeys(range(1, self.max_floor + 1), [])

        # return self.people_map

                # FIRST ATTEMPT:
                # self.people_rounds[int(line[0])] = []
                # for i in range(1, len(line)):
                #     if i % 2 != 0:
                #         self.people_rounds[int(line[0])].append(Person(int(line[i]), int(line[i+1])))

###############################################################################
# Elevator moving algorithms
###############################################################################
class Direction(Enum):
    """
    The following defines the possible directions an elevator can move.
    This is output by the simulation's algorithms.

    The possible values you'll use in your Python code are:
        Direction.UP, Direction.DOWN, Direction.STAY
    """
    UP = 1
    STAY = 0
    DOWN = -1


class MovingAlgorithm:
    """An algorithm to make decisions for moving an elevator at each round.
    """
    def move_elevators(self,
                       elevators: List[Elevator],
                       waiting: Dict[int, List[Person]],
                       max_floor: int) -> List[Direction]:
        """Return a list of directions for each elevator to move to.

        As input, this method receives the list of elevators in the simulation,
        a dictionary mapping floor number to a list of people waiting on
        that floor, and the maximum floor number in the simulation.

        Note that each returned direction should be valid:
            - An elevator at Floor 1 cannot move down.
            - An elevator at the top floor cannot move up.
        """
        raise NotImplementedError


class RandomAlgorithm(MovingAlgorithm):
    """A moving algorithm that picks a random direction for each elevator.
    """
    def move_elevators(self,
                       elevators: List[Elevator],
                       waiting: Dict[int, List[Person]],
                       max_floor: int) -> List[Direction]:
        """Return a list of directions for each elevator to move to.

        As input, this method receives the list of elevators in the simulation,
        a dictionary mapping floor number to a list of people waiting on
        that floor, and the maximum floor number in the simulation.

        Note that each returned direction should be valid:
            - An elevator at Floor 1 cannot move down.
            - An elevator at the top floor cannot move up.
        """
        elevator_moves = []
        direction = Direction

        for elevator in elevators:
            result = random.randint(1, 3)
            if result == 1:
                elevator_moves.append(direction.UP)
            elif result == 2:
                elevator_moves.append(direction.STAY)
            elif result == 3:
                elevator_moves.append(direction.DOWN)

        return elevator_moves


class PushyPassenger(MovingAlgorithm):
    """A moving algorithm that preferences the first passenger on each elevator.

    If the elevator is empty, it moves towards the *lowest* floor that has at
    least one person waiting, or stays still if there are no people waiting.

    If the elevator isn't empty, it moves towards the target floor of the
    *first* passenger who boarded the elevator.
    """
    pass


class ShortSighted(MovingAlgorithm):
    """A moving algorithm that preferences the closest possible choice.

    If the elevator is empty, it moves towards the *closest* floor that has at
    least one person waiting, or stays still if there are no people waiting.

    If the elevator isn't empty, it moves towards the closest target floor of
    all passengers who are on the elevator.

    In this case, the order in which people boarded does *not* matter.
    """
    pass


if __name__ == '__main__':
    # Don't forget to check your work regularly with python_ta!
    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['__init__'],
        'extra-imports': ['entities', 'random', 'csv', 'enum'],
        'max-nested-blocks': 4,
        'disable': ['R0201'],
        'max-attributes':12
    })
