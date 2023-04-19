
from __future__ import annotations
from board import Board
from collections.abc import Callable
import numpy as np
import copy
from queue import PriorityQueue
import time
from tqdm import tqdm

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
    for i in range(1,9):
        distances.append(np.subtract(np.argwhere(sol == i),np.argwhere(state == i)))
    
    return np.sum(np.abs(np.array(distances)))

# Non-admissible Heuristic
def NA(board: Board) -> int: 
    return CB(board) + 1


class Node:
    def __init__(self, parent=None, board=None, action=None) -> None:
        self.parent = parent
        self.board = board
        
        self.g = 0
        self.h = 0
        self.f = 0
        
        self.path = self._set_path(action)
        
        
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
    
'''
A* Search 
'''
def a_star_search(board: Board, heuristic: Callable[[Board], int]):
    
    start_node = Node(parent=None, board=board)
    
    open_list = PriorityQueue()
    closed_list = set()
    
    open_list.put(start_node)
    
    start_time = time.time()

    TIME_LIMIT_SECS = 60
    with tqdm(total=TIME_LIMIT_SECS, desc="Timer") as pbar:
        while not open_list.empty():

            # Update progress bar
            pbar.update(int(time.time() - start_time) - pbar.n)
            
            # Check if elapsed time exceeds 300 seconds
            if time.time() - start_time > TIME_LIMIT_SECS:
                return []
            
            # Get the current node
            current_node = open_list.get()

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
                found = False
                for open_node in open_list.queue:
                    if child == open_node and child.g > open_node.g:
                        found = True
                        break
                    elif child == open_node and child.g <= open_node.g:
                        open_list.queue.remove(open_node)
                        open_list.put(child)
                        found = True
                        break
                    
                if not found:
                    open_list.put(child)
        
    # goal not reachable
    pbar.close()
    return None