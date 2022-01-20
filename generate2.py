import os
import time

from pygraphviz import AGraph
from pygraphviz.agraph import Node, Edge
import graphviz

file_prefix = 'snap'
seq = 0
path_viz = 'viz'
make_snapshots = False

def generate_graph(version=0):
    graph = AGraph(directed=True)
    graph.layout(prog='dot')

    # set graph attributes
    graph.graph_attr['layout'] = 'dot'
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

def generate_paths(graph: AGraph, in_state: Node, version):
    end_state = False

    highlight_state(in_state)

    # unpacks in-state
    o_high, o_low, p_high, p_low = (
        int(in_state[0]), int(in_state[1]), int(in_state[2]), int(in_state[3])
    )

    # check for end state
    if p_high == p_low == 0:
        end_state = True
        graph.get_node(in_state).attr['shape'] = 'doublecircle'
        snapshot(graph)
        revert_state(in_state)
        return

    # apply actions
    generate_path_hh(graph, in_state, o_high, o_low, p_high, p_low, version)
    generate_path_hl(graph, in_state, o_high, o_low, p_high, p_low, version)
    generate_path_lh(graph, in_state, o_high, o_low, p_high, p_low, version)
    generate_path_ll(graph, in_state, o_high, o_low, p_high, p_low, version)
    # generate_path_su1(graph, in_state, o_high, o_low, p_high, p_low, version)
    # generate_path_sd1(graph, in_state, o_high, o_low, p_high, p_low, version)

    revert_state(in_state)

    return

def generate_path_hh(graph: AGraph, in_state, o_high, o_low, p_high, p_low, version):
    out_state_exists = False

    # applies action
    if p_high > 0 and o_high > 0:
        o_high += p_high
        if o_high >= version:
            o_high = 0

        # re-order highs, lows
        o_high, o_low = reorder(o_high, o_low)
    
        # repack out-state
        out_state_str = f'{p_high}{p_low}{o_high}{o_low}'
        out_state_label = fr'{p_high}{p_low}\n{o_high}{o_low}'

        # create node
        out_state = None
        if out_state_str in graph.nodes():
            out_state = graph.get_node(out_state_str)
            out_state_exists = True
        else:
            graph.add_node(out_state_str, label=out_state_label)
            out_state = graph.get_node(out_state_str)

        # create edge
        graph.add_edge(in_state, out_state, label='HH')
        path = graph.get_edge(in_state, out_state)
        highlight_path(path)
        snapshot(graph)

        if not out_state_exists:
            generate_paths(graph, out_state, version)

        revert_path(path)

    return None

def generate_path_hl(graph: AGraph, in_state, o_high, o_low, p_high, p_low, version):
    out_state_exists = False
    path = None

    # applies action
    if p_high > 0 and o_low > 0:
        o_low += p_high
        if o_low >= version:
            o_low = 0

        # re-order highs, lows
        o_high, o_low = reorder(o_high, o_low)
    
        # repack out-state
        out_state_str = f'{p_high}{p_low}{o_high}{o_low}'
        out_state_label = fr'{p_high}{p_low}\n{o_high}{o_low}'

        # create node
        out_state = None
        if out_state_str in graph.nodes():
            out_state = graph.get_node(out_state_str)
            out_state_exists = True
        else:
            graph.add_node(out_state_str, label=out_state_label)
            out_state = graph.get_node(out_state_str)

        # create edge
        if not graph.has_edge(in_state, out_state):
            graph.add_edge(in_state, out_state, label='HL')
            path = graph.get_edge(in_state, out_state)
            highlight_path(path)
            snapshot(graph)

        if not out_state_exists:
            generate_paths(graph, out_state, version)

    if path:
        revert_path(path)

    return None

def generate_path_lh(graph: AGraph, in_state, o_high, o_low, p_high, p_low, version):
    out_state_exists = False
    path = None

    # applies action
    if p_low > 0 and o_high > 0:
        o_high += p_low
        if o_high >= version:
            o_high = 0

        # re-order highs, lows
        o_high, o_low = reorder(o_high, o_low)
    
        # repack out-state
        out_state_str = f'{p_high}{p_low}{o_high}{o_low}'
        out_state_label = fr'{p_high}{p_low}\n{o_high}{o_low}'

        # create node
        out_state = None
        if out_state_str in graph.nodes():
            out_state = graph.get_node(out_state_str)
            out_state_exists = True
        else:
            graph.add_node(out_state_str, label=out_state_label)
            out_state = graph.get_node(out_state_str)

        # create edge
        if not graph.has_edge(in_state, out_state):
            graph.add_edge(in_state, out_state, label='LH')
            path = graph.get_edge(in_state, out_state)
            highlight_path(path)
            snapshot(graph)

        if not out_state_exists:
            generate_paths(graph, out_state, version)

    if path:
        revert_path(path)

    return None

