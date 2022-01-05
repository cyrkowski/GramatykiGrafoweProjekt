from typing import Tuple
from math import sqrt

from GramatykiGrafoweProjekt import Node, Graph
from GramatykiGrafoweProjekt.exceptions import TriangleNotFoundError

SCALE_MOVE = 5


def get_triangle_vertices(G: Graph, I: Node) -> Tuple[Node, Node, Node]:
    E_neighbours = G.get_neighbors_with_label(I, 'E')
    if len(E_neighbours) != 3:
        raise TriangleNotFoundError()

    E1 = min(E_neighbours, key=lambda node: (node.x, node.y))
    E_neighbours.remove(E1)
    E3 = next(node for node in E_neighbours if node in G.get_node_neighbours(E1) and node.x > E1.x)
    E_neighbours.remove(E3)
    E2 = next(node for node in E_neighbours if node in G.get_node_neighbours(E3))

    return E1, E3, E2


def get_triangle_vertices_for_p5(G: Graph, I: Node) -> Tuple[Node, Node, Node, Node, Node, Node]:
    E_neighbours = G.get_neighbors_with_label(I, 'E')
    if len(E_neighbours) != 3:
        raise TriangleNotFoundError()

    E1 = min(E_neighbours, key=lambda node: sqrt(
        (node.x - SCALE_MOVE) * (node.x - SCALE_MOVE) + (node.y - SCALE_MOVE) * (node.y - SCALE_MOVE)))
    E_neighbours.remove(E1)

    E2 = next(node for node in E_neighbours if node in G.get_node_neighbours(E1) and node in G.get_node_neighbours(I))
    E_neighbours.remove(E2)

    E3 = next(node for node in E_neighbours if node in G.get_node_neighbours(E2) and node in G.get_node_neighbours(I))
    E_neighbours.remove(E3)

    E4 = next(node for node in G.get_node_neighbours(E3) if node not in E_neighbours \
              and node.x == (E1.x + E3.x) / 2 and node.y == (E1.y + E3.y) / 2)

    return E1, E2, E3, E4, E5, E6
