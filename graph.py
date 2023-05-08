import networkx as nx
import matplotlib.pyplot as plt

possible_colors = ["red", "green", "blue", "yellow", "orange", "purple", "pink", "brown", "gold", "aqua", "violet"]

class Graph:

    def __init__(self, adjacency_list, chromatic_number, maximum_degree, number_of_edges, number_of_vertices):
        self.adjacency_list = adjacency_list
        self.chromatic_number = chromatic_number
        self.maximum_degree = maximum_degree
        self.number_of_edges = number_of_edges
        self.number_of_vertices = number_of_vertices
    

    def max_fitness(self):
        return self.number_of_edges * 2
    

    def __str__(self):
        return f"<{str(self.adjacency_list)}, chr_num={self.chromatic_number}, max_deg={self.maximum_degree}>"


    def __repr__(self):
        return f"<{str(self.adjacency_list)}, chr_num={self.chromatic_number}, max_deg={self.maximum_degree}>"
    

    def draw(self, solution):
        if self.chromatic_number > len(possible_colors):
            return
        network = nx.Graph()
        network.add_nodes_from([i + 1 for i in range(len(self.adjacency_list))])
        for vertice, adjacent_vertices in self.adjacency_list.items():
            for adjacent_vertice in adjacent_vertices:
                network.add_edge(vertice + 1, adjacent_vertice + 1)
        color_list = [possible_colors[i - 1] for i in solution]
        nx.draw(network, node_color=color_list, with_labels=True)
        plt.show()        
