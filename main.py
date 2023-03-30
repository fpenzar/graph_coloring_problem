import pygad
from Parser import Parser
import random

INPUT_FILE = "/home/filip/Work/FER/6_semestar/zavrsni_rad/sources/graphs/200_249.txt"



if __name__ == "__main__":
    parser = Parser(INPUT_FILE)
    parser.parse()
    correct = 0
    total = 0

    while True:
        graph = parser.next_graph()
        if not graph:
            break

        def fitness_func(solution, solution_idx):
            # this is actually the cost function
            fitness = 0
            for vertice, adjacent_vertices in graph.adjacency_list.items():
                for adjacent_vertice in adjacent_vertices:
                    if solution[vertice] == solution[adjacent_vertice]:
                        fitness -= 1
            return fitness
        
        def parent_selection_func(fitness_value, number_of_parents, ga_instance: pygad.GA):
            ...
        
        def mutation_func(offspring, ga_instance: pygad.GA):
            if ga_instance.best_solutions_fitness[0] >= -4:
                # more random mutation so as not to get stuck in local optima
                for chromosome in offspring:
                    for vertex, color in enumerate(chromosome):
                        # check if the current vertex shares a color with its neighbour
                        new_color_needed = False
                        for adjacent_vertice in graph.adjacency_list[vertex]:
                            if color == chromosome[adjacent_vertice]:
                                new_color_needed = True
                                break
                        if not new_color_needed:
                            continue
                        new_color = random.randint(ga_instance.init_range_low, ga_instance.init_range_high)
                        chromosome[vertex] = new_color
            else:
                # more precise mutation if the best fitness is not great
                for chromosome in offspring:
                    for vertex, color in enumerate(chromosome):
                        # check if the current vertex shares a color with its neighbour
                        new_color_needed = False
                        adjacent_colors = set()
                        for adjacent_vertice in graph.adjacency_list[vertex]:
                            adjacent_colors.add(chromosome[adjacent_vertice])
                            if color == chromosome[adjacent_vertice]:
                                new_color_needed = True
                        if not new_color_needed:
                            continue
                        # if number of different adjacent colors is the same as the total number of colors -> choose a random color
                        if len(adjacent_colors) == ga_instance.init_range_high:
                            new_color = random.randint(ga_instance.init_range_low, ga_instance.init_range_high)
                        # otherwise choose a color that does not match any of the adjacent colors
                        else:
                            available_colors = []
                            for possible_color in range(ga_instance.init_range_low, ga_instance.init_range_high + 1):
                                if possible_color not in adjacent_colors:
                                    available_colors.append(possible_color)
                            new_color = random.choice(available_colors)
                        chromosome[vertex] = new_color
            return offspring


        # starting value for number of colors is the max_degree + 1
        k = graph.maximum_degree + 1
        calculate_next = True
        while calculate_next:
            ga_instance = pygad.GA(num_generations=1000,
                                num_parents_mating=2,
                                fitness_func=fitness_func,
                                sol_per_pop=50,
                                num_genes=len(graph.adjacency_list),
                                gene_type=int,
                                init_range_low=1,
                                init_range_high=k,
                                # mutation_probability=0.2,
                                # mutation_by_replacement=True,
                                save_best_solutions=True,
                                crossover_type="single_point",
                                mutation_type=mutation_func,
                                parent_selection_type="sss",
                                keep_elitism=1,
                                stop_criteria=f"reach_0") # if the fitness reaches 0 -> stop (correct coloring)
            ga_instance.run()
            solution, solution_fitness, solution_idx = ga_instance.best_solution()
            # ga_instance.plot_fitness()
            if solution_fitness == 0:
                # we have found a valid coloring
                k -= 1
            else:
                calculate_next = False
                print(f"Real chromatic number: {graph.chromatic_number}")
                print(f"Found chromatic number: {k + 1}")
                print(f"Started from: {graph.maximum_degree + 1}")
                print(f"Number of vertices: {graph.number_of_vertices}")
                print(f"Number of edges: {graph.number_of_edges}")
                # ga_instance.plot_fitness()
                print("########################")
                if not graph.chromatic_number:
                    continue
                if k == graph.chromatic_number:
                    correct += 1
                total += 1
        # break
    print(f"[CONCLUSION] correct / total =  {correct} / {total} ({round(correct * 100 / total, 2)}%)")