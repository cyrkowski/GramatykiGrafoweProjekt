import unittest
from GramatykiGrafoweProjekt import Graph, CannotApplyProductionError, Node
from GramatykiGrafoweProjekt.project.t1 import P1, P2, make_initial_graph


class Production2Test(unittest.TestCase):

    def test_empty_graph(self):
        with self.assertRaises(CannotApplyProductionError):
            Graph().apply_production(P2)

    def test_after_first_production(self):
        G = make_initial_graph()
        G.apply_productions([P1, P2])
        G.display()
        self.assertEqual(G.get_nodes_number, 13)

    def test_production_no_triangle(self):
        G = Graph()
        i = Node(label='i', x=1, y=1, level=0)
        G.add_node(i)
        G.display()
        with self.assertRaises(CannotApplyProductionError):
            G.apply_production(P1)

    def test_not_triangle(self):
        G = make_initial_graph()
        G.apply_productions([P1])
        E = Node(label='E', x=1, y=1, level=1)
        I = G.get_first_node_with_label('I')
        G.add_node(E)
        G.new_edge(E, I)
        G.display()
        with self.assertRaises(CannotApplyProductionError):
            G.apply_production(P2)

    def test_no_i_node(self):
        G = make_initial_graph()
        G.apply_production(P1)
        E = Node(label='E', x=1, y=1, level=1)
        I1 = G.get_first_node_with_label('I')
        G.replace_node(I1, E)
        I2 = G.get_first_node_with_label('I')
        G.replace_node(I2, E)
        G.display()
        with self.assertRaises(CannotApplyProductionError):
            G.apply_production(P2)

    def test_one_init_node(self):
        G = make_initial_graph()
        G.apply_production(P1)
        E = Node(label='E', x=1, y=1, level=1)
        I = G.get_first_node_with_label('I')
        G.replace_node(I, E)
        G.display()
        G.apply_production(P2)
        self.assertEqual(G.get_nodes_number, 13)

    def test_one_edge_node_remove(self):
        G = make_initial_graph()
        G.apply_production(P1)
        E = G.get_first_node_with_label('E')
        G.remove_node(E)
        G.display()
        with self.assertRaises(CannotApplyProductionError):
            G.apply_production(P2)


if __name__ == '__main__':
    unittest.main()
