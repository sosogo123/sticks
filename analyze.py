from http.client import REQUESTED_RANGE_NOT_SATISFIABLE
from pygraphviz import AGraph
from pygraphviz.agraph import Node
import graphviz
from visualize import Visualizer

viz = Visualizer()
# after you initialize the visualizer
viz.make_snapshots = True

def analyze_graph(graph):
    # get origin node
    origin = graph.get_node('1111')
    analyze_node(origin,graph)
    return

def analyze_node(state,graph):
    viz.highlight_state(state)
    print(state)
    # find edges
    state.attr['found'] = 'true'
    edges = graph.out_edges(nbunch = state)

    for edge in edges:
        
        analyze_path(edge,graph)
    #print(edges)



      # analyze path for each edge
    return

def analyze_path(path,graph):

    viz.highlight_path(path)
    out_node = path[1]

    if out_node.attr['found'] != 'true':
        analyze_node(out_node,graph)
        print(out_node)
    # else:
    #     print('found loop')

    # this will find the next node
    # then, you call analyze node

    return

def main():
    graph = AGraph()
    graph.layout(prog='dot')
    graph.read(path='viz/version3.dot')
    graph.draw('viz/version3.png')
    # graphviz.view('viz/version3.png')
    analyze_graph(graph)
    viz.snapshot(graph)
    return None

if __name__ == '__main__':
    main()
