import networkx as nx
import matplotlib.pyplot as plt

# ER Model Parameters
N_ER = 11348
E_ER = 11314
p_ER = (2 * E_ER) / (N_ER * (N_ER - 1))

# Generate Erdős-Rényi graph
ER_graph = nx.fast_gnp_random_graph(N_ER, p_ER)

# Compute metrics for ER model
avg_degree_ER = sum(dict(ER_graph.degree()).values()) / N_ER
density_ER = nx.density(ER_graph)
avg_clustering_ER = nx.average_clustering(ER_graph)
triangles_ER = sum(nx.triangles(ER_graph).values()) // 3
connected_components_ER = nx.number_connected_components(ER_graph)

print("Erdős-Rényi Model")
print(f"Average degree: {avg_degree_ER}")
print(f"Density: {density_ER}")
print(f"Average clustering coefficient: {avg_clustering_ER}")
print(f"Number of triangles: {triangles_ER}")
print(f"Number of connected components: {connected_components_ER}")

plt.figure(figsize=(12, 10))  # Increase figure size for more space
pos_ER = nx.fruchterman_reingold_layout(ER_graph)  # Faster layout
nx.draw(ER_graph, pos_ER, with_labels=False, node_size=10)

plt.title("Erdős-Rényi Graph (Enhanced Visualization)")
plt.show()

# Draw the ER graph
#plt.figure(figsize=(10, 8))
#pos_ER = nx.spring_layout(ER_graph)
#nx.draw(ER_graph, pos_ER, with_labels=False, node_size=10)
#plt.title("Erdős-Rényi Graph")
#plt.show()