def generate_path_ll(graph: AGraph, in_state, o_high, o_low, p_high, p_low, version):
    out_state_exists = False
    path = None

    # applies action
    if p_low > 0 and o_low > 0:
        o_low += p_low
        if o_low >= version:
            o_low = 0

        # re-order highs, lows
        o_high, o_low = reorder(o_high, o_low)
    
        # repack out-state
        out_state_str = f'{p_high}{p_low}{o_high}{o_low}'
        out_state_label = fr'{p_high}{p_low}\n{o_high}{o_low}'

        # create node
        out_state = None
        if out_state_str in graph.nodes():
            out_state = graph.get_node(out_state_str)
            out_state_exists = True
        else:
            graph.add_node(out_state_str, label=out_state_label)
            out_state = graph.get_node(out_state_str)

        # create edge
        if not graph.has_edge(in_state, out_state):
            graph.add_edge(in_state, out_state, label='LL')
            path = graph.get_edge(in_state, out_state)
            highlight_path(path)
            snapshot(graph)

        if not out_state_exists:
            generate_paths(graph, out_state, version)

    if path:
        revert_path(path)

    return None

def generate_path_su1(graph: AGraph, in_state, o_high, o_low, p_high, p_low, version):
    out_state_exists = False
    path = None

    # applies action
    if p_high > 0 and p_low > 0 and p_high < version - 1:
        p_high += 1
        p_low -= 1

        # repack out-state
        out_state_str = f'{p_high}{p_low}{o_high}{o_low}'
        out_state_label = fr'{p_high}{p_low}\n{o_high}{o_low}'

        # create node
        out_state = None
        if out_state_str in graph.nodes():
            out_state = graph.get_node(out_state_str)
            out_state_exists = True
        else:
            graph.add_node(out_state_str, label=out_state_label)
            out_state = graph.get_node(out_state_str)

        # create edge
        if not graph.has_edge(in_state, out_state):
            graph.add_edge(in_state, out_state, label='SU1')
            path = graph.get_edge(in_state, out_state)
            highlight_path(path)
            snapshot(graph)

        if not out_state_exists:
            generate_paths(graph, out_state, version)

    if path:
        revert_path(path)

    return None

def generate_path_sd1(graph: AGraph, in_state, o_high, o_low, p_high, p_low, version):
    out_state_exists = False
    path = None

    # TODO: need to guard against shift swaps

    # applies action
    if p_high > 1 and p_high > p_low and p_high - 1 != p_low and p_low + 1 != p_high:
        p_high -= 1
        p_low += 1

        # repack out-state
        out_state_str = f'{p_high}{p_low}{o_high}{o_low}'
        out_state_label = fr'{p_high}{p_low}\n{o_high}{o_low}'

        # create node
        out_state = None
        if out_state_str in graph.nodes():
            out_state = graph.get_node(out_state_str)
            out_state_exists = True
        else:
            graph.add_node(out_state_str, label=out_state_label)
            out_state = graph.get_node(out_state_str)

        # create edge
        if not graph.has_edge(in_state, out_state):
            graph.add_edge(in_state, out_state, label='SD1')
            path = graph.get_edge(in_state, out_state)
            highlight_path(path)
            snapshot(graph)

        if not out_state_exists:
            generate_paths(graph, out_state, version)

    if path:
        revert_path(path)

    return None

def reorder(high, low):
    if high < low:
        return low, high
    return high, low

def get_path_viz():
    global seq
    seq += 1
    filename = f'{file_prefix}-{str(seq).zfill(4)}.png'
    filepath = os.path.join(path_viz, filename)
    return filepath

def snapshot(graph, force=False, display=True):
    if make_snapshots or force:
        filepath = get_path_viz()
        print(filepath)
        graph.draw(filepath)
        time.sleep(0.2)
        if display:
            graphviz.view(filepath)

def highlight_state(state: Node):
    if make_snapshots:
        state.attr['color'] = 'blue'
        state.attr['penwidth'] = 3.0
        state.attr['fontcolor'] = 'blue'

def highlight_path(path: Edge):
    if make_snapshots:
        path.attr['color'] = 'blue'
        path.attr['penwidth'] = 3.0
        path.attr['fontcolor'] = 'blue'

def revert_state(state: Node):
    if make_snapshots:
        state.attr['color'] = 'black'
        state.attr['penwidth'] = 1.0
        state.attr['fontcolor'] = 'black'

def revert_path(path: Edge):
    if make_snapshots:
        path.attr['color'] = 'black'
        path.attr['penwidth'] = 1.0
        path.attr['fontcolor'] = 'black'

def write_dot(graph: AGraph):
    filename = f'{file_prefix}.dot'
    filepath = os.path.join(path_viz, filename)
    graph.write(path=filepath)

def main():
    global file_prefix
    version = 4
    file_prefix = f'version{version}'

    graph = generate_graph(version=version)
    # graph = generate()
    write_dot(graph)

    snapshot(graph, force=True)

    print('done')

if __name__ == '__main__':
    main()
