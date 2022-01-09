import unittest
from GramatykiGrafoweProjekt import Graph, CannotApplyProductionError, Node
from GramatykiGrafoweProjekt.project.t2 import P3, make_initial_graph


class MyTestCase(unittest.TestCase):
    def test_production_empty_graph(self):
        with self.assertRaises(CannotApplyProductionError):
            Graph().apply_production(P3)

    def test_production_valid_graph(self):
        G = make_initial_graph()
        G.display()
        G.apply_production(P3)
        G.display()
        self.assertEqual(G.get_nodes_number, 11)

    def test_production_invalid_graph(self):
        G = Graph()
        i = Node(label='i', x=1, y=1, level=0)
        G.add_node(i)
        G.display()
        with self.assertRaises(CannotApplyProductionError):
            G.apply_production(P3)

    def test_production_wrong_label(self):
        G = make_initial_graph()
        G.display()
        e = G.get_first_node_with_label('E')
        m = Node(label='M', x=e.x, y=e.y, level=e.level)
        G.replace_node(e, m)
        G.display()
        with self.assertRaises(CannotApplyProductionError):
            G.apply_production(P3)

    def test_production_wrong_coords(self):
        G = make_initial_graph()
        G.display()
        e = G.get_first_node_with_label('E')
        m = Node(label='E', x=e.x/2, y=e.y/2, level=e.level)
        G.replace_node(e, m)
        G.display()
        with self.assertRaises(CannotApplyProductionError):
            G.apply_production(P3)

    def test_production_graph_removed_node(self):
        G = make_initial_graph()
        G.display()
        e = G.get_first_node_with_label('E')
        G.remove_node(e)
        G.display()
        with self.assertRaises(CannotApplyProductionError):
            G.apply_production(P3)

    def test_production_graph_removed_edge(self):
        G = make_initial_graph()
        G.display()
        i = G.get_first_node_with_label('I')
        e = [n for n in G.get_node_neighbours(i)][1]
        G.remove_edge(i, e)
        G.display()
        with self.assertRaises(CannotApplyProductionError):
            G.apply_production(P3)

    def test_production_graph_additional_node(self):
        param_list = [('E', 'N'), ('I', 'E')]
        for existing_node, node_to_add in param_list:
            with self.subTest():
                G = make_initial_graph()
                G.display()
                e = G.get_first_node_with_label(existing_node)
                n = Node(label=node_to_add, x=e.x/2, y=e.y/2, level=e.level)
                G.add_node(n)
                G.new_edge(e, n)
                G.display()
                G.apply_production(P3)
                G.display()
                self.assertEqual(G.get_nodes_number, 12)


if __name__ == '__main__':
    unittest.main()
