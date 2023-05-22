import pygad
from Parser import Parser
import random
import time
import sys

INPUT_FILE = "./sources/graphs/single_graph.txt"


def print_graph_score(chromatic_number, k_found, starting_number, num_vertices, num_edges):
    print("--------------------------------------------------")
    print(f"Real chromatic number: {chromatic_number}")
    print(f"Found chromatic number: {k_found}")
    print(f"Number of colors started from: {starting_number}")
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


def run(graph, fitness_func, mutation_func, parent_selection_func, draw_colored_graph):
    k = graph.maximum_degree + 1
    lowest_found = float("inf")
    highest_not_chromatic = graph.chromatic_number - 1
    previous_solution = None
    k_found = True
    while True:
        # # the optimal solution has been found
        # if k <= graph.chromatic_number - 1:
        #     print_graph_score(graph.chromatic_number, lowest_found, graph.maximum_degree + 1,
        #                         graph.number_of_vertices, graph.number_of_edges)
        #     scores[0] += 1
        #     # TODO take a screenshot of a graph that it did not manage to color
        #     if draw_colored_graph:
        #         graph.draw(previous_solution)
        #     break

        if k == highest_not_chromatic:
            if draw_colored_graph:
                graph.draw(previous_solution)

            return lowest_found

        ga_instance = pygad.GA(num_generations=1000,
                            num_parents_mating=2,
                            fitness_func=fitness_func,
                            sol_per_pop=50,
                            num_genes=len(graph.adjacency_list),
                            gene_type=int,
                            init_range_low=1,
                            init_range_high=k,
                            mutation_probability=0.2,
                            crossover_type="single_point",
                            mutation_type=mutation_func,
                            parent_selection_type=parent_selection_func,
                            keep_elitism=1,
                            stop_criteria=f"reach_0")
        ga_instance.run()
        solution, solution_fitness, solution_idx = ga_instance.best_solution()
        k_found = (solution_fitness == 0)

        if k_found:
            lowest_found = k
            previous_solution = solution
        else:
            highest_not_chromatic = k
        if not k_found and lowest_found == float("inf"):
            return -1

        k = int((lowest_found + highest_not_chromatic) / 2)


        # if solution_fitness < 0:
        #     print_graph_score(graph.chromatic_number, lowest_found, graph.maximum_degree + 1,
        #                         graph.number_of_vertices, graph.number_of_edges)
        #     if lowest_found - graph.chromatic_number == 1:
        #         scores[1] += 1
        #     elif lowest_found - graph.chromatic_number == 2:
        #         scores[2] += 1
        #     elif lowest_found - graph.chromatic_number == 3:
        #         scores[3] += 1
        #     else:
        #         scores[4] += 1
        #     if draw_colored_graph:
        #         if previous_solution is not None:
        #             graph.draw(previous_solution)
        #         else:
        #             graph.draw(solution)
        #     break
        # previous_solution = solution
        # lowest_found = k
        # k -= 1


def genetic_search(input_file, draw_colored_graph):
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
        

        def mutation_func_random_change_on_bad_vertices(offspring, ga_instance: pygad.GA):
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
            return offspring
        

        def mutation_func_targeted_change_on_bad_vertices(offspring, ga_instance: pygad.GA):
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

        k_found = run(graph, fitness_func, mutation_func, "sss", draw_colored_graph)
        print(f"Found chromatic number: {k_found}, Real chromatic_number: {graph.chromatic_number}")
        # # starting value for number of colors is the max_degree + 1
        # k = graph.maximum_degree + 1
        # lowest_found = float("inf")
        # highest_not_k = graph.chromatic_number - 1
        # total += 1
        # previous_solution = None
        # k_found = True
        # while True:
        #     # the optimal solution has been found
        #     if k <= graph.chromatic_number - 1:
        #         print_graph_score(graph.chromatic_number, lowest_found, graph.maximum_degree + 1,
        #                             graph.number_of_vertices, graph.number_of_edges)
        #         scores[0] += 1
        #         # TODO take a screenshot of a graph that it did not manage to color
        #         if draw_colored_graph:
        #             graph.draw(previous_solution)
        #         break

        #     ga_instance = pygad.GA(num_generations=1000,
        #                         num_parents_mating=2,
        #                         fitness_func=fitness_func,
        #                         sol_per_pop=50,
        #                         num_genes=len(graph.adjacency_list),
        #                         gene_type=int,
        #                         init_range_low=1,
        #                         init_range_high=k,
        #                         # mutation_probability=0.2,
        #                         # mutation_by_replacement=True,
        #                         # save_best_solutions=True,
        #                         crossover_type="single_point",
        #                         mutation_type=mutation_func,
        #                         parent_selection_type="rank",
        #                         keep_elitism=1,
        #                         stop_criteria=f"reach_0")
        #     ga_instance.run()
        #     solution, solution_fitness, solution_idx = ga_instance.best_solution()

        #     if solution_fitness < 0:
        #         print_graph_score(graph.chromatic_number, lowest_found, graph.maximum_degree + 1,
        #                             graph.number_of_vertices, graph.number_of_edges)
        #         if lowest_found - graph.chromatic_number == 1:
        #             scores[1] += 1
        #         elif lowest_found - graph.chromatic_number == 2:
        #             scores[2] += 1
        #         elif lowest_found - graph.chromatic_number == 3:
        #             scores[3] += 1
        #         else:
        #             scores[4] += 1
        #         if draw_colored_graph:
        #             if previous_solution is not None:
        #                 graph.draw(previous_solution)
        #             else:
        #                 graph.draw(solution)
        #         break
        #     previous_solution = solution
        #     lowest_found = k
        #     k -= 1

    # print_total_score(scores, total)



if __name__ == "__main__":
    random.seed(time.time())

    if len(sys.argv) == 2:
        input_file = sys.argv[1]
        draw_colored_graph = False
    elif len(sys.argv) == 3:
        input_file = sys.argv[1]
        draw_colored_graph = (sys.argv[2].lower() == "true" or sys.argv[2].lower() == "t")
    else:
        print("[USAGE] python3 main.py <input_file> [<draw_solution>]")
        print("                        <input_file> - path to the file containing graphs. Must not be empty.")
        print("                        <draw_solution> - set to \"true\" or \"t\" if you wish the solution to be drawn. Optional.")
        exit(1)
    genetic_search(input_file, draw_colored_graph)