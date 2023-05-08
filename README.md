# Solving graph coloring problem using evolutionary algorithm

This project is a BSc Thesis for the Computer Science Program at Faculty of Electrical Engineering and Computing, University of Zagreb.

## Installing required packages

To install the required packages, run the following command inside a python virtual environment:

```
$ pip install -r requirements.txt
```

## Running the program

To run the program, use the following syntax:
```
$ python3 main.py <input_file> [<draw_solution>]
                  <input_file> - path to the file containing graphs. Must not be empty.
                  <draw_solution> - set to "true" or "t" if you wish the solution to be drawn. Optional.
```
### Example

```
$ python3 main.py ./sources/graphs/single_graph.txt true
```

## Goals
The goals of this project are to:
* define the graph coloring problem with the minimum number of colors
* describe an evolutionary algorithm adapted to solving the specific problem of graph coloring
* programmatically realize a program system for solving the graph coloring problem with an
evolutionary algorithm with a simple user interface using freely available program libraries
* test the performance of the evolutionary algorithm on several graph coloring problems
* experimentally determine the set of parameters of the genetic algorithm that randomly
selects genetic operators
* attach the original program texts and cite the literature used with the paper