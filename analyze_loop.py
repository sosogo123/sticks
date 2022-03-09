from http.client import REQUESTED_RANGE_NOT_SATISFIABLE
from pygraphviz import AGraph
from pygraphviz.agraph import Node
import graphviz
from visualize import Visualizer

viz = Visualizer()
# after you initialize the visualizer
viz.make_snapshots = True

loop_list = []

def analyze_graph_loop(graph):
    # get origin node
    stack = []
    origin = graph.get_node('1111')
    analyze_node_loop(origin,graph,stack,loop_stack=[])

    return list(loop_list)

def analyze_node_loop(state,graph,stack, loop_stack):
    print(f'analyze node loop: {state}')

    stack.append(state)
    if loop_stack:
        loop_stack.append(state)

    out_edges = graph.out_edges(nbunch = state)
    for out_edge in out_edges:
        if out_edge.attr['condition'] != 'dead':
                # don't just save last loop, create loop stack
            analyze_path_loop(out_edge,graph,stack, loop_stack)

        if not loop_stack:
            if state.attr['condition'] == 'loop':
                loop_stack.append(state)
        
    stack.pop()
    if loop_stack:
        loop_stack.pop()

    return

def analyze_path_loop(path,graph,stack, loop_stack):
    out_node = path[1]

    # # check if out node is already in loop
    # for loop_check in loop_list:
    #     if out_node in loop_check:
    #         print(f'{out_node} already in loop')

    if out_node.attr['condition'] == 'loop':
        if loop_stack:
            # pass loop stack into process_loop
            process_loop(loop_stack, graph)
            path.attr['condition'] = 'loop'
            viz.highlight_path(path, color = 'orange')


    if out_node in stack:
        loop_start = stack.index(out_node)
        loop = stack[loop_start:]
        process_loop(loop,graph)
        print(stack[loop_start:])

    else: 
        analyze_node_loop(out_node,graph,stack, loop_stack)

    return

def process_loop(loop,graph):
    """
    check existing loops in the list and pop/merge
    """
    new_loop = []

    for node in loop:
        for index, loop_check in enumerate(loop_list):
            if node in loop_check:
                new_loop.extend(loop_list.pop(index))
                break
        if node not in new_loop:
            new_loop.append(node)

    if new_loop:
        loop_list.append(new_loop)

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
            if graph.has_edge(loop[index], loop[0]):
                loop_edge = graph.get_edge(loop[index], loop[0])
            else:
                loop_edge = None
        if loop_edge:
            loop_edge.attr['condition'] = 'loop'
            viz.highlight_path(loop_edge, color = 'orange')
            print(loop_edge)
       
    return