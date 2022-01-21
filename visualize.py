"""Visualize graph functions.
"""
import os
import time

import graphviz
from pygraphviz import AGraph
from pygraphviz.agraph import Node, Edge


file_prefix = 'snap'
seq = 0
path_viz = 'viz'
make_snapshots = False

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
