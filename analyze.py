from http.client import REQUESTED_RANGE_NOT_SATISFIABLE
from pygraphviz import AGraph
from pygraphviz.agraph import Node
import graphviz
from visualize import Visualizer
from analyze_loop import analyze_graph_loop
from analyze_timing import analyze_graph_timing

viz = Visualizer()
# after you initialize the visualizer
viz.make_snapshots = True

def analyze_graph(graph):
    # get origin node
    origin = graph.get_node('1111')
    analyze_node(origin,graph)
    return

def analyze_node(state,graph):
    # print(f'node: {state}')

    state.attr['found'] = 'true'    
    viz.highlight_state(state)

    # find edges
    edges = graph.out_edges(nbunch = state)

    if len(edges)==0:
        state.attr['type'] = 'end'
        viz.highlight_state(state,color='magenta')

    for edge in edges:        
        if edge.attr['condition'] !='dead':
            analyze_path(edge,graph)
    #print(edges)
        if edge.attr['condition'] == 'win':
            state.attr['condition'] = 'win'
            viz.highlight_state(state,color='green')

            # checks for paths not taken ('dead')
            for edgecheck in edges:
                if edgecheck.attr['condition'] != 'win':
                    edgecheck.attr['condition'] = 'dead'
                    viz.revert_path(edgecheck)

                    # analyze corresponding node
                    analyze_node_dead(edgecheck[1], graph)
                                        
        if edge.attr['condition'] == 'lose':
            all_losers = True
            for edge in edges:
                if edge.attr['condition'] not in ['lose', 'dead']:
                    all_losers = False
                    break

            if all_losers:
                state.attr['condition'] = 'lose'
                viz.highlight_state(state,color='red')

        if edge.attr['condition'] == 'dead':
            all_dead = True
            for edge in edges:
                if edge.attr['condition'] not in ['dead']:
                    all_dead = False
                    break

            if all_dead:
                state.attr['condition'] = 'dead'
                viz.revert_state(state)

    return

def analyze_node_dead(state, graph):
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

def analyze_path(path, graph):
    path.attr['found'] = 'true'
    viz.highlight_path(path)

    out_node = path[1]

    if out_node.attr['found'] != 'true':
        analyze_node(out_node,graph)

        # print(f'path out: {out_node}')
    if out_node.attr['type'] == 'end':
        path.attr['condition'] = 'win'
        viz.highlight_path(path,color= 'green')
    if out_node.attr['condition'] == 'win':
        path.attr['condition'] = 'lose'
        viz.highlight_path(path,color= 'red')
    if out_node.attr['condition'] == 'lose':
        path.attr['condition'] = 'win'
        viz.highlight_path(path,color= 'green')

    return

def main():
    version = 5
    graph = AGraph()
    graph.layout(prog='dot')
    graph.read(path=f'viz/version{version}.dot')
    # graph.draw(f'viz/version{version}.png')
    # graphviz.view(f'viz/version{version}.png')
    analyze_graph(graph)
    loop_list = analyze_graph_loop(graph)
    analyze_graph_timing(graph,loop_list)

    viz.snapshot(graph)
    return None

if __name__ == '__main__':
    main()
