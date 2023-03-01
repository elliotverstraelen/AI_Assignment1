#!/usr/bin/env python
"""
Name of the author(s):
- Auguste Burlats <auguste.burlats@uclouvain.be>
"""
import time
import sys
from copy import deepcopy
from search import *
import unittest


#################
# Problem class #
#################
class TowerSorting(Problem):

    def __init__(self, initial_state):
        self.initial = initial_state
        self.num_towers = initial_state.number
        self.max_tower_size = initial_state.size

    # The possible actions at any given state are moving a disk from the top
    # of one tower to another tower if and only if the target tower is either 
    # empty or its top disk has a larger size than the disk to be moved.
    def actions(self, state):
        actions = []
        # Loop through all pairs of towers
        for i in range(self.num_towers):
            for j in range(self.num_towers):
                # check if the pair of towers is distrinct
                if i != j:
                     # check if the source tower is not empty
                     if len(state.grid[i]) > 0:
                        # check if the target tower is either empty 
                        # or its top disk has a larger size
                        # than the disk to be moved
                        if len(state.grid[j]) == 0 or state.grid[i][-1] == state.grid[j][-1]:
                            actions.append((i, j))
        return actions

    def result(self, state, action):
        # Copy the current state to a new state
        new_state = deepcopy(state)
        # Remove the disk from the top of the source tower
        disk = new_state.grid[action[0]].pop()
        # Add the disk to the top of the target tower
        new_state.grid[action[1]].append(disk)
        # Return the new state
        return new_state

    def goal_test(self, state):
        # Loop through all towers
        for tower in state.grid:
            # check if the tower is not empty
            if len(tower) > 0:
                # Check if all disks in the tower are of the same color
                if len(set(tower)) != 1:
                    return False
        # Return True if all towers are uniform and complete
        return True

    def path_cost(self, c, state1, action, state2):
        # 1 for each action
        return c + 1


###############
# State class #
###############
class State:

    def __init__(self, number, size, grid, move="Init"):
        self.number = number
        self.size = size
        self.grid = grid
        self.move = move

    def __str__(self):
        s = self.move + "\n"
        for i in reversed(range(self.size)):
            for tower in self.grid:
                if len(tower) > i:
                    s += "".join(tower[i]) + " "
                else:
                    s += ". "
            s += "\n"
        return s

    # Not sure about implementation
    def __eq__(self, other):
        if isinstance(other, State):
            return self.grid == other.grid
        return False

    # Not sure about implementation
    def __hash__(self):
        return hash(tuple(map(tuple, self.grid)))


######################
# Auxiliary function #
######################
def read_instance_file(filepath):
    with open(filepath) as fd:
        lines = fd.read().splitlines()

    number_tower, size_tower = tuple([int(i) for i in lines[0].split(" ")])
    initial_grid = [[] for i in range(number_tower)]
    for row in lines[1:size_tower+1]:
        elems = row.split(" ")
        for index in range(number_tower):
            if elems[index] != '.':
                initial_grid[index].append(elems[index])

    for tower in initial_grid:
        tower.reverse()

    return number_tower, size_tower, initial_grid


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: ./sort_tower.py <path_to_instance_file>")
    filepath = sys.argv[1]

    number, size, initial_grid = read_instance_file(filepath)

    init_state = State(number, size, initial_grid, "Init")
    problem = TowerSorting(init_state)
    # Example of search
    start_timer = time.perf_counter()
    node, nb_explored, remaining_nodes = depth_first_tree_search(problem)
    end_timer = time.perf_counter()

    # Example of print
    path = node.path()

    for n in path:
        # assuming that the __str__ function of state outputs the correct format
        print(n.state)

    print("* Execution time:\t", str(end_timer - start_timer))
    print("* Path cost to goal:\t", node.depth, "moves")
    print("* #Nodes explored:\t", nb_explored)
    print("* Queue size at goal:\t",  remaining_nodes)

class TestTowerSorting(unittest.TestCase):

    def test_initial_state(self):
        ts = TowerSorting(3)
        state = ts.initial_state()
        expected = [[3, 2, 1], [], []]
        self.assertEqual(state.grid, expected)

    def test_actions(self):
        pass

    def test_result(self):
        pass

    def test_goal_test(self):
        pass


