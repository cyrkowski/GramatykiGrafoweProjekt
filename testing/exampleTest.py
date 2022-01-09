from GramatykiGrafoweProjekt import Node
from GramatykiGrafoweProjekt.project.t1 import make_initial_graph, P1, P2

if __name__ == '__main__':
    G = make_initial_graph()
    G.apply_productions([P1])
    E = Node(label='E', x=1, y=1, level=1)
    I = G.get_first_node_with_label('I')
    G.add_node(E)
    G.new_edge(E, I)
    G.display()
    G.apply_productions([P2])
    G.display()
    #
    # G = make_initial_graph()
    # G.apply_productions([P1, P2, P2, P2])
    # G.display()
