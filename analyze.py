from http.client import REQUESTED_RANGE_NOT_SATISFIABLE
from pygraphviz import AGraph
from pygraphviz.agraph import Node
import graphviz
from visualize import Visualizer
from analyze_dead import analyze_graph_dead
from analyze_loop import analyze_graph_loop

viz = Visualizer()
# after you initialize the visualizer
viz.make_snapshots = True

def analyze_graph(graph):
    # get origin node
    origin = graph.get_node('1111')
    analyze_node(origin,graph)
    return

def analyze_node(state,graph):
    state.attr['found'] = 'true'
    
    # DEBUG
    if state.attr['condition'] in ('win', 'lose'):
        print('node already set')

    viz.highlight_state(state)
    print(f'node: {state}')

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
                    
        if edge.attr['condition'] == 'lose':
            if len(edges)==1:
                state.attr['condition'] = 'lose'
                viz.highlight_state(state,color='red')

    # check all paths
    if len(edges)>0:
        all_losers = True
        for edge in edges:
            if edge.attr['condition'] != 'lose':
                all_losers = False
                break

        if all_losers:
            state.attr['condition'] = 'lose'
            viz.highlight_state(state,color='red')


      # analyze path for each edge
    return

def analyze_path(path,graph):
    path.attr['found'] = 'true'
    viz.highlight_path(path)

    out_node = path[1]

    if out_node.attr['found'] != 'true':
        analyze_node(out_node,graph)

        print(f'path out: {out_node}')
    if out_node.attr['type'] == 'end':
        path.attr['condition'] = 'win'
        viz.highlight_path(path,color= 'green')
    if out_node.attr['condition'] == 'win':
        path.attr['condition'] = 'lose'
        viz.highlight_path(path,color= 'red')
    if out_node.attr['condition'] == 'lose':
        path.attr['condition'] = 'win'
        viz.highlight_path(path,color= 'green')

    
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
    analyze_graph_dead(graph)
    analyze_graph_loop(graph)
    viz.snapshot(graph)
    return None

if __name__ == '__main__':
    main()
