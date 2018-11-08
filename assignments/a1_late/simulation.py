"""CSC148 Assignment 1 - Simulation

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This contains the main Simulation class that is actually responsible for
creating and running the simulation. You'll also find the function `sample_run`
here at the bottom of the file, which you can use as a starting point to run
your simulation on a small configuration.

Note that we have provided a fairly comprehensive list of attributes for
Simulation already. You may add your own *private* attributes, but should not
remove any of the existing attributes.
"""
# You may import more things from these modules (e.g., additional types from
# typing), but you may not import from any other modules.
from typing import Dict, List, Any
import algorithms
# from algorithms import Direction
from entities import Person, Elevator
from visualizer import Visualizer


class Simulation:
    """The main simulation class.

    === Attributes ===
    arrival_generator: the algorithm used to generate new arrivals.
    elevators: a list of the elevators in the simulation
    moving_algorithm: the algorithm used to decide how to move elevators
    num_floors: the number of floors
    visualizer: the Pygame visualizer used to visualize this simulation
    waiting: a dictionary of people waiting for an elevator
             (keys are floor numbers, values are the list of waiting people)
    """
    elevators: List[Elevator]
    arrival_generator: algorithms.ArrivalGenerator
    moving_algorithm: algorithms.MovingAlgorithm
    num_floors: int
    visualizer: Visualizer
    waiting: Dict[int, List[Person]]
    num_people_per_round: int
    num_iterations: int
    total_people: int
    times_completed: List

    def __init__(self,
                 config: Dict[str, Any]) -> None:
        """Initialize a new simulation using the given configuration."""

        self.elevators = []
        for _ in range(config['num_elevators']):
            new_elevator = Elevator(config['elevator_capacity'])
            self.elevators.append(new_elevator)

        self.arrival_generator = config['arrival_generator']
        self.moving_algorithm = config['moving_algorithm']
        self.num_floors = config['num_floors']

        self.visualizer = Visualizer(self.elevators,
                                     self.num_floors,
                                     config['visualize'])

        self.waiting = dict.fromkeys(range(1, self.num_floors + 1), [])
        self.num_people_per_round = config['num_people_per_round']

        # Summary Statistics:
        self.num_iterations = 0
        self.total_people = 0
        self.times_completed = []

    ############################################################################
    # Handle rounds of simulation.
    ############################################################################
    def run(self, num_rounds: int) -> Dict[str, Any]:
        """Run the simulation for the given number of rounds.

        Return a set of statistics for this simulation run, as specified in the
        assignment handout.

        Precondition: num_rounds >= 1.

        Note: each run of the simulation starts from the same initial state
        (no people, all elevators are empty and start at floor 1).
        """
        for i in range(num_rounds):
            self.visualizer.render_header(i)

            # Stage 1: generate new arrivals
            self._generate_arrivals(i)

            # Stage 2: leave elevators
            self._handle_leaving()

            # Stage 3: board elevators
            self._handle_boarding()

            # Stage 4: move the elevators using the moving algorithm
            self._move_elevators()

            # Pause for 1 second
            self.visualizer.wait(1)

        return self._calculate_stats()

    def _generate_arrivals(self, round_num: int) -> None:
        """Generate and visualize new arrivals."""

        # Update waiting_time of people waiting for elevators
        if self.waiting != {}:
            for floor in self.waiting:
                for person in self.waiting[floor]:
                    person.wait_time += 1

        # Generate new people, and add number of people to counter
        new_arrivals = self.arrival_generator.generate(round_num)
        people_counter = 0
        for floor in new_arrivals:
            people_counter += len(new_arrivals[floor])
        self.total_people += people_counter

        # Update dictionary of waiting people
        for floor in self.waiting:
            if new_arrivals[floor]:
                self.waiting[floor] = self.waiting[floor] + new_arrivals[floor]

        # Call visualizer show arrivals to show the new arrivals
        Visualizer.show_arrivals(self.visualizer, self.waiting)

    def _handle_leaving(self) -> None:
        """Handle people leaving elevators."""
        indices = []
        for j in range(len(self.elevators)):
            for i in range(len(self.elevators[j].passengers)):
                # if getting off or staying on both need to increase wait time
                self.elevators[j].passengers[i].wait_time += 1
                if self.elevators[j].passengers[i].target == \
                        self.elevators[j].floor:
                    Visualizer.show_disembarking(self.visualizer,
                                                 self.elevators[
                                                     j].passengers[
                                                         i],
                                                 self.elevators[j])
                    indices.append([j, i])

        while indices:
            index = indices.pop(-1)
            arrival = self.elevators[index[0]].passengers.pop(index[1])
            # update list of final wait times for arrivals at destination
            self.times_completed.append(arrival.wait_time)

    def _handle_boarding(self) -> None:
        """Handle boarding of people and visualize."""

        for elevator in self.elevators:
            while (self.waiting[elevator.floor]) and \
                    len(elevator.passengers) < elevator.capacity:
                new_passenger = self.waiting[elevator.floor].pop(0)
                elevator.passengers.append(new_passenger)
                Visualizer.show_boarding(self.visualizer,
                                         new_passenger,
                                         elevator)

    def _move_elevators(self) -> None:
        """Move the elevators in this simulation.

        Use this simulation's moving algorithm to move the elevators.
        """
        moves = self.moving_algorithm.move_elevators(self.elevators,
                                                     self.waiting,
                                                     self.num_floors)

        for i in range(len(moves)):
            self.elevators[i].floor += moves[i].value
            # if self.elevators[i].floor < 1:
            #     self.elevators[i].floor = 1
            #     moves[i] = Direction.STAY
            # if self.elevators[i].floor > self.num_floors:
            #     self.elevators[i].floor = self.num_floors
            #     moves[i] = Direction.STAY

        Visualizer.show_elevator_moves(self.visualizer, self.elevators, moves)
        self.num_iterations += 1

    ############################################################################
    # Statistics calculations
    ############################################################################
    def _calculate_stats(self) -> Dict[str, int]:
        """Report the statistics for the current run of this simulation.
        """
        times = self.times_completed
        min_time = -1
        max_time = -1
        avg_time = -1
        if times:
            avg_time = int(sum(times)/len(times))
            min_time = times[0]
            for time in times:
                if time > max_time:
                    max_time = time
                if time < min_time:
                    min_time = time

        return {
            'num_iterations': self.num_iterations,
            'total_people': self.total_people,
            'people_completed': len(times),
            'max_time': max_time,
            'min_time': min_time,
            'avg_time': avg_time
        }


def sample_run() -> Dict[str, int]:
    """Run a sample simulation, and return the simulation statistics."""
    config = {
        'num_floors': 6,
        'num_elevators': 6,
        'elevator_capacity': 3,
        'num_people_per_round': 2,
        # Random arrival generator with 6 max floors and 2 arrivals per round.
        'arrival_generator': algorithms.RandomArrivals(6, 2),
        'moving_algorithm': algorithms.RandomAlgorithm(),
        'visualize': False
    }
    sim = Simulation(config)
    stats = sim.run(15)
    return stats


if __name__ == '__main__':
    # Uncomment this line to run our sample simulation (and print the
    # statistics generated by the simulation).
    print(sample_run())

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['entities', 'visualizer', 'algorithms', 'time'],
        'max-nested-blocks': 4,
        'disable': ['R0201'],
        'max-attributes': 12

    })
