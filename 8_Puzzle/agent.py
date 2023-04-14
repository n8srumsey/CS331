from __future__ import annotations
from board import Board
from collections.abc import Callable
import numpy as np
import copy
from queue import PriorityQueue
'''
Heuristics
'''
def BF(board: Board) -> int: # Breadth First Search
    return 0

def MT(board: Board) -> int:
    sol = board.solution
    state = board.state
    
    distances = []
    for i in range(1, 9):
        goal_pos = np.argwhere(sol == i)[0]
        current_pos = np.argwhere(state == i)[0]
        if not np.array_equal(goal_pos, current_pos):
            distances.append(np.abs(goal_pos - current_pos).sum())
    
    return sum(distances)
    

def CB(board: Board) -> int: # Manhattan Distance
    sol = board.solution
    state = board.state
    
    distances = []
    for i in range(1,9):
        distances.append(np.subtract(np.argwhere(sol == i),np.argwhere(state == i)))
    
    return np.sum(np.abs(np.array(distances)))

def NA(board: Board) -> int: # Custom Non-admissible Heuristic
    sol = board.solution
    state = board.state
    
    n_conflicts = 0
    for r in range(3):
        for c in range(3):
            val = state[r, c]
            if val != 0:
                goal_row = (val - 1) // 3
                goal_col = (val - 1) % 3
                
                if r == goal_row:
                    for i in range(3):
                        if i != c and state[r, i] != 0 and state[r, i] < val and i < goal_col:
                            n_conflicts += 1
                            
                if c == goal_col:
                    for i in range(3):
                        if i != r and state[i, c] != 0 and state[i, c] < val and i < goal_row:
                            n_conflicts += 1
                
    return n_conflicts


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
        return self.board == other.board
    
    def __lt__(self, other):
        return self.f < other.f
    
    def __str__(self) -> str:
        return self.path
    
'''
A* Search 
'''
def a_star_search(board: Board, heuristic: Callable[[Board], int]):
    
    start_node = Node(parent=None, board=board)
    
    open_list = PriorityQueue()
    closed_list = []
    
    open_list.put(start_node)
    
    while not open_list.empty():
        # Get the current node
        current_node = open_list.get()

        # Add current to closed list
        closed_list.append(current_node)

        # Found the goal
        if current_node.board.goal_test():
            return current_node.path

        # Generate children
        children = []
        for new_state, action in current_node.board.next_action_states():
            new_node = Node(current_node, new_state, action)
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

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
    return None