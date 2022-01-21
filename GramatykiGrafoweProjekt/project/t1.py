from GramatykiGrafoweProjekt import Graph, NodeNotFoundError, CannotApplyProductionError, Node
from GramatykiGrafoweProjekt.exceptions import TriangleNotFoundError
from GramatykiGrafoweProjekt.project.utils import get_triangle_vertices, SCALE_MOVE


def make_initial_graph() -> Graph:
    G = Graph()
    E = Node(label='E', x=SCALE_MOVE, y=SCALE_MOVE, level=0)
    G.add_node(E)
    return G


def P1(G: Graph) -> None:
    try:
        E = G.get_first_node_with_label('E')
    except NodeNotFoundError:
        raise CannotApplyProductionError()

    x0 = E.x
    y0 = E.y
    level = E.level

    x1, y1 = x0 - SCALE_MOVE, y0 - SCALE_MOVE
    x2, y2 = x0 + SCALE_MOVE, y0 - SCALE_MOVE
    x3, y3 = x0 - SCALE_MOVE, y0 + SCALE_MOVE
    x4, y4 = x0 + SCALE_MOVE, y0 + SCALE_MOVE

    medium_x = (x1 + x4) / 2
    medium_y = (y1 + y4) / 2

    e = Node(label='e', x=x0, y=y0, level=level)
    I1 = Node(label='I', x=(x1 + medium_x) / 2, y=(y1 + medium_y) / 2, level=level + 1)
    I2 = Node(label='I', x=(x4 + medium_x) / 2, y=(y4 + medium_y) / 2, level=level + 1)
    E1 = Node(label='E', x=x1, y=y1, level=level + 1)
    E2 = Node(label='E', x=x2, y=y2, level=level + 1)
    E3 = Node(label='E', x=x3, y=y3, level=level + 1)
    E4 = Node(label='E', x=x4, y=y4, level=level + 1)

    G.replace_node(E, e)

    G.add_nodes([I1, I2, E1, E2, E3, E4])

    G.new_edges([
        (e, I1),
        (e, I2),
        (I1, E1), (I1, E2), (I1, E3),
        (I2, E2), (I2, E3), (I2, E4),
        (E1, E2), (E2, E4), (E4, E3), (E3, E1), (E3, E2)
    ])


def P2(G: Graph) -> None:
    try:
        I = G.get_first_node_with_label('I')
    except NodeNotFoundError:
        raise CannotApplyProductionError()

    level = I.level

    try:
        E1, E3, E2 = get_triangle_vertices(G, I)
    except TriangleNotFoundError:
        raise CannotApplyProductionError()

    x1, y1 = E1.x, E1.y
    x2, y2 = E2.x, E2.y
    x3, y3 = E3.x, E3.y

    x4, y4 = (x1 + x3) / 2, (y1 + y3) / 2

    i = Node(label='i', x=I.x, y=I.y, level=level)

    I1 = Node(label='I', x=(x1 + x2 + x4) / 3, y=(y1 + y2 + y3) / 3, level=level + 1)
    I2 = Node(label='I', x=(x2 + x3 + x4) / 3, y=(y2 + y3 + y4) / 3, level=level + 1)

    E1 = Node(label='E', x=x1, y=y1, level=level + 1)
    E2 = Node(label='E', x=x2, y=y2, level=level + 1)
    E3 = Node(label='E', x=x3, y=y3, level=level + 1)
    E4 = Node(label='E', x=x4, y=y4, level=level + 1)

    G.replace_node(I, i)

    G.add_nodes([
        I1, I2,
        E1, E2, E3, E4
    ])

    G.new_edges([
        (i, I1), (i, I2),
        (I1, E1), (I1, E2), (I1, E4),
        (I2, E2), (I2, E3), (I2, E4),
        (E1, E2), (E1, E4), (E2, E3), (E2, E4), (E3, E4)
    ])


def P9(G: Graph) -> None:
    try:
        I = G.get_first_node_with_label('I')
    except NodeNotFoundError:
        raise CannotApplyProductionError()

    level = I.level

    try:
        E1, E3, E2 = get_triangle_vertices(G, I)
    except TriangleNotFoundError:
        raise CannotApplyProductionError()

    x1, y1 = E1.x, E1.y
    x2, y2 = E2.x, E2.y
    x3, y3 = E3.x, E3.y

    i = Node(label='i', x=I.x, y=I.y, level=level)

    n_I = Node(label='I', x=(x1 + x2 + x3) / 3, y=(y1 + y2 + y3) / 3, level=level + 1)

    n_E1 = Node(label='E', x=x1, y=y1, level=level + 1)
    n_E2 = Node(label='E', x=x2, y=y2, level=level + 1)
    n_E3 = Node(label='E', x=x3, y=y3, level=level + 1)

    G.replace_node(I, i)

    G.add_nodes([n_I, n_E1, n_E2, n_E3])

    G.new_edges([
        (n_I, n_E1), (n_I, n_E2), (n_I, n_E3),
        (n_E1, n_E2), (n_E2, n_E3), (n_E3, n_E1),
        (i, n_I)
    ])


