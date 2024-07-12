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

# Path analysis
if nx.is_connected(G):
    diameter = nx.diameter(G)
    avg_path_length = nx.average_shortest_path_length(G)
else:
    largest_cc = max(nx.connected_components(G), key=len)
    subgraph = G.subgraph(largest_cc)
    diameter = nx.diameter(subgraph)
    avg_path_length = nx.average_shortest_path_length(subgraph)

print(f"Diameter of the network: {diameter}")
print(f"Average path length: {avg_path_length}")
