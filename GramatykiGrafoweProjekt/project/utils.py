from typing import Tuple

from GramatykiGrafoweProjekt import Node, Graph
from GramatykiGrafoweProjekt.exceptions import TriangleNotFoundError


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
