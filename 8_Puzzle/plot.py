import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv('./results.csv', keep_default_na=False, na_values=['NaN'], dtype={'correct': 'bool'})

""" Plot Percentage of Problems Solved """
# Calculate Percentage of Correct Solutions for Each m By Heuristic
correct = df.groupby(['m', 'heuristic'])['correct'].mean().reset_index()
correct = correct.pivot(index='m', columns='heuristic', values='correct')
correct = correct[['BF', 'MT', 'CB', 'NA']]
correct = correct.rename(columns={'BF': 'BF: Breadth-First', 'MT': 'MT: Misplaced Tiles', 'CB': 'CB: Manhattan Distance', 'NA': 'NA: Non-admissible'})

# Barplot of Percentage of Correct Solutions for Each m By Heuristic
fig, ax = plt.subplots(figsize=(12,6))
correct.plot.bar(ax=ax)
ax.set_title('Percentage of Correct Solutions for Each m By Heuristic')
ax.set_xlabel('m')
ax.set_ylabel('Percentage of Correct Solutions')
ax.set_ylim(0,1)
ax.grid()
plt.savefig('correct.png', dpi=300)

""" Plot Average CPU Time """
# Calculate Average CPU Time for Each m By Heuristic
cpu_time = df.groupby(['m', 'heuristic'])['cpu_time'].mean().reset_index()
cpu_time = cpu_time.pivot(index='m', columns='heuristic', values='cpu_time')
cpu_time = cpu_time[['BF', 'MT', 'CB', 'NA']]
cpu_time = cpu_time.rename(columns={'BF': 'BF: Breadth-First', 'MT': 'MT: Misplaced Tiles', 'CB': 'CB: Manhattan Distance', 'NA': 'NA: Non-admissible'})

# Barplot of Average CPU Time for Each m By Heuristic
fig, ax = plt.subplots(figsize=(12,6))
cpu_time.plot.bar(ax=ax)
ax.set_title('Average CPU Time for Each m By Heuristic')
ax.set_xlabel('m')
ax.set_ylabel('Average CPU Time (seconds)')
ax.grid()
plt.savefig('cpu_time.png', dpi=300)

""" Plot Average Search Nodes Generated """
# Calculate Average Search Nodes Generated for Each m By Heuristic
search_nodes_generated = df.groupby(['m', 'heuristic'])['search_nodes_generated'].mean().reset_index()
search_nodes_generated = search_nodes_generated.pivot(index='m', columns='heuristic', values='search_nodes_generated')
search_nodes_generated = search_nodes_generated[['BF', 'MT', 'CB', 'NA']]
search_nodes_generated = search_nodes_generated.rename(columns={'BF': 'BF: Breadth-First', 'MT': 'MT: Misplaced Tiles', 'CB': 'CB: Manhattan Distance', 'NA': 'NA: Non-admissible'})

# Barplot of Average Search Nodes Generated for Each m By Heuristic
fig, ax = plt.subplots(figsize=(12,6))
search_nodes_generated.plot.bar(ax=ax)
ax.set_title('Average Search Nodes Generated for Each m By Heuristic')
ax.set_xlabel('m')
ax.set_ylabel('Average Search Nodes Generated')
ax.grid()
plt.savefig('search_nodes_generated.png', dpi=300)

""" Plot Average Solution Length """
# Calculate Average Solution Length for Each m By Heuristic
solution_length = df[df['solution_length'] != 0].groupby(['m', 'heuristic'])['solution_length'].mean().reset_index()
solution_length = solution_length.pivot(index='m', columns='heuristic', values='solution_length')
solution_length = solution_length[['BF', 'MT', 'CB', 'NA']]
solution_length = solution_length.rename(columns={'BF': 'BF: Breadth-First', 'MT': 'MT: Misplaced Tiles', 'CB': 'CB: Manhattan Distance', 'NA': 'NA: Non-admissible'})



# Barplot of Average Solution Length for Each m By Heuristic
fig, ax = plt.subplots(figsize=(12,6))
solution_length.plot.bar(ax=ax)
ax.set_title('Average Solution Length for Each m By Heuristic')
ax.set_xlabel('m')
ax.set_ylabel('Average Solution Length')
ax.grid()
plt.savefig('solution_length.png', dpi=300)