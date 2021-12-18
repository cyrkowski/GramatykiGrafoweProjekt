import unittest
from GramatykiGrafoweProjekt import Graph, Node
from GramatykiGrafoweProjekt.exceptions import TriangleNotFoundError
from GramatykiGrafoweProjekt.project.utils import get_triangle_vertices


class GraphOperationsTest(unittest.TestCase):

    def test_add_node(self):
        G = Graph()
        E = Node(label='E', x=1, y=1, level=0)
        G.add_node(E)
        self.assertEqual(G.get_nodes_number, 1)
        self.assertTrue(G.has_node(E))
        I = Node(label='I', x=2, y=2, level=0)
        G.add_node(I)
        self.assertEqual(G.get_nodes_number, 2)
        self.assertTrue(G.has_node(I))

    def test_remove_node(self):
        G = Graph()
        E = Node(label='E', x=1, y=1, level=0)
        G.add_node(E)
        self.assertEqual(G.get_nodes_number, 1)
        self.assertTrue(G.has_node(E))
        G.remove_node(E)
        self.assertEqual(G.get_nodes_number, 0)
        self.assertFalse(G.has_node(E))

    def test_add_edge(self):
        G = Graph()
        E1 = Node(label='E', x=1, y=1, level=0)
        E2 = Node(label='E', x=0, y=0, level=0)
        G.add_nodes([E1, E2])
        G.new_edge(E1, E2)
        self.assertEqual(G.get_edges_number, 1)

    def test_add_edge_to_empty_graph(self):
        G = Graph()
        E1 = Node(label='E', x=1, y=1, level=0)
        E2 = Node(label='E', x=0, y=0, level=0)
        with self.assertRaises(AssertionError):
            G.new_edge(E1, E2)

    def test_get_triangle(self):
        G = Graph()
        I = Node(label='I', x=0.5, y=0.6, level=0)
        E1 = Node(label='E', x=0, y=1, level=0)
        E2 = Node(label='E', x=1, y=1, level=0)
        E3 = Node(label='E', x=0.5, y=0, level=0)
        G.add_nodes([E1, E2, E3, I])
        G.new_edges([
            (E1, E2), (E1, E3), (E2, E3),
            (I, E1), (I, E2), (I, E3)
        ])
        self.assertEqual(G.get_nodes_number, 4)
        self.assertEqual(G.get_edges_number, 6)
        self.assertEqual((E1, E2, E3), get_triangle_vertices(G, I))

    def test_get_triangle_if_not_exists(self):
        G = Graph()
        I = Node(label='I', x=0.5, y=0.6, level=0)
        E1 = Node(label='E', x=0, y=1, level=0)
        E2 = Node(label='E', x=1, y=1, level=0)
        E3 = Node(label='E', x=0.5, y=0, level=0)
        G.add_nodes([E1, E2, E3, I])
        G.new_edges([
            (E1, E2), (E1, E3),
            (I, E1), (I, E2), (I, E3)
        ])
        with self.assertRaises(TriangleNotFoundError):
            get_triangle_vertices(G, I)

    def test_get_triangle_if_square_1(self):
        G = Graph()
        I = Node(label='I', x=0.5, y=0.6, level=0)
        E1 = Node(label='E', x=0, y=1, level=0)
        E2 = Node(label='E', x=1, y=1, level=0)
        E3 = Node(label='E', x=1, y=0, level=0)
        E4 = Node(label='E', x=1, y=1, level=0)
        G.add_nodes([E1, E2, E3, E4, I])
        G.new_edges([
            (E1, E2), (E2, E3), (E3, E4), (E4, E1),
            (I, E1), (I, E2), (I, E3), (I, E4),
        ])
        with self.assertRaises(TriangleNotFoundError):
            get_triangle_vertices(G, I)

    def test_get_triangle_if_square_2(self):
        G = Graph()
        I = Node(label='I', x=0.5, y=0.6, level=0)
        E1 = Node(label='E', x=0, y=1, level=0)
        E2 = Node(label='E', x=1, y=1, level=0)
        E3 = Node(label='E', x=1, y=0, level=0)
        E4 = Node(label='E', x=1, y=1, level=0)
        G.add_nodes([E1, E2, E3, E4, I])
        G.new_edges([
            (E1, E2), (E2, E3), (E3, E4), (E4, E1),
            (I, E1), (I, E2), (I, E3),
        ])
        with self.assertRaises(TriangleNotFoundError):
            get_triangle_vertices(G, I)


if __name__ == '__main__':
    unittest.main()
