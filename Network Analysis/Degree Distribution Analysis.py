import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# Load data
edges = pd.read_csv('youtube_edges.csv')
nodes = pd.read_csv('youtube_nodes.csv')

# Extract only the Source and Target columns
edges = edges[['Source', 'Target']]

# Create graph
G = nx.Graph()
G.add_edges_from(edges.values)

# Degree distribution
degrees = [deg for node, deg in G.degree()]
plt.hist(degrees, bins=range(min(degrees), max(degrees) + 1), edgecolor='black', linewidth=1.2)
plt.title('Degree Distribution')
plt.xlabel('Degree')
plt.ylabel('Frequency')
plt.show()
