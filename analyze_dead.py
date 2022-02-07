from http.client import REQUESTED_RANGE_NOT_SATISFIABLE
from pygraphviz import AGraph
from pygraphviz.agraph import Node
import graphviz
from visualize import Visualizer

viz = Visualizer()
# after you initialize the visualizer
viz.make_snapshots = True

def analyze_graph_dead(graph):
    # explicitly mark un-found edges as dead
    edges = graph.edges()
    for edge in edges:
        if edge.attr['found'] is None or edge.attr['found'] == '':
            edge.attr['condition'] = 'dead'

    # get origin node
    origin = graph.get_node('1111')
    analyze_node_dead(origin,graph)
    return

def analyze_node_dead(state,graph):
    print(f'analyze node dead: {state}')
    state.attr['dead_found'] = 'true'
    out_edges = graph.out_edges(nbunch = state)
    in_edges = graph.in_edges(nbunch = state)

    if state != '1111':
        all_dead = True
        for in_edge in in_edges:
            if (
                in_edge.attr['condition'] != 'lose' and
                in_edge.attr['condition'] != 'dead' and
                in_edge.attr['found'] is not None
            ) :
                all_dead = False
                break

        if all_dead:
            state.attr['condition'] = 'dead'
            viz.revert_state(state)

    for out_edge in out_edges:        
        if out_edge.attr['condition'] !='dead':
            analyze_path_dead(out_edge,graph)

      # analyze path for each edge
    return

def analyze_path_dead(path,graph):
    out_node = path[1]
    in_node = path[0]

    if in_node.attr['condition'] == 'dead':
        path.attr['condition'] = 'dead'
        viz.revert_path(path)

    if out_node.attr['condition'] != 'dead':
        if out_node.attr['dead_found'] != 'true' or out_node.attr['type'] == 'end':
            analyze_node_dead(out_node,graph)

            print(f'path out: {out_node}')
            
    

    return