def verify_subgraph(graph: Graph, node: Node) -> bool:
    possble_valid_E = [n for n in graph.get_neighbors_with_label(node, 'E') if len(graph.get_neighbors_with_label(n, 'i')) == 2]
    if len(possble_valid_E) < 2:
        return False
    E1 = possble_valid_E[0]
    E2 = possble_valid_E[1]

    i1 = [n for n in graph.get_neighbors_with_label(E1, 'i') if n != node][0]
    i2 = [n for n in graph.get_neighbors_with_label(E2, 'i') if n != node][0]

    if i1 != i2:
        return False
    return verify_i_node(graph, i1) and verify_i_node(graph, node)


def verify_E_neighbour(graph: Graph, node: Node) -> bool:
    all_node_neighbours = list(graph.get_node_neighbours(node))
    if len(all_node_neighbours) < 3:
        return False
    E_neighbour = [E for E in graph.get_neighbors_with_label(node, 'E') if len(graph.get_neighbors_with_label(E, 'i')) == 2]
    if len(E_neighbour) < 2:
        return False
    E2 = E_neighbour[0]

    i_neighbours_node = graph.get_neighbors_with_label(node, 'i')
    if len(i_neighbours_node) < 2:
        return False
    i_neighbours_E2 = graph.get_neighbors_with_label(E2, 'i')
    if len(i_neighbours_E2) < 2:
        return False
    if not i_neighbours_E2.__contains__(i_neighbours_node[0]):
        return False
    if not i_neighbours_E2.__contains__(i_neighbours_node[1]):
        return False

    for i in i_neighbours_node:
        if not verify_i_node(graph, i):
            return False

    return True


def verify_i_node(graph: Graph, node: Node) -> bool:
    I_neighbours = graph.get_neighbors_with_label(node, 'I')
    if len(I_neighbours) != 1:
        return False
    I = I_neighbours[0]
    return verify_I_node(graph, I)


def verify_I_node(graph: Graph, node: Node) -> bool:
    E_neighbours = graph.get_neighbors_with_label(node, 'E')
    if len(E_neighbours) < 2:
        return False
    for E in E_neighbours:
        nei = [E_n for E_n in graph.get_neighbors_with_label(E, 'E') if E_n != E and E in E_neighbours]
        if nei is not []:
            return True
    return False


def get_P12_nodes(G: Graph) -> list[Node, Node, Node, Node, Node, Node]:
    valid_start_nodes = [node for node in G.get_nodes_with_label('i') if verify_subgraph(G, node)]
    if len(valid_start_nodes) < 1:
        raise NodeNotFoundError()
    i = valid_start_nodes[0]
    possble_valid_E = [n for n in G.get_neighbors_with_label(i, 'E') if
                       len(G.get_neighbors_with_label(n, 'i')) == 2]
    if len(possble_valid_E) < 2:
        raise NodeNotFoundError()
    E1 = possble_valid_E[0]
    E2 = possble_valid_E[1]

    i1 = [n for n in G.get_neighbors_with_label(E1, 'i') if n != i][0]
    i2 = [n for n in G.get_neighbors_with_label(E2, 'i') if n != i1][0]

    I1 = G.get_neighbors_with_label(i1, 'I')[0]
    I2 = G.get_neighbors_with_label(i2, 'I')[0]
    if I1 in G.get_node_neighbours(I2):
        raise NodeNotFoundError()

    E_I1_neigbours = sorted(G.get_neighbors_with_label(I1, 'E'), key=lambda n: (n.x, -n.y))
    nei = []
    for E in E_I1_neigbours:
        sorted_E_E_neighbours = sorted(G.get_neighbors_with_label(E, 'E'), key=lambda node: (node.x, -node.y))
        nei = [E_n for E_n in sorted_E_E_neighbours if E_n != E and E in E_I1_neigbours]
        if len(nei) > 0:
            E_I1_neigbours = [E, nei[0]]
            break

    if len(nei) == 0:
        raise NodeNotFoundError()

    E11 = min(E_I1_neigbours, key=lambda node: (node.y, node.x))
    E12 = max(E_I1_neigbours, key=lambda node: (node.y, node.x))

    E_I2_neigbours = sorted(G.get_neighbors_with_label(I2, 'E'), key=lambda n: (-n.x, n.y))
    for E in E_I2_neigbours:
        if E in E_I1_neigbours:
            continue
        sorted_E_E_neighbours = sorted(G.get_neighbors_with_label(E, 'E'), key=lambda node: (-node.x, node.y))
        nei = [E_n for E_n in sorted_E_E_neighbours if E_n != E]
        if len(nei) > 0:
            E_I2_neigbours = [E, nei[0]]
            break

    if len(nei) == 0:
        raise NodeNotFoundError()
    E21 = min(E_I2_neigbours, key=lambda node: (node.y, node.x))
    E22 = max(E_I2_neigbours, key=lambda node: (node.y, node.x))
    return I1, I2, E11, E12, E21, E22

def P12(G: Graph):
    try:
        I1, I2, E11, E12, E21, E22 = get_P12_nodes(G)
    except NodeNotFoundError:
        raise CannotApplyProductionError()

    E11_neighbours = G.get_node_neighbours(E11)
    E22_neighbours = G.get_node_neighbours(E22)
    G.remove_nodes([E11, E22])
    G.new_edges([
        (I1, E21),
        (I2, E12),
        (E12, E21)
    ] + [
        (E21, x) for x in E11_neighbours if x not in [I1, I2]
    ] + [
        (E12, x) for x in E22_neighbours if x not in [I1, I2]
    ])

    # if len(G.get_nodes) != 13:
    #     raise CannotApplyProductionError()

