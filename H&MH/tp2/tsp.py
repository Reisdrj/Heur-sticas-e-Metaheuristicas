import math
import random
import itertools
import sys
from copy import deepcopy

class TSP:
    def __init__(self, cities):
        self.cities = cities
        self.num_cities = len(cities)
        self.distances = self.calculate_distances()

    def calculate_distances(self):
        distances = [[0] * self.num_cities for _ in range(self.num_cities)]
        for i in range(self.num_cities):
            for j in range(self.num_cities):
                if i == j: distances[i][j] = sys.float_info.max
                else: distances[i][j] = self.euclidean_distance(self.cities[i], self.cities[j])
        return distances

    def euclidean_distance(self, city1, city2):
        return math.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)
    
    def initial_solution(self):
        return random.sample(range(self.num_cities), self.num_cities)

    def greedy_solution(self):
        solution = []
        visited = []

        i = random.randint(0, len(self.cities)-1)

        for _ in range(0, len(self.cities)):
            min_value = sys.float_info.max
            index = 0
            for j in range(0, len(self.cities)-1):
                if self.distances[i][j] < min_value and j not in visited:
                    min_value = self.distances[i][j]
                    index = j
            solution.append(index)
            visited.append(index)
            i = index

        return solution

    def random_neighbour(self, path):
        new_path = path[:]
        index1, index2 = random.sample(range(self.num_cities), 2)
        new_path[index1], new_path[index2] = new_path[index2], new_path[index1]
        return new_path

    def total_distance(self, path):
        total = 0
        for i in range(self.num_cities):
            total += self.distances[path[i]][path[(i + 1) % self.num_cities]]
        return total
    
    # Sequencial 2 Swap
    def get_neighbours_s2swap(self, solution):
        neighbours = []
        solution_Cost = self.total_distance(solution)
        aux_distance = 0
        for i in range(0, len(solution) - 1):
            neighbour = solution[:]
            neighbour[i], neighbour[i + 1] = neighbour[i + 1], neighbour[i]
            aux_distance = self.total_distance(neighbour)
            if aux_distance < solution_Cost: neighbours.append([neighbour, aux_distance])
        return neighbours
    
    # Random 2 Swap
    def get_neighbours_r2swap(self, solution):
        neighbours = []
        solution_cost = self.total_distance(solution)
        aux_distance = 0
        for i in range(0, len(solution) - 1):
            index = random.randint(0, self.num_cities-2)
            neighbour = solution[:]
            neighbour[index], neighbour[index + 1] = neighbour[index + 1], neighbour[index]
            aux_distance = self.total_distance(neighbour)
            if aux_distance < solution_cost: neighbours.append([neighbour, aux_distance])
        return neighbours
    
    # Shift solution element
    def get_neighbours_3shift(self, solution):
        neighbours = []
        solution_cost = self.total_distance(solution)
        aux_distance = 0
        for i in range(0, len(solution)):
            neighbour = solution[:]
            element = neighbour.pop(i)
            index = (i + 3) % len(neighbour)
            neighbour.insert(index, element)
            aux_distance = self.total_distance(neighbour)
            if aux_distance < solution_cost: neighbours.append([neighbour, aux_distance])
        return neighbours

    
    def best_neighbour(self, neighbours):

        best_neighbour = []
        best_value = sys.float_info.max

        for neighbour in neighbours:
                if neighbour[1] < best_value:
                    best_value = neighbour[1]
                    best_neighbour = neighbour[0][:]
                
        return best_neighbour, best_value


    def local_search(self, initial_solution):
        solution = initial_solution[:]
        solution_cost = self.total_distance(solution)
        neighbours = self.get_neighbours_s2swap(solution)

        contador = 0

        while contador < 2:

            best_neighbour, best_cost = self.best_neighbour(neighbours)

            if best_cost < solution_cost:
                solution_cost = best_cost
                solution = best_neighbour[:]
                contador = 0
            else: 
                contador += 1
            neighbours = self.get_neighbours_s2swap(solution)


        return solution, solution_cost
    
    def local_search_vns(self, initial_solution, vmax, k):
        solution = initial_solution[:]
        solution_cost = self.total_distance(solution)
        neighbours = vmax[k](solution)

        contador = 0

        while contador < 2:

            best_neighbour, best_cost = self.best_neighbour(neighbours)

            if best_cost < solution_cost:
                solution_cost = best_cost
                solution = best_neighbour[:]
                contador = 0
            else: 
                contador += 1
            
            neighbours = vmax[k](solution)


        return solution, solution_cost
    
    def greedy_construct(self):
        solution = []
        visited = set()
        index = 0
        distances = deepcopy(self.distances)
        
        for _ in range(len(self.cities)):
            lc = []
            lrc = []

            for j in range(len(distances[index])):
                if j not in visited:
                    lc.append((distances[index][j], j))

            lc.sort()

            size = max(1, int(math.ceil(len(lc) * 0.2)))

            lrc = lc[:size]

            if len(lrc) > 0:
                choice = random.choice(lrc)[1]
            else:
                return solution
            
            solution.append(choice)
            visited.add(choice)
            index = choice

        return solution

    def grasp(self, max_iterations=100):
        best_path = []
        best_distance = sys.float_info.max

        iterations = 0
        while iterations < max_iterations:
            solution = self.greedy_construct()
            solution_distance = self.total_distance(solution)

            best_neighbour, best_neighbour_distance = self.local_search(solution)

            if best_neighbour_distance < solution_distance:
                solution_distance = best_neighbour_distance
                solution = best_neighbour

            if solution_distance < best_distance:
                best_distance = solution_distance
                best_path = solution

            iterations += 1

        return best_path, best_distance

    
    def shake(self, solution, d):
        for _ in range(d):
            solution = self.random_neighbour(solution)
        return solution

    
    def ils(self, max_iterations=15):
        initial_solution = self.greedy_solution()
        current_solution, current_cost = self.local_search(initial_solution)

        d = 1
        iterations = 0

        while iterations < max_iterations:
            iterations += 1
            shaken_solution = self.shake(current_solution, d)
            shaken_search_solution, shaken_search_cost = self.local_search(
                shaken_solution
            )
            if shaken_search_cost < current_cost:
                current_solution = shaken_search_solution[:]
                current_cost = shaken_search_cost
                iterations = 0
                d = 1
            else:
                d += 1


        return current_solution, current_cost
    
    def change_neighbourhood(self, solution, neighbour, k):
        k += 1
        melhora = 0
        solution_cost = self.total_distance(solution)
        neighbour_cost = self.total_distance(neighbour)
        best_solution = solution[:]
        if neighbour_cost < solution_cost:
            best_solution = neighbour[:]
        return best_solution, k, melhora


    def vns(self, max_iterations = 1000):
        solution = self.initial_solution()
        
        vmax = [self.get_neighbours_s2swap, self.get_neighbours_r2swap, self.get_neighbours_3shift]

        iterations = 0
        while iterations <  max_iterations: # Número de iterções sem melhora
            k = 1
            while k < len(vmax): # Passar pelas vizinhanças
                shaken_solution = self.shake(solution, k)
                neighbour, _ = self.local_search_vns(shaken_solution, vmax, k)
                solution, k, melhora = self.change_neighbourhood(solution, neighbour, k)
                if melhora: iterations = 0
            iterations += 1

        return solution, self.total_distance(solution)
    


def read_cities_from_file(filename):
    cities = []
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split()
            x = int(parts[1])
            y = int(parts[2])
            cities.append((x, y))
    return cities
