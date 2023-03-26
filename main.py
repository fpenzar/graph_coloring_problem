import pygad
from Parser import Parser

INPUT_FILE = "/home/filip/Work/FER/6_semestar/zavrsni_rad/sources/graphs/31_34.txt"



if __name__ == "__main__":
    parser = Parser(INPUT_FILE)
    parser.parse()
    while True:
        graph = parser.next_graph()
        if not graph:
            break

        
        def fitness_function(solution, solution_idx):
            fitness = graph.max_fitness()
            for vertice, adjacent_vertices in graph.adjacency_list.items():
                for adjacent_vertice in adjacent_vertices:
                    if solution[vertice] == solution[adjacent_vertice]:
                        fitness -= 1
            return fitness

        ga_instance = pygad.GA(num_generations=1000,
                               num_parents_mating=2,
                               fitness_func=fitness_function,
                               sol_per_pop=30,
                               num_genes=len(graph.adjacency_list),
                               gene_type=int,
                               init_range_low=0.05,
                               init_range_high=graph.maximum_degree + 1,
                               mutation_probability=0.1,
                               mutation_by_replacement=True,
                               stop_criteria=f"reach_{graph.max_fitness()}")
        ga_instance.run()
        solution, solution_fitness, solution_idx = ga_instance.best_solution()
        print(f"Real chromatic number: {graph.chromatic_number}")
        print(f"Searched for chromatic number: {graph.maximum_degree + 1}")
        print(f"Theoretical fitness: {graph.max_fitness()}")
        print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
        print("Index of the best solution : {solution_idx}".format(solution_idx=solution_idx))
        ga_instance.plot_fitness()

        break