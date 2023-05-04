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
    
    for h1 in heuristics:
        for h2 in heuristics:
            for p1 in pruning:
                for p2 in pruning:
                    n1, n2, _ = test_depths(h1, p1, h2, p2, depths=svd_depths)
                    for n, d in zip(n1, svd_depths):
                        results.append({'heuristic': h1, 'prune': p1, 'depth': d, 'nodes_expanded': n})
                    for n, d in zip(n2, svd_depths):
                        results.append({'heuristic': h2, 'prune': p2, 'depth': d, 'nodes_expanded': n})
                        
    df = pd.DataFrame(results)
    
    df.to_csv('svd_results.csv', index=False)
    
def parse_state(s: int) -> int:
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
    
    results = []
    for h1 in heuristics:
        for h2 in heuristics:
            _, _, states = test_depths(h1, 1, h2, 1, depths=hq_depths)
            for s, d in zip(states, hq_depths):
                results.append({'h1': h1, 'h2': h2, 'depth': d, 'state': parse_state(s)})
                
    df = pd.DataFrame(results)
    
    df.to_csv('hq_results.csv', index=False)
        

def report_heuristic_quality():
    df = pd.read_csv('hq_results.csv')
    
    class WinLossResults:
        def __init__(self):
            self.wins = 0
            self.losses = 0
            self.ties = 0
            
        def __str__(self):
            return f'Wins: {self.wins}, Losses: {self.losses}, Ties: {self.ties}'
        
        def update(self, state):
            if state > 0:
                self.wins += 1
            elif state < 0:
                self.losses += 1
            else:
                self.ties += 1
    
    win_loss_ratios = []
    for h1 in heuristics:
        win_loss_ratios.append([])
        for h2 in heuristics:
            results = WinLossResults()
            for _, row in df.iterrows():
                if row['h1'] == h1 and row['h2'] == h2:
                    results.update(row['state'])
            win_loss_ratios[h1].append(results)
    
    for h1 in heuristics:
        for h2 in heuristics:
            if h1 == h2:
                continue
            
            print(f'Heuristic {h1} vs. Heuristic {h2}')
            print(win_loss_ratios[h1][h2])
            print()
    
        

if __name__ == '__main__':
    if not os.path.exists('svd_results.csv'):
        test_search_vs_depth()
    if not os.path.exists('hq_results.csv'):
        test_heuristic_quality()
    plot_svd()
    report_heuristic_quality()