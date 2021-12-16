
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from itertools import count
from typing import List, Iterable, Tuple, Callable

import networkx as nx
from networkx.classes.reportviews import NodeView

from GramatykiGrafoweProjekt.exceptions import NodeNotFoundError, CannotApplyProductionError


@dataclass(eq=True, frozen=True)
class Node:
    label: str
    x: float
    y: float
    level: int
    id: int = field(default_factory=count().__next__, init=False)


class NodeInformation:
    def __init__(self):
        self._dict = defaultdict(list)

    @staticmethod
    def get_key(node: Node) -> Tuple[int, float, float]:
        return node.level, node.x, node.y

    def add_node(self, node: Node) -> None:
        self._dict[self.get_key(node)].append(node)

    def remove_node(self, node: Node) -> None:
        self._dict[self.get_key(node)].remove(node)

    def get_duplicates_of(self, node: Node) -> Iterable[Node]:
        group = self._dict[node.level, node.x, node.y]
        return [n for n in group if n is not node and n.label == node.label]

    def get_duplicates_with_label(self, label: str) -> Iterable[List[Node]]:
        for group in self._dict.values():
            nodes = [n for n in group if n.label == label]
            if len(nodes) >= 2:
                yield nodes

    def count_duplicates(self) -> int:
        return sum(1 for group in self._dict.values() if len(group) >= 2)


def node_match(a: dict, b: dict) -> bool:
    a = a['node']
    b = b['node']
    return a.label == b.label and a.x == b.x and a.y == b.y and a.level == b.level


class Graph:
    def __init__(self):
        self._Graph = nx.Graph()
        self._node_information = NodeInformation()

    def __contains__(self, node: Node) -> bool:
        return self.has_node(node)

    @property
    def get_nodes(self) -> NodeView:
        return self._Graph.nodes

    @property
    def get_nodes_number(self) -> int:
        return self._Graph.number_of_nodes()

    @property
    def get_edges_number(self) -> int:
        return self._Graph.number_of_edges()

    def add_node(self, node: Node) -> None:
        self._Graph.add_node(node, node=node)
        self._node_information.add_node(node)

    def add_nodes(self, nodes: Iterable[Node]) -> None:
        for node in nodes:
            self.add_node(node)

    def new_edge(self, u: Node, v: Node) -> None:
        assert u in self, f'{u} not in graph'
        assert v in self, f'{v} not in graph'
        self._Graph.add_edge(u, v)

    def new_edges(self, edges: Iterable[Tuple[Node, Node]]):
        for u, v in edges:
            self.new_edge(u, v)

    def has_node(self, node: Node) -> bool:
        return node in self._Graph

    def remove_node(self, node: Node) -> None:
        self._Graph.remove_node(node)
        self._node_information.remove_node(node)

    def remove_nodes(self, nodes: Iterable[Node]) -> None:
        for node in nodes:
            self.remove_node(node)

    def remove_edge(self, u: Node, v: Node) -> None:
        assert u in self, f'{u} not in graph'
        assert v in self, f'{v} not in graph'
        self._Graph.remove_edge(u, v)

    def replace_node(self, old: Node, new: Node) -> None:
        neighbors = self.get_node_neighbours(old)
        self.remove_node(old)
        self.add_node(new)
        self.new_edges((n, new) for n in neighbors)

    def merge_two_nodes(self, old1: Node, old2: Node) -> Node:
        assert old1.label == old2.label and old1.x == old2.x and old1.y == old2.y and old1.level == old2.level
        neighbors = set(self.get_node_neighbours(old1)) | set(self.get_node_neighbours(old2)) - {old1, old2}
        self.remove_node(old1)
        self.remove_node(old2)
        new = Node(label=old1.label, x=old1.x, y=old1.y, level=old1.level)
        self.add_node(new)
        self.new_edges((n, new) for n in neighbors)
        return new

    def get_node_neighbours(self, node: Node):
        return self._Graph.neighbors(node)

    def get_first_node_with_label(self, label: str) -> Node:
        found = [node for node in self.get_nodes if node.label == label]
        if not found:
            raise NodeNotFoundError(f'Node with label "{label}" not found')
        return min(found, key=lambda node: (node.level, node.id))

    def get_neighbors_with_label(self, node: Node, label: str) -> List[Node]:
        return [n for n in self.get_node_neighbours(node) if n.label == label]

    def get_nodes_common_neighbors_with_label(self, a: Node, b: Node, label: str) -> Iterable[Node]:
        for node in self.get_node_neighbours(a):
            if node.label == label and node in self.get_node_neighbours(b):
                yield node

    def apply_production(self, production: Callable[[Graph], None], *, times: int = 1) -> Graph:
        for _ in range(times):
            production(self)
        return self

    def apply_productions(self, productions: Iterable[Callable[[Graph], None]]) -> Graph:
        for production in productions:
            production(self)
        return self

    def apply_production_while_possible(self, production: Callable[[Graph], None]) -> Graph:
        while True:
            try:
                production(self)
            except CannotApplyProductionError:
                return self

    def get_duplicates_of(self, node: Node) -> Iterable[Node]:
        return self._node_information.get_duplicates_of(node)

    def get_duplicates_with_label(self, label: str) -> Iterable[List[Node]]:
        return self._node_information.get_duplicates_with_label(label)

    def get_duplicates_number(self) -> int:
        return self._node_information.count_duplicates()

    def assert_no_duplicated_nodes(self) -> None:
        duplicates_number = self.get_duplicates_number()
        if duplicates_number:
            pass
        assert not duplicates_number, f'There are {duplicates_number} duplicated nodes'

    def is_isomorphic_with(self, other: Graph) -> bool:
        return nx.is_isomorphic(self._Graph, other._Graph, node_match=node_match)

    def display(self):
        from GramatykiGrafoweProjekt.vis import display
        display(self)
