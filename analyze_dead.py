from http.client import REQUESTED_RANGE_NOT_SATISFIABLE
from pygraphviz import AGraph
from pygraphviz.agraph import Node
from visualize import Visualizer

viz = Visualizer()
# after you initialize the visualizer
viz.make_snapshots = True

def analyze_node_dead(state, graph):
    if state == '1111':
        return

    state.attr['dead_found'] = 'true'
    # find edges
    in_edges = graph.in_edges(nbunch = state)

    all_dead = True
    for in_edge in in_edges:
        if in_edge.attr['condition'] != 'dead':
            all_dead = False
            break

    if all_dead:
        # viz.snapshot(graph)
        state.attr['condition'] = 'dead'
        viz.revert_state(state)

        out_edges = graph.out_edges(nbunch = state)
        for out_edge in out_edges:        
            if out_edge.attr['condition'] !='dead':
                out_edge.attr['condition'] = 'dead'
                viz.revert_path(out_edge)

