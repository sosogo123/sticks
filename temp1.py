import networkx as nx
import matplotlib.pyplot as plt

graph = nx.DiGraph()
graph.add_edges_from(
    [
        ('A', 'B'),
        ('A', 'C'),
        ('C', 'B')
    ]
)
pos = nx.spring_layout(graph)
nx.draw_networkx_nodes(graph, pos, node_size=500)
nx.draw_networkx_edges(graph, pos, edgelist=graph.edges(), edge_color='black')
nx.draw_networkx_labels(graph, pos)

plt.show()