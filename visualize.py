"""Visualize graph functions.
"""
import os
import time

import graphviz
from pygraphviz import AGraph
from pygraphviz.agraph import Node, Edge


class Visualizer:
    def __init__(self) -> None:
        self.file_prefix = 'snap'
        self.seq = 0
        self.path_viz = 'viz'
        self.make_snapshots = False

    def get_path_viz(self):
        self.seq += 1
        filename = f'{self.file_prefix}-{str(self.seq).zfill(4)}.png'
        filepath = os.path.join(self.path_viz, filename)
        return filepath

    def snapshot(self, graph, force=False, display=True):
        if self.make_snapshots or force:
            filepath = self.get_path_viz()
            print(filepath)
            graph.draw(filepath)
            time.sleep(0.2)
            if display:
                graphviz.view(filepath)

    def highlight_state(self, state: Node):
        if self.make_snapshots:
            state.attr['color'] = 'blue'
            state.attr['penwidth'] = 3.0
            state.attr['fontcolor'] = 'blue'

    def highlight_path(self, path: Edge):
        if self.make_snapshots:
            path.attr['color'] = 'blue'
            path.attr['penwidth'] = 3.0
            path.attr['fontcolor'] = 'blue'

    def revert_state(self, state: Node):
        if self.make_snapshots:
            state.attr['color'] = 'black'
            state.attr['penwidth'] = 1.0
            state.attr['fontcolor'] = 'black'

    def revert_path(self, path: Edge):
        if self.make_snapshots:
            path.attr['color'] = 'black'
            path.attr['penwidth'] = 1.0
            path.attr['fontcolor'] = 'black'

    def write_dot(self, graph: AGraph):
        filename = f'{self.file_prefix}.dot'
        filepath = os.path.join(self.path_viz, filename)
        graph.write(path=filepath)
