from copy import deepcopy
import numpy as np
import random
import math
from tqdm import tqdm


def read_input(filename):
    with open(filename, "r") as file:
        length, weight = [int(i) for i in file.readline().strip().split()]
        items = []
        for _ in range(0, length):
            items.append([int(i) for i in file.readline().split()])
    return items, weight


def greedy_solution_knapsack(items, weight):

    solution = [0] * len(items)
    solution_weight = 0
    solution_value = 0
    sorted_items = sorted(items, key=lambda x: x[0], reverse=True)
    for item in sorted_items:
        if (solution_weight + item[1]) < weight:
            for i in range(0, len(items)):
                if item[0] == items[i][0] and item[1] == items[i][1]:
                    solution[i] = 1
                    solution_weight += item[1]
                    solution_value += item[0]
    return solution, solution_weight, solution_value


class Knapsack:

    def __init__(
        self,
        max_iterations,
        items,
        initial_solution,
        initial_cost,
        initial_value,
        max_weight,
    ):


        self.initial_solution = initial_solution[:]
        self.initial_cost = initial_cost
        self.initial_value = initial_value
        self.max_weight = max_weight
        self.max_iterations = max_iterations
        self.items = items
        self.knapsack_length = len(items)


    def flip(self, pos):
        if pos == 1:
            return 0
        else:
            return 1

    def get_neighbours(self, solution):
        neighbours = []
        for i in range(0, self.knapsack_length):
            auxiliar = deepcopy(solution)
            auxiliar[i] = self.flip(auxiliar[i])
            weight = self.get_solution_weight(auxiliar)
            value = 0

            # penality
            if weight > self.max_weight:
                for i in auxiliar:
                    if i == 1:
                        value -= 20 * (weight - self.max_weight)

            else:
                value = self.get_solution_value(auxiliar)
            neighbours.append((auxiliar, weight, value))

        return neighbours

    def get_solution_value(self, solution):
        value = 0
        for i in range(len(solution)):
            if solution[i] == 1:
                value += self.items[i][0]
        return value

    def get_solution_weight(self, solution):
        weight = 0
        for i in range(len(solution)):
            if solution[i] == 1:
                weight += self.items[i][1]
        return weight

    def get_initial_solution(self):
        solution = [0] * self.knapsack_length
        solution_weight = 0
        solution_value = 0
        while True:
            rand_int = random.randint(0, self.knapsack_length - 1)
            if (solution_weight + self.items[rand_int][1]) <= self.max_weight:
                solution[rand_int] = 1
                solution_weight += self.items[rand_int][1]
                solution_value += self.items[rand_int][0]
            else:
                break
        return solution, solution_weight, solution_value

    def tabu_search(self):

        tabu_list = []
        tabu_size = 2

        solution = self.initial_solution
        cost = self.initial_cost
        value = self.initial_value
        s_best = solution
        c_best = cost
        v_best = value
        iterations = 0

        while iterations < self.max_iterations:
            iterations = iterations + 1
            neighbours = self.get_neighbours(solution)

            # get best neighbour
            aux = value
            index = 0
            for i in range(0, len(neighbours)):
                if neighbours[i][2] > aux and i not in tabu_list:
                    aux = neighbours[i][2]
                    index = i

            if len(tabu_list) == tabu_size:
                tabu_list.pop(0)
                tabu_list.append(index)
                value = neighbours[index][2]
                solution = neighbours[index][0]
                cost = neighbours[index][1]
            else:
                tabu_list.append(index)
                value = neighbours[index][2]
                solution = neighbours[index][0]
                cost = neighbours[index][1]

            if value > v_best:
                s_best = solution
                v_best = value
                c_best = cost

        return s_best, c_best, v_best

    def acceptance_probability(self, current_value, neighbour_value, temperature):
        result = math.exp((neighbour_value - current_value) / temperature)
        result = round(result, 10)
        return result

    def simulated_annealing(
        self,
        initial_temperature=1000,
        cooling_rate=0.999,
        stopping_temperature=0.001,
        max_iterations=200,
    ):

        current_sol, current_weight, current_value = self.get_initial_solution()
        best_sol = current_sol[:]
        best_weight = current_weight
        best_value = current_value

        temperature = initial_temperature
        iteration = 0

        while temperature > stopping_temperature:
            while iteration < max_iterations:
                rand_int = random.randint(0, self.knapsack_length - 1)
                neighbour_path = current_sol[:]
                neighbour_path[rand_int] = self.flip(current_sol[rand_int])
                neighbour_weight = self.get_solution_weight(neighbour_path)
                neighbour_value = self.get_solution_value(neighbour_path)

                if neighbour_weight <= self.max_weight:
                    if neighbour_value > current_value:
                        current_sol = neighbour_path[:]
                        current_value = neighbour_value
                        current_weight = neighbour_weight

                        if neighbour_value > best_value:
                            best_value = neighbour_value
                            best_sol = neighbour_path[:]
                            best_weight = neighbour_weight
                    else:
                        acceptance = self.acceptance_probability(
                            current_value, neighbour_value, temperature
                        )
                        if acceptance > random.random():
                            current_sol = neighbour_path[:]
                            current_weight = neighbour_weight
                            current_value = neighbour_value

                iteration += 1

            temperature *= cooling_rate
            iteration = 0

        return best_sol, best_weight, best_value
