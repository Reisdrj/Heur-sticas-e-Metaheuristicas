from knapsack import Knapsack
import knapsack as ks
import tsp as tsp
from tsp import TSP
import sys


def knapsack_solve(method, input_file):
    items, weight = ks.read_input(input_file)
    sol, cost, value = ks.greedy_solution(items, weight)
    knapsack_instance = Knapsack(
        max_iterations=20,
        items=items,
        initial_solution=sol,
        initial_cost=cost,
        initial_value=value,
        max_weight=weight,
    )

    if method.strip() == "GRASP":
        tabu_solution = knapsack_instance.grasp()
        return tabu_solution

    elif method.strip() == "ILS":
        sm_solution = knapsack_instance.ils()
        return sm_solution
    
    elif method.strip() == "VNS":
        vns_solution = knapsack_instance.vns()
        return vns_solution


def tsp_solve(method, input_file):
    cities = tsp.read_cities_from_file(input_file)
    tsp_instance = TSP(cities)
    
    if method.strip() == "GRASP":
        grasp_solution = tsp_instance.grasp()
        return grasp_solution

    elif method.strip() == "ILS":
        ils_solution = tsp_instance.ils()
        return ils_solution
    
    elif method.strip() == "VNS":
        vns_solution = tsp_instance.vns()
        return vns_solution



def main():

    # Reading args
    problem = sys.argv[1]
    method = sys.argv[2]
    input_file = sys.argv[3]

    problem_methods = {
        "tsp": {
            "GRASP": lambda: tsp_solve(method, input_file),
            "ILS": lambda: tsp_solve(method, input_file),
            "VNS": lambda: tsp_solve(method, input_file)
        },
        "knapsack": {
            "GRASP": lambda: knapsack_solve(method, input_file),
            "ILS": lambda: knapsack_solve(method, input_file),
            "VNS": lambda: knapsack_solve(method, input_file)
        }
    }

    r = problem_methods[problem][method]()
    print(f"Best Solution: {r}\n" f"Problem: {problem}\n" f"Method: {method}")


main()