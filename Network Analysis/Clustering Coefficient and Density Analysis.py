import networkx as nx
import pandas as pd

# Load data
edges = pd.read_csv('youtube_edges.csv')
nodes = pd.read_csv('youtube_nodes.csv')

# Extract only the Source and Target columns
edges = edges[['Source', 'Target']]

# Create graph
G = nx.Graph()
G.add_edges_from(edges.values)

# Clustering coefficient
avg_clustering = nx.average_clustering(G)
print(f"Average clustering coefficient: {avg_clustering}")

# Density
density = nx.density(G)
print(f"Density of the network: {density}")
