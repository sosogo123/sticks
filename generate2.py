"""Generate graph functions.
"""
from pygraphviz import AGraph
from pygraphviz.agraph import Node

from visualize import Visualizer

# initialize visualizer
viz = Visualizer()

def generate_graph(version=0):
    graph = AGraph(directed=True)
    graph.layout(prog='dot')

    # set graph attributes
    graph.graph_attr['layout'] = 'dot'
    graph.graph_attr['rankdir'] = 'LR'
    graph.graph_attr['fontname'] = 'Courier New'
    # graph.graph_attr['size'] = '7.5,10'
    # graph.graph_attr['ratio'] = 'fill'

    # set node attributes
    graph.node_attr['shape'] = 'circle'
    graph.node_attr['fontname'] = 'Courier New'

    # set edge attributes
    graph.edge_attr['arrowsize'] = '1.0'
    graph.edge_attr['fontname'] = 'Courier New'

    # set origin
    graph.add_node('1111', label=r'11\n11', shape='doublecircle')
    origin = graph.get_node('1111')

    generate_paths(graph, origin, version)

    return graph

def generate_paths(graph: AGraph, in_state: Node, version: int):
    end_state = False

    viz.highlight_state(in_state)

    # create position tuple from state string
    o_high, o_low, p_high, p_low = (
        int(in_state[0]), int(in_state[1]), int(in_state[2]), int(in_state[3])
    )
    pos_tuple = (o_high, o_low, p_high, p_low)

    # check for end state
    if p_high == p_low == 0:
        end_state = True
        in_state.attr['shape'] = 'doublecircle'
        viz.snapshot(graph)
        viz.revert_state(in_state)
        return None

    # apply actions
    action_list = ['HH', 'HL', 'LH', 'LL', 'SU1', 'SD1']
    for action in action_list:
        generate_path(graph, in_state, pos_tuple, version, action)

    viz.revert_state(in_state)

    return None

def generate_path(graph: AGraph, in_state: Node, pos_tuple: tuple, version: int, action: str):
    """Generate a single path for the specified state and action.

    Args:
        pos_tuple: Position tuple, defines o_high, o_low, p_high, p_low
    """
    # apply action
    out_pos_tuple = apply_action(pos_tuple, version, action)

    # stop, if invalid action
    if not out_pos_tuple:
        return None

    # get out state
    out_state = get_out_state(graph, out_pos_tuple)
    out_state_loop = True if out_state.attr.get('loop') == 'True' else False

    # create path
    path = create_path(graph, in_state, out_state, action)

    # continue
    if not out_state_loop:
        generate_paths(graph, out_state, version)

    if path:
        viz.revert_path(path)

def get_out_state(graph: AGraph, pos_tuple: tuple) -> Node:
    # unpack position tuple
    o_high, o_low, p_high, p_low = pos_tuple

    # repack out-state
    out_state_str = f'{p_high}{p_low}{o_high}{o_low}'
    out_state_label = fr'{p_high}{p_low}\n{o_high}{o_low}'

    # create node
    if out_state_str in graph.nodes():
        out_state = graph.get_node(out_state_str)
        out_state.attr['loop'] = True
    else:
        graph.add_node(out_state_str, label=out_state_label)
        out_state = graph.get_node(out_state_str)

    return out_state

def create_path(graph: AGraph, in_state: Node, out_state: Node, action: str):
    path = None

    if not graph.has_edge(in_state, out_state):
        graph.add_edge(in_state, out_state, label=action)
        path = graph.get_edge(in_state, out_state)
        viz.highlight_path(path)
        viz.snapshot(graph)

    return path

def apply_action(pos_tuple: tuple, version: int, action: str):
    # unpack position tuple
    o_high, o_low, p_high, p_low = pos_tuple

    # applies action
    if action == 'HH':
        if not (p_high > 0 and o_high > 0):
            return None

        o_high += p_high
        if o_high >= version:
            o_high = 0

    elif action == 'HL':
        if not (p_high > 0 and o_low > 0):
            return None

        o_low += p_high
        if o_low >= version:
            o_low = 0

    elif action == 'LH':
        if not (p_low > 0 and o_high > 0):
            return None

        o_high += p_low
        if o_high >= version:
            o_high = 0

    elif action == 'LL':
        if not (p_low > 0 and o_low > 0):
            return None

        o_low += p_low
        if o_low >= version:
            o_low = 0

    elif action == 'SU1':
        p_tuple = shift_up(1, p_high, p_low, version)
        if not p_tuple:
            return None

        p_high, p_low = p_tuple

    elif action == 'SD1':
        p_tuple = shift_down(1, p_high, p_low, version)
        if not p_tuple:
            return None

        p_high, p_low = p_tuple

    # re-order opponent's highs, lows
    if o_high < o_low:
        o_high, o_low = o_low, o_high

    # return new tuple
    return (o_high, o_low, p_high, p_low)

def shift_up(degree, p_high, p_low, version):
    """
    constraints:
    - degree:
    - p_high:
        p_high + degree < version
    - p_low:
        p_low >= degree
        p_low <= p_high
    """
    if p_high + degree >= version:
        return None
    if p_low < degree:
        return None
    if p_low > p_high:
        return None

    p_high += degree
    p_low -= degree

    return p_high, p_low

def shift_down(degree, p_high, p_low, version):
    """
    constraints:
    - degree: degree <= (version - 1) / 2
    - p_high:
        p_high > p_low
        p_high >= degree
    - p_low:
        p_low + degree < version
    """
    if degree > (version - 1) / 2:
        return None
    if p_high <= p_low:
        return None
    if p_high < degree:
        return None
    if p_low + degree >= version:
        return None
    if p_low + degree == p_high:
        return None

    p_high -= degree
    p_low += degree

    return p_high, p_low

def main():
    version = 3
    viz.file_prefix = f'version{version}'

    graph = generate_graph(version=version)
    # graph = generate()
    viz.write_dot(graph)

    viz.snapshot(graph, force=True)

    return None

if __name__ == '__main__':
    main()
