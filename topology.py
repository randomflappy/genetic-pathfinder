import baseline_algorithms
from matplotlib import pyplot as plt
import networkx as nx


class Graph:
    def __init__(self, num_nodes, edges, is_directed=False):
        if len(edges) < 1:
            raise Exception('Graph should contain at least one node.')
        if len(edges[0]) == 2:
            self._is_weighted = False
        elif len(edges[0]) == 3:
            self._is_weighted = True
        else:
            raise Exception('Unsupported edge type.')

        self._is_directed = is_directed
        self.num_nodes = num_nodes
        self.data = [[0] * num_nodes for _ in range(num_nodes)]
        if self._is_weighted:
            for n1, n2, weight in edges:
                self.data[n1][n2] = weight
                if not is_directed:
                    self.data[n2][n1] = weight
        else:
            for n1, n2 in edges:
                self.data[n1][n2] = 1
                if not is_directed:
                    self.data[n2][n1] = 1

    def __repr__(self):
        header = '    '
        for i in range(len(self.data)):
            header += f'{i}: '
        header += '\n'
        return header + '\n'.join([f'{n}: {neighbours}' for n, neighbours in enumerate(self.data)])

    def __str__(self):
        return self.__repr__()

    def add_edge(self, edge: tuple[int, ...]):
        if self._is_weighted:
            if len(edge) != 3:
                raise Exception('Wrong edge type for weighted graph, should be tuple(int, int, int).')
            n1, n2, weight = edge
            self.data[n1][n2] = weight
            if not self._is_directed:
                self.data[n2][n1] = weight
        else:
            if len(edge) != 2:
                raise Exception('Wrong edge type for unweighted graph, should be tuple(int, int).')
            n1, n2 = edge
            self.data[n1][n2] = 1
            if not self._is_directed:
                self.data[n2][n1] = 1

    def remove_edge(self, edge: tuple[int, int]):
        n1, n2 = edge
        self.data[n1][n2] = 0
        if not self._is_directed:
            self.data[n2][n1] = 0


def draw_directed_weighted_graph(edges, path=None):
    edges = ((n1, n2, {"weight": weight}) for n1, n2, weight in edges)
    graph = nx.DiGraph(edges)
    position = nx.spring_layout(graph)
    if path:
        node_colors = ["#72f536" if node in path else "#4287f5" for node in graph.nodes()]
    else:
        node_colors = "#4287f5"
    nx.draw(graph, pos=position, with_labels=True, font_weight='bold', node_color=node_colors)
    edge_weight = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos=position, edge_labels=edge_weight)
    plt.show()


def main():
    num_nodes = 6
    edges = [(0, 1, 4), (0, 2, 2), (1, 3, 10), (1, 2, 5), (2, 4, 3), (3, 5, 11), (4, 3, 4)]
    graph = Graph(num_nodes, edges, is_directed=True)
    print(graph)
    result = baseline_algorithms.dijkstra(graph.data, 0, 5)
    print(result)

    draw_directed_weighted_graph(edges, path=result[0])


if __name__ == '__main__':
    main()
