import pygad
from Parser import Parser
import random
import time
import sys

INPUT_FILE = "/home/filip/Work/FER/6_semestar/zavrsni_rad/sources/graphs/200_249.txt"


def print_graph_score(chromatic_number, k_found, starting_number, num_vertices, num_edges):
    print("--------------------------------------------------")
    print(f"Real chromatic number: {chromatic_number}")
    print(f"Found chromatic number: {k_found}")
    print(f"Started from: {starting_number}")
    print(f"Number of vertices: {num_vertices}")
    print(f"Number of edges: {num_edges}")


def print_total_score(scores, total):
    print("##################################################################################################")
    print(f"[CONCLUSION]")
    print(f"[CORRECT]       correct      / total            = {scores[0]} / {total} ({round(scores[0]*100/total, 2)}%)")
    print(f"[ERROR == 1]    off_by_one   / total            = {scores[1]} / {total} ({round(scores[1]*100/total, 2)}%)")
    print(f"[ERROR == 2]    off_by_two   / total            = {scores[2]} / {total} ({round(scores[2]*100/total, 2)}%)")
    print(f"[ERROR == 3]    off_by_three / total            = {scores[3]} / {total} ({round(scores[3]*100/total, 2)}%)")
    print(f"[ERROR >= 4]    off_by_four_or_more / total     = {scores[4]} / {total} ({round(scores[4]*100/total, 2)}%)")



if __name__ == "__main__":
    random.seed(time.time())

    if len(sys.argv) == 2:
        input_file = sys.argv[1]
    else:
        input_file = INPUT_FILE

    parser = Parser(input_file)
    parser.parse()
    # keeps track of how many graphs were off by how much from the real chr num
    scores = {i: 0 for i in range(5)}
    total = 0

    while True:
        graph = parser.next_graph()
        if not graph:
            break
        if not graph.chromatic_number:
            continue

        def fitness_func(solution, solution_idx):
            # this is actually the cost function
            fitness = 0
            for vertice, adjacent_vertices in graph.adjacency_list.items():
                for adjacent_vertice in adjacent_vertices:
                    if solution[vertice] == solution[adjacent_vertice]:
                        fitness -= 1
            return fitness

        
        # 91% success rate on 200-249 vertices graphs 
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
        lowest_found = None
        total += 1
        while True:
            if k <= graph.chromatic_number - 1:
                print_graph_score(graph.chromatic_number, lowest_found, graph.maximum_degree + 1,
                                    graph.number_of_vertices, graph.number_of_edges)
                scores[0] += 1
                break

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
                                # save_best_solutions=True,
                                crossover_type="single_point",
                                mutation_type=mutation_func,
                                parent_selection_type="sss",
                                keep_elitism=1,
                                stop_criteria=f"reach_0")
            ga_instance.run()
            solution, solution_fitness, solution_idx = ga_instance.best_solution()

            if solution_fitness < 0:
                print_graph_score(graph.chromatic_number, lowest_found, graph.maximum_degree + 1,
                                    graph.number_of_vertices, graph.number_of_edges)
                if lowest_found - graph.chromatic_number == 1:
                    scores[1] += 1
                elif lowest_found - graph.chromatic_number == 2:
                    scores[2] += 1
                elif lowest_found - graph.chromatic_number == 3:
                    scores[3] += 1
                else:
                    scores[4] += 1
                break
            lowest_found = k
            k -= 1

    print_total_score(scores, total)