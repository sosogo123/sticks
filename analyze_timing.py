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

def analyze_graph_timing(graph):
    graph_state_previous = {}
    graph_state_current =  get_graph_state(graph)
    counter = 0
    while graph_state_changed(graph_state_previous, graph_state_current):
        counter = (counter+1)
        print('counter', counter)
        
        # make a list of living nodes
        node_list = [node for node in graph.nodes() if node.attr['condition'] !='dead']
        print(f'living nodes: {len(node_list)}')
        for node in node_list:
            analyze_node_timing(node,graph)
            analyze_node_timing_dead(node, graph)

        # reset graph states
        graph_state_previous = graph_state_current
        graph_state_current = get_graph_state(graph)

    return

def get_graph_state(graph):
    win_list = [node for node in graph.nodes() if node.attr['condition'] == 'win']
    lose_list = [node for node in graph.nodes() if node.attr['condition'] == 'lose']
    loop_list = [node for node in graph.nodes() if node.attr['condition'] == 'loop']
    null_list = [node for node in graph.nodes() if node.attr['condition'] not in ['loop', 'lose', 'win']]
    graph_state_dict = {'loop': len(loop_list), 'lose': len(lose_list), 'win': len(win_list), 'null':len(null_list)}
    return graph_state_dict

def graph_state_changed(previous, current):
    if previous != current:
        return True
    else:
        return False

def analyze_node_timing(state,graph):
    # check for dead state
    analyze_node_dead(state, graph)

    # find edges
    edges = graph.out_edges(nbunch = state)

    for edge in edges:        
        if edge.attr['condition'] !='dead':
            analyze_path_timing(edge,graph)

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

        if state != '1111':
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

def analyze_node_timing_dead(state,graph):
    return
    if state.attr['condition'] == 'dead':
        return

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

        # find edges
        out_edges = graph.out_edges(nbunch = state)

        for out_edge in out_edges:        
            out_edge.attr['condition'] ='dead'
            viz.revert_path(out_edge)

        # viz.snapshot(graph)

    return

def analyze_path_timing(path,graph):
    in_node = path[0]
    out_node = path[1]

    if out_node.attr['condition'] not in ['loop', 'dead']:
        analyze_node_timing(out_node,graph)
        analyze_node_timing_dead(out_node, graph)

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