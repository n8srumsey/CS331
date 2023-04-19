
from __future__ import annotations
from board import Board
from collections.abc import Callable
import numpy as np
import copy
from queue import PriorityQueue
import time

'''
Heuristics
'''
# Breadth First Search Heuristic


def BF(board: Board) -> int:
    return 0

# Number of Misplaced Tiles Heuristic


def MT(board: Board) -> int:
    sol = board.solution
    state = board.state

    misplaced = 0
    for i in range(1, 9):
        goal_pos = np.argwhere(sol == i)[0]
        current_pos = np.argwhere(state == i)[0]
        if not np.array_equal(goal_pos, current_pos):
            misplaced += 1

    return misplaced

# Manhattan Distance Heuristic


def CB(board: Board) -> int:
    sol = board.solution
    state = board.state

    distances = []
    for i in range(1, 9):
        distances.append(np.subtract(np.argwhere(sol == i), np.argwhere(state == i)))

    return np.sum(np.abs(np.array(distances)))

# Non-admissible Heuristic
def NA(board: Board) -> int:
    # Non-admissible heuristic becuase in the case where the board is in the goal state, the heuristic will return 1
    return MT(board) + CB(board) + 1


class Node:
    n_search_nodes = 0

    def __init__(self, parent=None, board=None, action=None) -> None:
        self.parent = parent
        self.board = board

        self.g = 0
        self.h = 0
        self.f = 0

        self.path = self._set_path(action)

        Node.n_search_nodes += 1

    def _set_path(self, action: str):
        if self.parent is None or action is None:
            return []
        path = copy.copy(self.parent.path)
        path.append(action)
        return path

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Node):
            return np.array_equal(self.board.state, other.board.state)
        return False

    def __lt__(self, other):
        if self.f == other.f:
            return self.g > other.g
        return self.f < other.f

    def __str__(self) -> str:
        return self.path

    def __hash__(self) -> int:
        return hash(tuple(self.board.state.flatten()))

    def _reset():
        Node.n_search_nodes = 0


'''
A* Search 
'''


def a_star_search(board: Board, heuristic: Callable[[Board], int]):
    Node._reset()
    start_node = Node(parent=None, board=board)

    open_list = PriorityQueue()
    open_set = {}
    closed_list = set()

    open_list.put(start_node)
    open_set.update({hash(start_node): start_node})
    
    start_time = time.time()

    TIME_LIMIT_SECS = 60

    while not open_list.empty():

        # Check if elapsed time exceeds 300 seconds
        if time.time() - start_time > TIME_LIMIT_SECS:
            return []

        # Get the current node
        current_node = open_list.get()
        if current_node in open_set:
            open_set.pop(hash(current_node))
        
        # Found the goal
        if current_node.board.goal_test():
            return current_node.path

        # Add current to closed list
        closed_list.add(current_node)

        # Generate children
        children = []
        for new_state, action in current_node.board.next_action_states():
            new_node = Node(current_node, new_state, action)
            if new_node not in closed_list:
                children.append(new_node)

        # Loop through children
        for child in children:

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = heuristic(child.board)
            child.f = child.g + child.h

            # Child is already in the open list
            if child in open_set:
                # get node 'open_node' from open_set that has the same hash as child without using next()
                open_node = open_set[hash(child)]
                if child.g <= open_node.g:
                    open_list.queue.remove(open_node)
                    open_list.put(child)
                    open_set[hash(child)] = child
            else:
                open_list.put(child)
                open_set.update({hash(child): child})

    # goal not reachable
    return None
