import unittest
from GramatykiGrafoweProjekt import Graph, CannotApplyProductionError, Node
from GramatykiGrafoweProjekt.project.t2 import P3, make_initial_graph


class MyTestCase(unittest.TestCase):
    def test_production_empty_graph(self):
        with self.assertRaises(CannotApplyProductionError):
            Graph().apply_production(P3)

    def test_production_valid_graph(self):
        G = make_initial_graph()
        G.apply_production(P3)
        G.display()
        self.assertEqual(G.get_nodes_number, 11)

    def test_production_invalid_graph(self):
        G = Graph()
        i = Node(label='i', x=1, y=1, level=0)
        G.add_node(i)
        with self.assertRaises(CannotApplyProductionError):
            G.apply_production(P3)


if __name__ == '__main__':
    unittest.main()
