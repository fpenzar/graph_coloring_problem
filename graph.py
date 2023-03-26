class Graph:

    def __init__(self, adjacency_list, chromatic_number, maximum_degree, number_of_edges):
        self.adjacency_list = adjacency_list
        self.chromatic_number = chromatic_number
        self.maximum_degree = maximum_degree
        self.number_of_edges = number_of_edges
    

    def max_fitness(self):
        return self.number_of_edges * 2
    

    def __str__(self):
        return f"<{str(self.adjacency_list)}, chr_num={self.chromatic_number}, max_deg={self.maximum_degree}>"


    def __repr__(self):
        return f"<{str(self.adjacency_list)}, chr_num={self.chromatic_number}, max_deg={self.maximum_degree}>"