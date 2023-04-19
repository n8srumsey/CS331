import pandas as pd
import time
from tqdm import tqdm
from agent import BF, MT, CB, NA, a_star_search, Node
from board import Board
import os

if __name__ == "__main__":
    heuristics = [BF, MT, CB, NA]
    if os.path.exists('results.csv'):
        heuristics = [NA]
    
    df = pd.DataFrame(columns=['m', 'n', 'heuristic', 'cpu_time', 'correct', 'solution_length', 'search_nodes_generated'])

    for m in [10,20,30,40,50]:
        print(f'========================\nTesting Problem {m}\n========================')
        for heuristic in heuristics:
            print(f'Testing Heuristic {heuristic.__name__}')
            for seed in tqdm(range(0,10)):
                board = Board(m, seed)
                
                start =  time.process_time()
                solution = a_star_search(board, heuristic)
                end =  time.process_time()
                
                solution_cpu_time = end-start
                correct = board.check_solution(solution)
                sol_length = len(solution)
                search_nodes_generated = Node.n_search_nodes
                
                df.update(pd.DataFrame([[m, seed, heuristic.__name__, solution_cpu_time, correct, sol_length, search_nodes_generated]], 
                                       columns=['m', 'n', 'heuristic', 'cpu_time', 'correct', 'solution_length', 'search_nodes_generated']))
    
    if os.path.exists('results.csv'):
        df = pd.concat([df, pd.read_csv('results.csv')])
    df.to_csv('results.csv', index=False)
