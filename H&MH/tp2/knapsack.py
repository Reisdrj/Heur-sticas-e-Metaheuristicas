from copy import deepcopy
import random
import math
from tqdm import tqdm
import sys


def read_input(filename):
    with open(filename, "r") as file:
        length, weight = [int(i) for i in file.readline().strip().split()]
        items = []
        for _ in range(0, length):
            items.append([int(i) for i in file.readline().split()])
    return items, weight

def greedy_solution(items, max_weight):

        solution = [0] * len(items)
        solution_weight = 0
        solution_value = 0
        sorted_items = sorted(items, key=lambda x: x[0], reverse=True)
        for item in sorted_items:
            if (solution_weight + item[1]) < max_weight:
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

    # Neighbourhood of fliping all idxs
    def get_neighbours_1flip(self, solution):
        neighbours = []
        solution_value = self.get_solution_value(solution)
        for i in range(0, len(solution)):
            auxiliar = solution[:]
            auxiliar[i] = self.flip(auxiliar[i])
            weight = self.get_solution_weight(auxiliar)
            value = self.get_solution_value(auxiliar)
            if weight <= self.max_weight:
                if value > solution_value:
                    neighbours.append((auxiliar, weight, value))


        return neighbours
    
    # Random k-flips neighbourhood
    def get_neighbours_kflip(self, solution, k=4):
        neighbours = []
        solution_value = self.get_solution_value(solution)
        for i in range(0, len(solution)):
            idxs = [random.randint(0, len(solution)-1) for _ in range(k)]
            auxiliar = solution[:]
            for idx in idxs:
                auxiliar[idx] = self.flip(auxiliar[idx])
            weight = self.get_solution_weight(auxiliar)
            value = self.get_solution_value(auxiliar)
            if weight <= self.max_weight:
                if value > solution_value:
                    neighbours.append((auxiliar, weight, value))
        return neighbours
    
    def get_best_neighbour(self, neighbours):
        best_neighbour = []
        best_value = 0
        for neighbour in neighbours:
            if neighbour[2] > best_value and neighbour[1] <= self.max_weight:
                best_value = neighbour[2]
                best_neighbour = neighbour[0][:]

        return best_neighbour, best_value
    
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
    
    def local_search(self, initial_solution):
        solution = initial_solution[:]
        solution_value = self.get_solution_value(solution)
        neighbours = self.get_neighbours_1flip(solution)

        contador = 0

        while len(neighbours) > 0:

            best_neighbour, best_value = self.get_best_neighbour(neighbours)
            
            if best_value > solution_value:
                solution_value = best_value
                solution = best_neighbour[:]

            neighbours = self.get_neighbours_1flip(solution)
            contador += 1

        return solution, solution_value
    
    def local_search_vns(self, initial_solution, vmax, k):
        solution = initial_solution[:]
        solution_value = self.get_solution_value(solution)
        neighbours = vmax[k](solution)

        contador = 0

        while contador < 2:

            best_neighbour, best_value = self.get_best_neighbour(neighbours)
            
            if best_value > solution_value:
                solution_value = best_value
                solution = best_neighbour[:]

            neighbours = vmax[k](solution)
            contador += 1

        return solution, solution_value
    
    def shake(self, solution, d):
        aux = solution[:]
        for _ in range(d):
            random_index = random.randint(0, len(solution)-1)
            aux[random_index] = self.flip(aux[random_index])

        return aux

    def ils(self, max_iterations=30):
        initial_solution, _, _ = self.get_initial_solution()
        current_solution, current_value = self.local_search(initial_solution)

        d = 1
        iterations = 0

        while iterations < max_iterations:
            iterations += 1
            shaken_solution = self.shake(current_solution, d)
            aux_search_solution, aux_search_value = self.local_search(shaken_solution)
            shaken_search_solution, shaken_search_value = aux_search_solution[:], aux_search_value
            shaken_search_weight = self.get_solution_weight(shaken_search_solution)
            if shaken_search_value > current_value and shaken_search_weight <= self.max_weight:
                current_solution = shaken_search_solution[:]
                current_value = shaken_search_value
                iterations = 0
                d = 1
            else:
                d += 1

        current_value = self.get_solution_value(current_solution)

        return current_solution, current_value
    
    def greedy_construct(self):
        solution = []
        total_value = 0
        total_weight = 0
        candidate_items = deepcopy(self.items)

        while candidate_items:
            lc = [] 
            lrc = []
            
            for item in candidate_items:
                if item[1] + total_weight <= self.max_weight:
                    lc.append(item)

            if not lc:
                break

            size = max(1, int(math.ceil(len(lc) * 0.2)))

            lrc = lc[:size]

            selected_item = random.choice(lrc)
            
            solution.append(selected_item)
            total_value += selected_item[0]
            total_weight += selected_item[1]

            candidate_items.remove(selected_item)

        return solution, total_value


    def grasp(self, max_iterations=1000):
        best_solution = []
        best_value = -sys.maxsize # Get the minimum value

        iterations = 0
        while iterations < max_iterations:
            solution, total_value = self.greedy_construct()

            best_neighbour, best_neighbour_value = self.local_search(solution)

            if best_neighbour_value > total_value:
                total_value = best_neighbour_value
                solution = best_neighbour

            if total_value > best_value:
                best_value = total_value
                best_solution = solution

            iterations += 1
            
        return best_solution, best_value
    
    def change_neighbourhood(self, solution, neighbour, k):
        k += 1
        melhora = 0
        solution_value = self.get_solution_value(solution)
        neighbour_value = self.get_solution_value(neighbour)
        neighbour_cost = self.get_solution_weight(neighbour)
        best_solution = solution[:]
        if neighbour_value > solution_value and neighbour_cost < self.max_weight:
            best_solution = neighbour[:]
            melhora = 1
        return best_solution, k, melhora


    def vns(self, max_iterations = 1000):
        solution, _, _ = self.get_initial_solution()

        vmax = [self.get_neighbours_1flip, self.get_neighbours_kflip]

        iterations = 0
        while iterations <  max_iterations: # Número de iterções sem melhora
            k = 1
            while k < len(vmax): # Passar pelas vizinhanças
                shaken_solution = self.shake(solution, k)
                neighbour, _ = self.local_search_vns(shaken_solution, vmax, k)
                solution, k, melhora = self.change_neighbourhood(solution, neighbour, k)
                if melhora: iterations = 0
            iterations += 1

        return solution, self.get_solution_value(solution)
