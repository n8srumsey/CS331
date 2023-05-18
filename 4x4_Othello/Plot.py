from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

def plot_svd(mode='line_err'):
    # Load data
    df = pd.read_csv('svd_results.csv')
    
    # Split data into pruning on and off
    prune_off = df[df['prune'] == 0]
    prune_on = df[df['prune'] == 1]
    
    # Plot Type: Line Plot with Error Bars (95% Confidence Interval)
    if mode == 'line_err':
        # Create figure and axes
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

        # Calculate the maximum jitter amount based on the number of unique depths
        max_jitter = 0.05 * len(prune_off['depth'].unique())

        # Plot the data
        for i, (key, grp) in enumerate(prune_off.groupby(['heuristic'])):
            # Calculate the mean and standard deviation of the nodes expanded for each depth
            means = grp.groupby('depth')['nodes_expanded'].mean()
            stds = grp.groupby('depth')['nodes_expanded'].std()
            
            # Add horizontal jitter to the x-values of the error bars
            x_jitter = np.random.uniform(-max_jitter, max_jitter, len(means.index))
            x_values = means.index + x_jitter
            
            # Plot the error bars (95% confidence interval)
            ax1.errorbar(x_values, means, yerr=stds, label=key, marker='o', linestyle='-', capsize=4)

        # Add legend, title, and axis labels
        ax1.legend(loc='best', title='Heuristic')
        ax1.set_title('Nodes Expanded vs. Depth: No Pruning')
        ax1.set_xlabel('Depth')
        ax1.set_ylabel('Nodes Expanded')

        # Repeat for pruning on
        for i, (key, grp) in enumerate(prune_on.groupby(['heuristic'])):
            # Calculate the mean and standard deviation of the nodes expanded for each depth
            means = grp.groupby('depth')['nodes_expanded'].mean()
            stds = grp.groupby('depth')['nodes_expanded'].std()
            
            # Add horizontal jitter to the x-values of the error bars
            x_jitter = np.random.uniform(-max_jitter, max_jitter, len(means.index))
            x_values = means.index + x_jitter
            
            # Plot the error bars (95% confidence interval)
            ax2.errorbar(x_values, means, yerr=stds, label=key, marker='o', linestyle='-', capsize=4)

        # Add legend, title, and axis labels
        ax2.legend(loc='best', title='Heuristic')
        ax2.set_title('Nodes Expanded vs. Depth: With Pruning')
        ax2.set_xlabel('Depth')
        ax2.set_ylabel('Nodes Expanded')

        # Adjust spacing between subplots and display the plot
        plt.tight_layout()
        plt.show()
    
    # Plot Type: Scatter Plot
    elif mode=='scatter':
        # Create figure and axes
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

        # Create a color map for the heuristics
        colors = plt.cm.tab10(np.linspace(0, 1, len(prune_off['heuristic'].unique())))

        # Plot the data
        for i, (key, grp) in enumerate(prune_off.groupby(['heuristic'])):
            grp.plot(ax=ax1, kind='scatter', x='depth', y='nodes_expanded', label=key, color=colors[i])

        # Add legend, title, and axis labels
        ax1.legend(loc='best')
        ax1.set_title('Nodes Expanded vs. Depth: No Pruning')
        ax1.set_xlabel('Depth')
        ax1.set_ylabel('Nodes Expanded')

        # Repeat for pruning on
        for i, (key, grp) in enumerate(prune_on.groupby(['heuristic'])):
            grp.plot(ax=ax2, kind='scatter', x='depth', y='nodes_expanded', label=key, color=colors[i])

        # Add legend, title, and axis labels
        ax2.legend(loc='best')
        ax2.set_title('Nodes Expanded vs. Depth: With Pruning')
        ax2.set_xlabel('Depth')
        ax2.set_ylabel('Nodes Expanded')

        # Adjust spacing between subplots and display the plot
        plt.tight_layout()
        plt.show()
        
    # Plot Type: Line Plot
    elif mode=='line':        
        # Create figure and axes
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

        # Plot the data
        for key, grp in prune_off.groupby(['heuristic']):
            ax1.plot(grp['depth'], grp['nodes_expanded'], marker='o', label=key, linestyle='-', markerfacecolor='none')

        # Add legend, title, and axis labels
        ax1.legend(loc='best')
        ax1.set_title('Nodes Expanded vs. Depth: No Pruning')
        ax1.set_xlabel('Depth')
        ax1.set_ylabel('Nodes Expanded')

        # Repeat for pruning on
        for key, grp in prune_on.groupby(['heuristic']):
            ax2.plot(grp['depth'], grp['nodes_expanded'], marker='o', label=key, linestyle='-', markerfacecolor='none')

        # Add legend, title, and axis labels
        ax2.legend(loc='best')
        ax2.set_title('Nodes Expanded vs. Depth: With Pruning')
        ax2.set_xlabel('Depth')
        ax2.set_ylabel('Nodes Expanded')

        # Adjust spacing between subplots and display the plot
        plt.tight_layout()
        plt.show()

    
if __name__ == '__main__':
    # Plotting modes: 'scatter', 'line', 'line_err'
    modes = ['line_err'] # 'scatter', 'line']
    
    # Plot the data
    for m in modes:
        plot_svd(mode=m)