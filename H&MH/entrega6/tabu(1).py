import itertools
import numpy as np
from copy import deepcopy

def greedy_solution(items, weight):
    print(f"{items}\n")
    solution = []
    solution_weight = 0
    solution_value = 0
    sorted_items = sorted(items, key=lambda x: x[0])
    for item in sorted_items:
        if (solution_weight + item[1]) > weight:
            solution.append(0)
        else:
            solution.append(1)
            solution_weight += item[1]
            solution_value += item[0]
    return solution, solution_weight, solution_value

class Tabu:

    def __init__(self, max_iterations, items, initial_solution, initial_cost, initial_value, max_weight):
        self.initial_solution = initial_solution
        self.initial_cost = initial_cost
        self.initial_value = initial_value
        self.max_weight = max_weight
        self.max_iterations = max_iterations
        self.items = items
        self.knapsack_length = len(items)

    def get_solution_weight(self, solution):
        weight = 0
        for i in range(len(solution)):
            if solution[i] == 1:
                weight += self.items[i][0]
        return weight
    
    def get_solution_value(self, solution):
        value = 0
        for i in range(len(solution)):
            if solution[i] == 1:
                value += self.items[i][1]
        return value

    def get_initial_solution(self):
        prob = np.random.rand(self.knapsack_length)
        solution = [0 if element < 0.5 else 1 for element in prob]
        return solution
    
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

    def tabu_search(self):

        tabu_list = []
        tabu_size = 2
        solution = self.initial_solution
        cost = self.initial_cost
        value = self.initial_value
        s_best = self.initial_solution
        c_best = self.initial_cost
        v_best = self.initial_value
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

            if len(tabu_list) == 2:
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
    
def read_input():
    print("Lendo... \n")
    length, weight = [int(i) for i in input().split()]
    items = []
    for i in range(0, length):
        items.append([int(i) for i in input().split()])
    return items, weight
    

def main():

    items, weight = read_input()
    sol, cost, value = greedy_solution(items, weight)
    tabu = Tabu(max_iterations=200, items=items, initial_solution=sol, initial_cost=cost, initial_value=value, max_weight = weight)
    best_solution = tabu.tabu_search()
    print(f"\n\n{sol} {cost} {value}\n\n{best_solution}")

main()