from GramatykiGrafoweProjekt import Graph, NodeNotFoundError, CannotApplyProductionError, Node
from GramatykiGrafoweProjekt.exceptions import TriangleNotFoundError
from GramatykiGrafoweProjekt.project.utils import get_triangle_vertices

SCALE_MOVE = 5


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
