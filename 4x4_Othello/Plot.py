from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

def plot_svd(mode='line_err'):
    df = pd.read_csv('svd_results.csv')
    
    prune_off = df[df['prune'] == 0]
    prune_on = df[df['prune'] == 1]
    
    
    if mode == 'line_err':
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

        # Calculate the maximum jitter amount based on the number of unique depths
        max_jitter = 0.05 * len(prune_off['depth'].unique())

        for i, (key, grp) in enumerate(prune_off.groupby(['heuristic'])):
            means = grp.groupby('depth')['nodes_expanded'].mean()
            stds = grp.groupby('depth')['nodes_expanded'].std()
            
            # Add horizontal jitter to the x-values of the error bars
            x_jitter = np.random.uniform(-max_jitter, max_jitter, len(means.index))
            x_values = means.index + x_jitter
            
            ax1.errorbar(x_values, means, yerr=stds, label=key, marker='o', linestyle='-', capsize=4)

        ax1.legend(loc='best')
        ax1.set_title('Nodes Expanded vs. Depth: No Pruning')
        ax1.set_xlabel('Depth')
        ax1.set_ylabel('Nodes Expanded')

        for i, (key, grp) in enumerate(prune_on.groupby(['heuristic'])):
            means = grp.groupby('depth')['nodes_expanded'].mean()
            stds = grp.groupby('depth')['nodes_expanded'].std()
            
            # Add horizontal jitter to the x-values of the error bars
            x_jitter = np.random.uniform(-max_jitter, max_jitter, len(means.index))
            x_values = means.index + x_jitter
            
            ax2.errorbar(x_values, means, yerr=stds, label=key, marker='o', linestyle='-', capsize=4)

        ax2.legend(loc='best')
        ax2.set_title('Nodes Expanded vs. Depth: With Pruning')
        ax2.set_xlabel('Depth')
        ax2.set_ylabel('Nodes Expanded')

        plt.tight_layout()
        plt.show()
    
    elif mode=='scatter':
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

        colors = plt.cm.tab10(np.linspace(0, 1, len(prune_off['heuristic'].unique())))

        for i, (key, grp) in enumerate(prune_off.groupby(['heuristic'])):
            grp.plot(ax=ax1, kind='scatter', x='depth', y='nodes_expanded', label=key, color=colors[i])

        ax1.legend(loc='best')
        ax1.set_title('Nodes Expanded vs. Depth: No Pruning')
        ax1.set_xlabel('Depth')
        ax1.set_ylabel('Nodes Expanded')

        for i, (key, grp) in enumerate(prune_on.groupby(['heuristic'])):
            grp.plot(ax=ax2, kind='scatter', x='depth', y='nodes_expanded', label=key, color=colors[i])

        ax2.legend(loc='best')
        ax2.set_title('Nodes Expanded vs. Depth: With Pruning')
        ax2.set_xlabel('Depth')
        ax2.set_ylabel('Nodes Expanded')

        plt.tight_layout()
        plt.show()
        
    elif mode=='line':        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

        for key, grp in prune_off.groupby(['heuristic']):
            ax1.plot(grp['depth'], grp['nodes_expanded'], marker='o', label=key, linestyle='-', markerfacecolor='none')

        ax1.legend(loc='best')
        ax1.set_title('Nodes Expanded vs. Depth: No Pruning')
        ax1.set_xlabel('Depth')
        ax1.set_ylabel('Nodes Expanded')

        for key, grp in prune_on.groupby(['heuristic']):
            ax2.plot(grp['depth'], grp['nodes_expanded'], marker='o', label=key, linestyle='-', markerfacecolor='none')

        ax2.legend(loc='best')
        ax2.set_title('Nodes Expanded vs. Depth: With Pruning')
        ax2.set_xlabel('Depth')
        ax2.set_ylabel('Nodes Expanded')

        plt.tight_layout()
        plt.show()

    
if __name__ == '__main__':
    modes = ['line_err', 'scatter', 'line']
    for m in modes:
        plot_svd(mode=m)