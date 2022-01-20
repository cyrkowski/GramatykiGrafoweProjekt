import unittest
from GramatykiGrafoweProjekt import Graph, CannotApplyProductionError, Node
from GramatykiGrafoweProjekt.project.t4 import make_initial_graph, P5


class MyTestCase(unittest.TestCase):
    def test_production_empty_graph(self):
        with self.assertRaises(CannotApplyProductionError):
            Graph().apply_production(P5)

    def test_production_valid_graph(self):
        G = make_initial_graph()
        G.apply_production(P5)
        G.display()
        self.assertEqual(17, G.get_nodes_number)

    def test_production_valid_graph_with_additional_node(self):
        G = make_initial_graph()
        I = Node(label='I', x=1, y=1, level=0)
        G.add_node(I)
        G.new_edge(G.get_first_node_with_label("E"), I)
        G.apply_production(P5)
        G.display()
        self.assertEqual(18, G.get_nodes_number)

    def test_production_invalid_graph_without_one_node(self):
        G = make_initial_graph()
        G.remove_node(G.get_first_node_with_label('E'))
        with self.assertRaises(CannotApplyProductionError):
            G.apply_production(P5)
            G.display()

    def test_production_invalid_graph(self):
        G = Graph()
        i = Node(label='i', x=1, y=1, level=0)
        G.add_node(i)
        with self.assertRaises(CannotApplyProductionError):
            G.apply_production(P5)


if __name__ == '__main__':
    unittest.main()
