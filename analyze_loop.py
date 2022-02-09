from http.client import REQUESTED_RANGE_NOT_SATISFIABLE
from pygraphviz import AGraph
from pygraphviz.agraph import Node
import graphviz
from visualize import Visualizer

viz = Visualizer()
# after you initialize the visualizer
viz.make_snapshots = True

def analyze_graph_loop(graph):
    # get origin node
    stack = []
    origin = graph.get_node('1111')
    analyze_node_loop(origin,graph,stack)
    return

def analyze_node_loop(state,graph,stack):
    print(f'analyze node loop: {state}')

    stack.append(state)

    out_edges = graph.out_edges(nbunch = state)
    in_edges = graph.in_edges(nbunch = state)
    for out_edge in out_edges:
        if out_edge.attr['condition'] != 'dead':
            analyze_path_loop(out_edge,graph,stack)

    stack.pop()

    return

def analyze_path_loop(path,graph,stack):
    out_node = path[1]
    if out_node in stack:
        loop_start = stack.index(out_node)
        
        print(stack[loop_start:])
    else: 
        analyze_node_loop(out_node,graph,stack)
    
            
    
    return
