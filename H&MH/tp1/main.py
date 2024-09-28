import itertools
import numpy as np
from copy import deepcopy
from knapsack import Knapsack
import knapsack as ks
import tsp as tsp
from tsp import TSP
import sys
import random


def knapsack_solve(method, input_file):
    items, weight = ks.read_input(input_file)
    sol, cost, value = ks.greedy_solution_knapsack(items, weight)
    knapsack_instance = Knapsack(
        max_iterations=20,
        items=items,
        initial_solution=sol,
        initial_cost=cost,
        initial_value=value,
        max_weight=weight,
    )

    if method.lower().strip() == "tabusearch":
        tabu_solution = knapsack_instance.tabu_search()
        return tabu_solution

    elif method.lower().strip() == "simulated_annealing":
        sm_solution = knapsack_instance.simulated_annealing()
        return sm_solution


def tsp_solve(method, input_file):
    cities = tsp.read_cities_from_file(input_file)
    tsp_instance = TSP(cities)
    if method.lower().strip() == "tabusearch":
        tabu_solution = tsp_instance.tabu_search()
        return tabu_solution

    elif method.lower().strip() == "simulated_annealing":
        sm_solution = tsp_instance.simulated_annealing()
        return sm_solution


def main():

    # Reading args
    problem = sys.argv[1]
    method = sys.argv[2]
    input_file = sys.argv[3]

    problem_methods = {
        "knapsack": {
            "tabusearch": lambda: knapsack_solve(method, input_file),
            "simulated_annealing": lambda: knapsack_solve(method, input_file),
        },
        "tsp": {
            "tabusearch": lambda: tsp_solve(method, input_file),
            "simulated_annealing": lambda: tsp_solve(method, input_file),
        },
    }

    r = problem_methods[problem][method]()
    print(f"Best Solution: {r}\n" f"Problem: {problem}\n" f"Method: {method}")


main()
