import os
import time

import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout, to_agraph
# import pygraphviz as pgv
import graphviz

file_prefix = 'snap'
seq = 0
path_viz = 'viz'

def generate(version=0):
    graph = nx.DiGraph()

    # set graph attributes
    graph.graph['graph'] = {
        'layout': 'dot',
        'fontname': 'Courier New',
        'size': '7.5,10',
        'ratio': 'fill'
    }

    # set node attributes
    graph.graph['node'] = {
        'shape':'circle',
        'fontname': 'Courier New'
    }

    # set edge attributes
    graph.graph['edge'] = {
        'arrowsize':'1.0',
        'fontname': 'Courier New'
    }

    # set origin
    graph.add_node('1111', label=r'11\n11', shape='doublecircle')

    generate_paths(graph, '1111', version)

    return graph

def generate_paths(graph: nx.DiGraph, in_state, version):
    end_state = False

    # unpacks in-state
    o_high, o_low, p_high, p_low = (
        int(in_state[0]), int(in_state[1]), int(in_state[2]), int(in_state[3])
    )

    # check for end state
    if p_high == p_low == 0:
        end_state = True
        graph.nodes[in_state]['shape'] = 'doublecircle'
        return

    # apply actions
    generate_path_hh(graph, in_state, o_high, o_low, p_high, p_low, version)

    return

def generate_path_hh(graph: nx.DiGraph, in_state, o_high, o_low, p_high, p_low, version):
    out_state_exists = False

    # applies action
    if p_high > 0 and o_high > 0:
        o_high += p_high
        if o_high >= version:
            o_high = 0

        # re-order highs, lows
        if o_high < o_low:
            o_high, o_low = o_low, o_high
    
        # repack out-state
        out_state = f'{p_high}{p_low}{o_high}{o_low}'
        out_state_label = fr'{p_high}{p_low}\n{o_high}{o_low}'

        # create node
        if out_state in graph.nodes:
            out_state_exists = True
        else:
            graph.add_node(out_state, label=out_state_label)

        # create edge
        graph.add_edge(in_state, out_state, label='HH')

        snapshot(graph)

        if not out_state_exists:
            generate_paths(graph, out_state, version)

    return None

def get_path_viz():
    global seq
    seq += 1
    filename = f'{file_prefix}-{str(seq).zfill(4)}.png'
    file_path = os.path.join(path_viz, filename)
    return file_path

def snapshot(graph):
    agraph = to_agraph(graph)
    agraph.layout('dot')
    file_path = get_path_viz()
    agraph.draw(file_path)
    # graphviz.render('dot', filepath=file_path)
    time.sleep(0.2)
    graphviz.view(file_path)

def print_dot(graph):
    agraph = to_agraph(graph)
    print(agraph)

def generate_graph():
    global file_prefix
    version = 2
    file_prefix = f'version{version}'

    graph = generate(version=version)
    # graph = generate()
    print_dot(graph)

    snapshot(graph)

if __name__ == '__main__':
    generate_graph()
