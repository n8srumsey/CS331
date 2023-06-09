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
    # Get states
    sol = board.solution
    state = board.state

    misplaced = 0
    # Loop through each tile to check if it is in the correct position
    for i in range(1, 9):
        # Get position of tile in current and goal state
        goal_pos = np.argwhere(sol == i)[0]
        current_pos = np.argwhere(state == i)[0]
        
        # If not in goal position, increment misplaced
        if not np.array_equal(goal_pos, current_pos):
            misplaced += 1

    # Return result
    return misplaced

# Manhattan Distance Heuristic
def CB(board: Board) -> int:
    # Get states
    sol = board.solution
    state = board.state

    # Get distances between each tile and its goal position
    distances = []
    for i in range(1, 9):
        distances.append(np.subtract(np.argwhere(sol == i), np.argwhere(state == i)))

    # Return sum of distances
    return np.sum(np.abs(np.array(distances)))

# Non-admissible Heuristic
def NA(board: Board) -> int:
    # Non-admissible heuristic becuase in the case where the board is in the goal state, 
    # the heuristic will return 1
    return MT(board) + CB(board) + 1

""" Node Class to keep track of path in A* Search """
class Node:
    n_search_nodes = 0

    # Initialize Values
    def __init__(self, parent=None, board=None, action=None) -> None:
        self.parent = parent
        self.board = board

        self.g = 0 # Cost to get to this node
        self.h = 0 # Heuristic value
        self.f = 0 # F-score

        self.path = self._set_path(action)

        Node.n_search_nodes += 1

    # Update path
    def _set_path(self, action: str):
        if self.parent is None or action is None:
            return []
        
        path = copy.copy(self.parent.path)
        path.append(action)
        
        return path

    # Check if node is equal in state to another
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Node):
            return np.array_equal(self.board.state, other.board.state)
        return False

    # Check if f-score is less than another, with tie-breaking on g-score
    def __lt__(self, other):
        if self.f == other.f:
            return self.g > other.g
        return self.f < other.f

    # Print path
    def __str__(self) -> str:
        return self.path

    # Hash function for sets and dictionaries
    def __hash__(self) -> int:
        return hash(tuple(self.board.state.flatten()))

    # Reset number of search nodes between searches
    def _reset():
        Node.n_search_nodes = 0


'''
A* Search 
'''
def a_star_search(board: Board, heuristic: Callable[[Board], int]):
    Node._reset() # Reset number of search nodes for this search
    
    # Create start node
    start_node = Node(parent=None, board=board)

    # Create the open and closed lists
    open_list = PriorityQueue()
    open_set = {}
    closed_list = set()

    # Add first node to the open list
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
                
                # If the child's f is less than open_node's f, replace open_node with child
                if child.f <= open_node.f:
                    open_list.queue.remove(open_node)
                    open_list.put(child)
                    open_set[hash(child)] = child
            
            # If child is not in open list, add it to the open list
            else:
                open_list.put(child)
                open_set.update({hash(child): child})

    # goal not reachable
    return None
