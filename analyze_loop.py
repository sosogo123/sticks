from http.client import REQUESTED_RANGE_NOT_SATISFIABLE
from pygraphviz import AGraph
from pygraphviz.agraph import Node
import graphviz
from visualize import Visualizer

viz = Visualizer()
# after you initialize the visualizer
viz.make_snapshots = True

loop_list = set()

def analyze_graph_loop(graph):
    # get origin node
    stack = []
    origin = graph.get_node('1111')
    analyze_node_loop(origin,graph,stack)

    return list(loop_list)

def analyze_node_loop(state,graph,stack):
    print(f'analyze node loop: {state}')

    stack.append(state)

    out_edges = graph.out_edges(nbunch = state)
    for out_edge in out_edges:
        if out_edge.attr['condition'] != 'dead':
            analyze_path_loop(out_edge,graph,stack)

    stack.pop()

    return

def analyze_path_loop(path,graph,stack):
    out_node = path[1]
    if out_node in stack:
        loop_start = stack.index(out_node)
        loop = stack[loop_start:]
        loop_list.add(tuple(loop))
        process_loop(loop,graph)
        print(stack[loop_start:])


    else: 
        analyze_node_loop(out_node,graph,stack)
    
            
    
    return

def process_loop(loop,graph):
    # mark nodes with loop
    for loop_node in loop:
        loop_node.attr['condition'] = 'loop'
        viz.highlight_state(loop_node, color='orange')
    # mark edges woth loop
    
    for index in range(len(loop)):
        loop_node = loop[index]
        print(loop_node)
        try:
            loop_edge = graph.get_edge(loop[index], loop[index + 1])
        except IndexError:
            loop_edge = graph.get_edge(loop[index], loop[0])
        loop_edge.attr['condition'] = 'loop'
        viz.highlight_path(loop_edge, color = 'orange')
        print(loop_edge)
       
    return