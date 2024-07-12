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

# Degree centrality
degree_centrality = nx.degree_centrality(G)
print("Top 5 nodes by degree centrality:")
print(sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5])

# Closeness centrality
closeness_centrality = nx.closeness_centrality(G)
print("Top 5 nodes by closeness centrality:")
print(sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)[:5])

# Betweenness centrality
betweenness_centrality = nx.betweenness_centrality(G)
print("Top 5 nodes by betweenness centrality:")
print(sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:5])
