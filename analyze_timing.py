from http.client import REQUESTED_RANGE_NOT_SATISFIABLE
from shutil import register_unpack_format
from numpy import true_divide
from pygraphviz import AGraph
from pygraphviz.agraph import Node
from visualize import Visualizer
from analyze_dead import analyze_node_dead

viz = Visualizer()
# after you initialize the visualizer
viz.make_snapshots = True

def analyze_graph_timing(graph,loop_list):
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
            analyze_node_timing(node,graph, loop_list)

        for loop in loop_list:
            analyze_loop_timing(loop,graph)

        # reset graph states
        graph_state_previous = graph_state_current
        graph_state_current = get_graph_state(graph)

    return

def analyze_loop_timing(loop, graph):
    """
    If the loop is dead, it could be removed from the loop list.
    """
    in_edges = graph.in_edges(nbunch = loop)
    out_edges = graph.out_edges(nbunch = loop)
    all_dead = True
    for edge in in_edges:
        if edge.attr['condition'] not in ['loop', 'dead']:
            all_dead = False
            break

    if all_dead:
        for node in loop:
            node.attr['condition'] = 'dead'
            viz.revert_state(node)
        for edge in in_edges:
            edge.attr['condition'] = 'dead'
            viz.revert_path(edge)
        for edge in out_edges:
            edge.attr['condition'] = 'dead'
            viz.revert_path(edge)

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

def analyze_node_timing(state,graph, loop_list):
    # check for dead state
    analyze_node_dead(state, graph)

    # find edges
    edges = graph.out_edges(nbunch = state)

    for edge in edges:        
        if edge.attr['condition'] !='dead':
            analyze_path_timing(edge,graph, loop_list)

        if edge.attr['condition'] == 'win':
            apply_state_condition(state, 'win', loop_list)

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
                apply_state_condition(state, 'lose', loop_list)

        if state != '1111':
            if edge.attr['condition'] == 'dead':
                all_dead = True
                for edge in edges:
                    if edge.attr['condition'] not in ['dead']:
                        all_dead = False
                        break

                if all_dead:
                    apply_state_condition(state, 'dead', loop_list)

    return

def apply_state_condition(state, condition, loop_list):
    # set condition attribute
    state.attr['condition'] = condition

    # update the viz
    if condition == 'win':
        viz.highlight_state(state,color='green')
    elif condition == 'lose':
        viz.highlight_state(state,color='red')
    elif condition == 'dead':
        viz.revert_state(state)

    # check against loop list
    for loop in loop_list:
        if state in loop:
            index = loop.index(state)
            loop.pop(index)
            break

def analyze_path_timing(path,graph, loop_list):
    in_node = path[0]
    out_node = path[1]

    if out_node.attr['condition'] not in ['loop', 'dead']:
        analyze_node_timing(out_node,graph,loop_list)

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