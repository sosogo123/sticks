import networkx as nx
import matplotlib.pyplot as plt
import graphviz

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

# nx.drawing.nx_pydot.write_dot(graph, 'temp5.gv')

A =  nx.nx_agraph.to_agraph(graph)
print(A)
A.layout('dot')
A.draw('abcd.png')
# plt.show()
