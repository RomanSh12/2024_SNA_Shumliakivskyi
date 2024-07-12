import networkx as nx
import matplotlib.pyplot as plt

# BA Model Parameters
N_BA = 11348
E_BA = 11314
m_BA = max(1, int(E_BA / N_BA))

# Generate Barabási-Albert graph
BA_graph = nx.barabasi_albert_graph(N_BA, m_BA)

# Compute metrics for BA model
avg_degree_BA = sum(dict(BA_graph.degree()).values()) / N_BA
density_BA = nx.density(BA_graph)
avg_clustering_BA = nx.average_clustering(BA_graph)
triangles_BA = sum(nx.triangles(BA_graph).values()) // 3
connected_components_BA = nx.number_connected_components(BA_graph)

print("\nBarabási-Albert Model")
print(f"Average degree: {avg_degree_BA}")
print(f"Density: {density_BA}")
print(f"Average clustering coefficient: {avg_clustering_BA}")
print(f"Number of triangles: {triangles_BA}")
print(f"Number of connected components: {connected_components_BA}")

# Draw the BA graph
plt.figure(figsize=(10, 8))
pos_BA = nx.spring_layout(BA_graph)
nx.draw(BA_graph, pos_BA, with_labels=False, node_size=10)
plt.title("Barabási-Albert Graph")
plt.show()
