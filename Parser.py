from graph import Graph


class Parser:
    
    def __init__(self, file):
        self.file = file
        self.graphs = []
        self.i = 0
    

    def parse(self):
        initial = True
        with open(self.file, "r") as file:
            for line in file.readlines():
                line = line.strip()
                if len(line) == 0:
                    continue
                # new graph definition
                if line.startswith("1:"):
                    if not initial:
                        self.graphs.append(Graph(adjacency_list, 
                                                 chromatic_number, 
                                                 max_degree,
                                                 number_of_edges,
                                                 number_of_vertices))
                    initial = False
                    adjacency_list = {}
                    max_degree = None
                    chromatic_number = None
                    number_of_edges = None
                    number_of_vertices = None
                key = line.split(":")[0]
                values = line.split(":")[1]
                # graph definition
                if key.strip().isnumeric():
                    adjacency_list.update({int(key)-1: []})
                    for value in values.split(" "):
                        if not value:
                            continue
                        adjacency_list[int(key)-1].append(int(value)-1)
                    continue
                # graph invariants
                if key == "Maximum Degree":
                    max_degree = int(values)
                    continue
                if key == "Chromatic Number":
                    if values.strip().isnumeric():
                        chromatic_number = int(values)
                    else:
                        chromatic_number = None
                    continue
                if key == "Number of Edges":
                    number_of_edges = int(values)
                    continue
                if key == "Number of Vertices":
                    number_of_vertices = int(values)
                    continue
    

    def next_graph(self) -> Graph:
        if self.i == len(self.graphs) - 1:
            return None
        else:
            self.i += 1
            return self.graphs[self.i - 1]
