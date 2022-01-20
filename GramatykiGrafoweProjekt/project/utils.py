from typing import Tuple

from GramatykiGrafoweProjekt import Node, Graph
from GramatykiGrafoweProjekt.exceptions import TriangleNotFoundError, NodeNotFoundError
from math import sqrt

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


def get_triangle_vertices_for_p3(G: Graph, I: Node) -> Tuple[Node, Node, Node, Node]:
    E_neighbours = G.get_neighbors_with_label(I, 'E')
    if len(E_neighbours) < 3:
        raise TriangleNotFoundError()

    E1 = min(E_neighbours,
        key=lambda node: sqrt((node.x - SCALE_MOVE) * (node.x - SCALE_MOVE) + (node.y - SCALE_MOVE) * (node.y - SCALE_MOVE)))
    E_neighbours.remove(E1)
    E2 = next(node for node in E_neighbours if node in G.get_node_neighbours(E1) and node in G.get_node_neighbours(I))
    E_neighbours.remove(E2)
    E3 = next(node for node in E_neighbours if node in G.get_node_neighbours(E2) and node in G.get_node_neighbours(I))
    E_neighbours.remove(E3)
    E4 = [node for node in G.get_node_neighbours(E3) if node not in E_neighbours \
          and node.x == (E1.x + E3.x)/2 and node.y == (E1.y + E3.y)/2 and node.label == 'E']
    if len(E4) == 0:
        raise NodeNotFoundError()
    else:
        E4 = E4[0]
    return E1, E3, E2, E4

def get_triangle_vertices_for_p4(G: Graph, I: Node) -> Tuple[Node, Node, Node, Node, Node]:
    E_neighbours = G.get_neighbors_with_label(I, 'E')
    if len(E_neighbours) != 3:
        raise TriangleNotFoundError()
    E1_test=E_neighbours[0]
    E2_test=E_neighbours[1]
    E3_test=E_neighbours[2]
    E1_neighbours=G.get_node_neighbours(E1_test)
    E2_neighbours=G.get_node_neighbours(E2_test)

    counter=0
    iterate=True
    while iterate:
        try:
            node = next(E1_neighbours)
            if node == E2_test:
                counter+=1
            if node == E3_test:
                counter+=1
        except StopIteration:
            iterate=False
    iterate=True

    while iterate:
        try:
            node = next(E2_neighbours)
            if node == E3_test:
                counter+=1
        except StopIteration:
            iterate=False

    if counter !=1:
        raise TriangleNotFoundError()

    E1 = min(E_neighbours,
        key=lambda node: sqrt((node.x - SCALE_MOVE) * (node.x - SCALE_MOVE) + (node.y - SCALE_MOVE) * (node.y - SCALE_MOVE)))
    E_neighbours.remove(E1)
    E5 = min(G.get_neighbors_with_label(E1, "E"), key=lambda node: node.x)
    E4 = max(G.get_neighbors_with_label(E1, "E"), key=lambda node: node.x)

    E2 = next(node for node in E_neighbours if node in G.get_node_neighbours(E5) and node in G.get_node_neighbours(I))
    E_neighbours.remove(E2)

    E3 = next(node for node in E_neighbours if node in G.get_node_neighbours(E4) and node in G.get_node_neighbours(I))
    E_neighbours.remove(E3)

    if E5.x!=(E1.x+E2.x)/2:
        raise TriangleNotFoundError()
    if E4.x!=(E1.x+E3.x)/2:
        raise TriangleNotFoundError()
    return E1, E2, E3, E4, E5


def get_triangle_vertices_for_p5(G: Graph, I: Node) -> Tuple[Node, Node, Node, Node, Node, Node]:
    E_neighbours = G.get_neighbors_with_label(I, 'E')
    if len(E_neighbours) != 3:
        raise TriangleNotFoundError()

    E1 = min(E_neighbours, key=lambda node: sqrt(
        (node.x - SCALE_MOVE) * (node.x - SCALE_MOVE) + (node.y - SCALE_MOVE) * (node.y - SCALE_MOVE)))
    E_neighbours.remove(E1)
    E2 = min(E_neighbours, key=lambda node: node.y)
    E_neighbours.remove(E2)
    E3 = max(E_neighbours, key=lambda node: node.y)
    E_neighbours.remove(E3)

    E4 = next(node for node in G.get_node_neighbours(E1) if node in G.get_node_neighbours(E1) and node in G.get_node_neighbours(E3) and node.label == 'E')
    E5 = next(node for node in G.get_node_neighbours(E1) if node in G.get_node_neighbours(E1) and node in G.get_node_neighbours(E2) and node.label == 'E')
    E6 = next(node for node in G.get_node_neighbours(E3) if node in G.get_node_neighbours(E3) and node in G.get_node_neighbours(E3) and node.label == 'E')

    return E1, E2, E3, E4, E5, E6
