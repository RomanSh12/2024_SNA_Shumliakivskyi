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

# Connected components
components = list(nx.connected_components(G))
component_sizes = [len(c) for c in components]
print(f"Number of connected components: {len(components)}")
print(f"Sizes of connected components: {component_sizes}")

# Plot component size distribution
plt.hist(component_sizes, bins=range(1, max(component_sizes) + 1), edgecolor='black', linewidth=1.2)
plt.title('Connected Component Size Distribution')
plt.xlabel('Component Size')
plt.ylabel('Frequency')
plt.show()
