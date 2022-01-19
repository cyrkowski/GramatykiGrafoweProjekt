import unittest
from GramatykiGrafoweProjekt import Graph, CannotApplyProductionError, Node
from GramatykiGrafoweProjekt.project.t3 import make_initial_graph, P4, make_triple_broken_graph, make_invalid_graph

class MyTestCase(unittest.TestCase):
    def test_production_empty_graph(self):
        with self.assertRaises(CannotApplyProductionError):
            Graph().apply_production(P4)

    def test_production_valid_graph(self):
        G = make_initial_graph()
        G.apply_production(P4)
        G.display()
        self.assertEqual(14, G.get_nodes_number)

    def test_production_additional_node(self):
        G = make_initial_graph()
        I = Node(label='I', x=1, y=1, level=0)
        G.add_node(I)
        G.new_edge(G.get_first_node_with_label("E"), I)
        G.display()
        G.apply_production(P4)
        G.display()
        self.assertEqual(G.get_nodes_number, 15)

    def test_production_three_edges_broken(self):
        G = make_triple_broken_graph()
        G.display()
        with self.assertRaises(CannotApplyProductionError):
            G.apply_production(P4)
            G.display()

    def test_coordinates_on_broken_edges(self):
        G = make_invalid_graph()
        G.display()
        with self.assertRaises(CannotApplyProductionError):
            G.apply_production(P4)
            G.display()


if __name__ == '__main__':
    unittest.main()
