import unittest
from GramatykiGrafoweProjekt import Graph, CannotApplyProductionError, Node
from GramatykiGrafoweProjekt.project.t3 import make_initial_graph, P4

class MyTestCase(unittest.TestCase):
    def test_production_empty_graph(self):
        with self.assertRaises(CannotApplyProductionError):
            Graph().apply_production(P4)

    def test_production_valid_graph(self):
        G = make_initial_graph()
        G.apply_production(P4)
        G.display()
        self.assertEqual(14, G.get_nodes_number)

    def test_production_invalid_graph(self):
        G = Graph()
        i = Node(label='i', x=1, y=1, level=0)
        G.add_node(i)
        with self.assertRaises(CannotApplyProductionError):
            G.apply_production(P4)


if __name__ == '__main__':
    unittest.main()
