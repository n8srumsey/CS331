import pandas as pd
import time
from tqdm import tqdm
from agent import BF, MT, CB, NA, a_star_search, Node
from board import Board

if __name__ == "__main__":
    # List of all heuristics to evaluate
    heuristics = [BF, MT, CB, NA]

    # Create a dataframe to store the results
    df = pd.DataFrame(columns=['m', 'n', 'heuristic', 'cpu_time', 'correct', 
                               'solution_length', 'search_nodes_generated']).astype({'correct': 'bool'})
    
    # For each case where the initial state is shuffled m times (m = 10, 20, 30, 40, 50)
    for m in [10,20,30,40,50]:
        print(f'========================\nTesting Problem {m}\n========================')
        # Test Each Heuristic
        for heuristic in heuristics:
            print(f'Testing Heuristic {heuristic.__name__}')
            for seed in tqdm(range(0,10)):
                # Initialize the board
                board = Board(m, seed)
                
                # Run A* Search and time execution
                start =  time.process_time()
                solution = a_star_search(board, heuristic)
                end =  time.process_time()
                
                # Calculate results
                solution_cpu_time = end-start
                correct = board.check_solution(solution)
                sol_length = len(solution)
                search_nodes_generated = Node.n_search_nodes
                
                # Generate result dataframe for instance
                result = pd.DataFrame([[m, seed, heuristic.__name__, solution_cpu_time, correct, sol_length, search_nodes_generated]], 
                                       columns=['m', 'n', 'heuristic', 'cpu_time', 'correct', 'solution_length', 'search_nodes_generated'])
                
                # Append result to Result Dataframe
                df = pd.concat([df, result], ignore_index=True)
    
    # Save Results
    df.to_csv('results.csv', index=False)
