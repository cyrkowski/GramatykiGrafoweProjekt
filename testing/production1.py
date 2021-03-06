import unittest
from GramatykiGrafoweProjekt import Graph, CannotApplyProductionError, Node
from GramatykiGrafoweProjekt.project.t1 import P1, make_initial_graph


class MyTestCase(unittest.TestCase):
    def test_empty_graph(self):
        with self.assertRaises(CannotApplyProductionError):
            Graph().apply_production(P1)

    def test_valid_graph(self):
        G = make_initial_graph()
        G.apply_production(P1)
        G.display()
        self.assertEqual(G.get_nodes_number, 7)

    def test_invalid_graph(self):
        G = Graph()
        i = Node(label='i', x=1, y=1, level=0)
        G.add_node(i)
        G.display()
        with self.assertRaises(CannotApplyProductionError):
            G.apply_production(P1)

    def test_big_graph(self):
        G = make_initial_graph()
        G.apply_production(P1)
        G.apply_production(P1)
        G.display()
        self.assertEqual(G.get_nodes_number, 13)


if __name__ == '__main__':
    unittest.main()
