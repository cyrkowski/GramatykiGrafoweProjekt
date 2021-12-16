from typing import Dict, List, Optional, Tuple

import matplotlib.pyplot as plot
import networkx as nx
from networkx import Graph as NGraph

from GramatykiGrafoweProjekt import Node, Graph

Y_SHIFT_FACTOR = 15
MAX_LEVEL = 3  # number of productions for testing

node_colors = {
    0: {
        'E': '#fe0000',
        'e': '#fe0000',
    },
    1: {
        'E': '#4e81bd',
        'I': '#c0504d',
        'i': '#c0504d',
    },
    2: {
        'E': '#93d051',
        'I': '#f79645',
        'i': '#f79645',
    },
    3: {
        'E': '#feff00',
        'I': '#d9d9d9',
        'i': '#d9d9d9',
    },
}


def get_node_color(node: Node) -> str:
    return node_colors.get(min(node.level, MAX_LEVEL), {}).get(node.label, 'blue')


def get_node_colors(G: NGraph) -> List[str]:
    return [get_node_color(node) for node in G.nodes]


def get_node_labels(G: NGraph) -> Dict[int, str]:
    return {
        node: node.label
        for node in G.nodes
    }


def calculate_layout(G: NGraph) -> Dict[int, Tuple[float, float]]:
    return {
        node: (node.x, node.y - node.level * Y_SHIFT_FACTOR)
        for node in G.nodes
    }


def draw_graph(G: Graph, *, level: Optional[int] = None) -> plot.Figure:
    fig, ax = plot.subplots()
    ax.set_aspect('equal', adjustable='datalim')
    ax.set(xlabel='$x$', ylabel='$y$')

    G = G._Graph
    if level is not None:
        G = G.subgraph([node for node in G.nodes if node.level == level])

    positions = calculate_layout(G)
    node_color = get_node_colors(G)
    labels = get_node_labels(G)
    nx.draw(G, ax=ax, pos=positions, node_color=node_color, labels=labels)

    return fig


def display(G: Graph, **kwargs):
    draw_graph(G, **kwargs)
    plot.show()
