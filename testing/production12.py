import unittest
from GramatykiGrafoweProjekt import Graph, CannotApplyProductionError, Node
from GramatykiGrafoweProjekt.project.t1 import P1, P9, P12, make_initial_graph


class Production12Test(unittest.TestCase):

    def test_empty_graph(self):
        with self.assertRaises(CannotApplyProductionError):
            Graph().apply_production(P9)

    def test_correct(self):
        G = make_initial_graph()
        G.apply_productions([P1, P9, P9])
        G.display()
        G.apply_production(P12)
        G.display()

    def test_removed_one_node(self):
        G = make_initial_graph()
        G.apply_productions([P1, P9, P9])
        G.display()
        I = G.get_first_node_with_label('I')
        G.remove_node(I)
        with self.assertRaises(CannotApplyProductionError):
            G.apply_production(P12)

    def test_different_node(self):
        G = make_initial_graph()
        G.apply_productions([P1, P9, P9])
        I = G.get_first_node_with_label('I')
        E = Node('E', I.x, I.y, I.level)
        G.replace_node(I, E)
        G.display()
        with self.assertRaises(CannotApplyProductionError):
            G.apply_production(P12)

    def test_additional_edge_between_I(self):
        G = make_initial_graph()
        G.apply_productions([P1, P9, P9])
        I1 = G.get_first_node_with_label('I')
        I1_neighbours = G.get_node_neighbours(I1)
        G.remove_node(I1)
        I2 = G.get_first_node_with_label('I')
        I2_neighbours = G.get_node_neighbours(I2)
        G.remove_node(I2)
        G.add_nodes([I1, I2])
        G.new_edge(I1, I2)
        G.new_edges([(I1, n) for n in I1_neighbours])
        G.new_edges([(I2, n) for n in I2_neighbours])
        G.display()
        with self.assertRaises(CannotApplyProductionError):
            G.apply_production(P12)

    def test_no_one_triangle(self):
        G = make_initial_graph()
        G.apply_productions([P1, P9, P9])
        I = G.get_first_node_with_label('I')
        G.remove_nodes([x for x in G.get_neighbors_with_label(I, 'E')])
        G.display()
        with self.assertRaises(CannotApplyProductionError):
            G.apply_production(P12)

    def test_different_labels_in_triangle(self):
        G = make_initial_graph()
        G.apply_productions([P1, P9, P9])
        I = G.get_first_node_with_label('I')
        I_neighbours = [x for x in G.get_neighbors_with_label(I, 'E')]
        for neighbour in I_neighbours:
            n_ns = G.get_node_neighbours(neighbour)
            T = Node('T', neighbour.x, neighbour.y, neighbour.level)
            G.replace_node(neighbour, T)
        G.display()
        with self.assertRaises(CannotApplyProductionError):
            G.apply_production(P12)

    def test_multiple_productions(self):
        G = make_initial_graph()
        G.apply_productions([P1, P9, P9, P12, P9, P9])
        G.display()
        G.apply_production(P12)
        G.display()

    def test_multiple_productions_failed(self):
        G = make_initial_graph()
        G.apply_productions([P1, P9, P9, P12, P9])
        G.display()
        with self.assertRaises(CannotApplyProductionError):
            G.apply_production(P12)

    def test_multiple_productions_more(self):
        G = make_initial_graph()
        G.apply_productions([P1, P9, P9, P12, P9, P9, P12, P9, P9])
        G.display()
        G.apply_production(P12)
        G.display()


if __name__ == '__main__':
    unittest.main()
