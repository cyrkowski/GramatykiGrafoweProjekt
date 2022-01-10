from GramatykiGrafoweProjekt import Graph, NodeNotFoundError, CannotApplyProductionError, Node
from GramatykiGrafoweProjekt.exceptions import TriangleNotFoundError
from GramatykiGrafoweProjekt.project.utils import SCALE_MOVE, get_triangle_vertices_for_p4


def make_initial_graph() -> Graph:
    G = Graph()
    E1 = Node(label='E', x=SCALE_MOVE, y=SCALE_MOVE, level=0)
    E2 = Node(label='E', x=E1.x, y=E1.y - SCALE_MOVE, level=0)
    E3 = Node(label='E', x=E1.x + SCALE_MOVE, y=E1.y + SCALE_MOVE, level=0)
    E4 = Node(label='E', x=(E1.x + E3.x) / 2, y=(E1.y + E3.y) / 2, level=0)
    E5 = Node(label='E', x=(E1.x + E2.x) / 2, y=(E1.y + E2.y) / 2, level=0)

    medium_x = (E1.x + E3.x) / 2
    medium_y = (E1.y + E5.y) / 2

    I = Node(label='I', x=(E1.x + medium_x) / 2, y=(E1.y + medium_y) / 2, level=0)

    G.add_nodes([I, E1, E2, E3, E4, E5])

    G.new_edges([
        (I, E1), (I, E2), (I, E3),
        (E1, E4), (E1, E5), (E4, E3), (E5, E2), (E2, E3)
    ])
    return G


def P4(G: Graph) -> None:
    try:
        I = G.get_first_node_with_label('I')
    except NodeNotFoundError:
        raise CannotApplyProductionError()

    level = I.level

    try:
        E1, E2, E3, E4, E5 = get_triangle_vertices_for_p4(G, I)
    except TriangleNotFoundError:
        raise CannotApplyProductionError()

    x1, y1 = E1.x, E1.y
    x2, y2 = E2.x, E2.y
    x3, y3 = E3.x, E3.y
    x4, y4 = E4.x, E4.y
    x5, y5 = E5.x, E5.y


    i = Node(label='i', x=I.x, y=I.y, level=level)

    I1 = Node(label='I', x=(x1 + x2 + x4) / 3, y=(y1 + y2 + y3) / 3, level=level + 1)
    I2 = Node(label='I', x=(x2 + x3 + x4) / 3, y=(y2 + y3 + y4) / 3, level=level + 1)
    I3 = Node(label='I', x=(x2 + x4 + x5) / 3, y=(y2 + y4 + y5) / 3, level=level + 1)

    E1 = Node(label='E', x=x1, y=y1, level=level + 1)
    E2 = Node(label='E', x=x2, y=y2, level=level + 1)
    E3 = Node(label='E', x=x3, y=y3, level=level + 1)
    E4 = Node(label='E', x=x4, y=y4, level=level + 1)
    E5 = Node(label='E', x=x5, y=y5, level=level + 1)

    G.replace_node(I, i)

    G.add_nodes([
        I1, I2, I3,
        E1, E2, E3, E4, E5,
    ])

    G.new_edges([
        (i, I1), (i, I2),
        (I1, E1), (I1, E4), (I1, E5),
        (I2, E2), (I2, E3), (I2, E5),
        (I3, E2), (I3, E4), (I3, E5),
        (E1, E4), (E1, E5),
        (E2, E4), (E2, E3), (E2, E5),
        (E3, E4),
        (E4, E5)
    ])
