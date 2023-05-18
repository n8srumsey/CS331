import pandas as pd
import os

from GameDriver import GameDriver
from Plot import plot_svd

BOARD_SIZE = 4

heuristics = ["0", "1", "2"]
pruning = ["0", "1"]
svd_depths = ["2", "4", "6", "8", "10", "12"]
hq_depths = ["2", "4", "6", "8"]

def test_configuration(p1_heuristic, p1_prune, p1_depth, 
                       p2_heuristic, p2_prune, p2_depth):
    game = GameDriver(p1type="alphabeta", p2type="alphabeta", num_rows=BOARD_SIZE, num_cols=BOARD_SIZE, 
                      p1_eval_type=p1_heuristic, p1_prune=p1_prune, 
                      p2_eval_type=p2_heuristic, p2_prune=p2_prune, 
                      p1_depth=p1_depth, p2_depth=p2_depth)
    game.run()
    return game.p1.total_nodes_seen, game.p2.total_nodes_seen, game.state

def test_depths(p1_heuristic, p1_prune, p2_heuristic, p2_prune, depths):
    p1_nodes_seen = []
    p2_nodes_seen = []
    states = []
    for depth in depths:
        p1, p2, s = test_configuration(p1_heuristic, p1_prune, depth, p2_heuristic, p2_prune, depth)
        p1_nodes_seen.append(p1)
        p2_nodes_seen.append(p2)
        states.append(s)
    return p1_nodes_seen, p2_nodes_seen, states

def test_search_vs_depth():
    """
    Results Format:
    'heuristic': int
    'prune': int
    'depth': int
    'nodes_expanded': int
    """
    results = []
    
    # Test every permutation of heursitics and pruning for each player at each depth
    for h1 in heuristics:
        for h2 in heuristics:
            for p1 in pruning:
                for p2 in pruning:
                    n1, n2, _ = test_depths(h1, p1, h2, p2, depths=svd_depths)
                    # Report P1 stats
                    for n, d in zip(n1, svd_depths):
                        results.append({'heuristic': h1, 'prune': p1, 'depth': d, 'nodes_expanded': n})
                        
                    # Report P2 stats
                    for n, d in zip(n2, svd_depths):
                        results.append({'heuristic': h2, 'prune': p2, 'depth': d, 'nodes_expanded': n})
                   
    # Construct dataframe and save to csv
    df = pd.DataFrame(results)
    df.to_csv('svd_results.csv', index=False)
    
    
def parse_state(s: int) -> int:
    """ Parses the state result of a game and returns 1 if P1 wins, -1 if P2 wins, and 0 if tie """
    if s > 0:
        return 1
    elif s < 0:
        return -1
    return 0    

def test_heuristic_quality():
    """
    Results Format:
    'h1': int
    'h2': int
    'depth': int
    'state': int
    """
    
    # Test every permutation of heuristics for each player at each depth
    results = []
    for h1 in heuristics:
        for h2 in heuristics:
            _, _, states = test_depths(h1, "1", h2, "1", depths=hq_depths)
            for s, d in zip(states, hq_depths):
                results.append({'h1': h1, 'h2': h2, 'depth': d, 'state': parse_state(s)})
    
    # Construct dataframe and save to csv
    df = pd.DataFrame(results)
    df.to_csv('hq_results.csv', index=False)
        

def report_heuristic_quality():
    # Load results
    df = pd.read_csv('hq_results.csv')
    
    class WinLossResults:
        """ Class to store win/loss/tie results for a heuristic """
        def __init__(self):
            # Initialize to 0
            self.wins = 0
            self.losses = 0
            self.ties = 0
            
        def __str__(self):
            # Return string representation
            return f'Wins: {self.wins}, Losses: {self.losses}, Ties: {self.ties}'
        
        def update(self, state):
            # Update results based on state
            if state > 0:
                self.wins += 1
            elif state < 0:
                self.losses += 1
            else:
                self.ties += 1
    
    # Create win/loss/tie results for each heuristic
    win_loss_ratios = []
    for h1 in heuristics:
        # Initialize list for h1 against all P2 heuristics
        win_loss_ratios.append([])
        for h2 in heuristics:
            # Load results into list
            results = WinLossResults()
            for _, row in df.iterrows():
                if str(row['h1']) == h1 and str(row['h2']) == h2:
                    results.update(row['state'])
            win_loss_ratios[int(h1)].append(results)
    
    # Print results
    for h1 in heuristics:
        for h2 in heuristics:
            if h1 == h2:
                continue
            print(f'Heuristic {h1} vs. Heuristic {h2}')
            print(win_loss_ratios[int(h1)][int(h2)])
            print()
          
    # Calculate total victories for each heuristic  
    total_victories = [0] * 3
    for h1 in heuristics:
        for h2 in heuristics:
            if h1 == h2:
                continue
            total_victories[int(h1)] += win_loss_ratios[int(h1)][int(h2)].wins
            total_victories[int(h2)] += win_loss_ratios[int(h1)][int(h2)].losses
    
    # Print total victories
    for h in heuristics:
        print(f'Heuristic {h} total victories: {total_victories[int(h)]}')
    print()
    
    # Calculate total win rates for each heuristic
    p1_p2_win_rates = {}
    for d in hq_depths:
        p1_p2_win_rates[d] = {'p1': 0, 'p2': 0}
    for _, row in df.iterrows():
        if row['h1'] == row['h2']:
            continue
        if row['state'] == 1:
            p1_p2_win_rates[str(row['depth'])]['p1'] += 1
        if row['state'] == -1:
            p1_p2_win_rates[str(row['depth'])]['p2'] += 1
            
    # Print player win rates for each depth
    for d in hq_depths:
        print("Depth:", d)
        print("\tP1 Wins:", p1_p2_win_rates[d]['p1'])
        print("\tP1 Win Rate:", p1_p2_win_rates[d]['p1'] / (p1_p2_win_rates[d]['p1'] + p1_p2_win_rates[d]['p2']))
        print("\tP2 Wins:", p1_p2_win_rates[d]['p2'])
        print("\tP2 Win Rate:", p1_p2_win_rates[d]['p2'] / (p1_p2_win_rates[d]['p1'] + p1_p2_win_rates[d]['p2']))
        
if __name__ == '__main__':
    # Run tests if results don't exist
    if not os.path.exists('svd_results.csv'):
        test_search_vs_depth()
        
    # Run tests if results don't exist
    if not os.path.exists('hq_results.csv'):
        test_heuristic_quality()
        
    # Plot results
    plot_svd()
    
    # Report heuristic quality
    report_heuristic_quality()