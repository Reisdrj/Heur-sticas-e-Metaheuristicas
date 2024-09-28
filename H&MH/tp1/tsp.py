import math
import random
import itertools


def read_cities_from_file(filename):
    cities = []
    with open(filename, "r") as f:
        for line in f:
            parts = line.strip().split()
            x = int(parts[1])
            y = int(parts[2])
            cities.append((x, y))
    return cities


class TSP:
    def __init__(self, cities):
        self.cities = cities
        self.num_cities = len(cities)
        self.distances = self.calculate_distances()

    def calculate_distances(self):
        distances = [[0] * self.num_cities for _ in range(self.num_cities)]
        for i in range(self.num_cities):
            for j in range(self.num_cities):
                distances[i][j] = distances[j][i] = self.euclidean_distance(
                    self.cities[i], self.cities[j]
                )
        return distances

    def euclidean_distance(self, city1, city2):
        return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

    def initial_solution(self):
        return random.sample(range(self.num_cities), self.num_cities)

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

    def acceptance_probability(self, current_distance, new_distance, temperature):
        if new_distance < current_distance:
            return 1.0
        return math.exp((current_distance - new_distance) / temperature)

    def simulated_annealing(
        self,
        initial_temperature=10000,
        cooling_rate=0.999,
        stopping_temperature=0.001,
        max_iterations=200,
    ):
        current_path = self.initial_solution()
        best_path = current_path[:]
        current_distance = self.total_distance(current_path)
        best_distance = current_distance

        temperature = initial_temperature
        iteration = 0

        while temperature > stopping_temperature:
            iteration = 0
            while iteration < max_iterations:
                neighbour_path = self.random_neighbour(current_path)
                neighbour_distance = self.total_distance(neighbour_path)

                if neighbour_distance < current_distance:
                    current_distance = neighbour_distance
                    current_path = neighbour_path[:]

                    if current_distance < best_distance:
                        best_distance = current_distance
                        best_path = current_path[:]

                else:
                    if (
                        self.acceptance_probability(
                            current_distance, neighbour_distance, temperature
                        )
                        > random.random()
                    ):
                        current_path = neighbour_path
                        current_distance = neighbour_distance

                        if current_distance < best_distance:
                            best_path = current_path[:]
                            best_distance = current_distance

                iteration += 1
            temperature *= cooling_rate

        return best_path, best_distance

    def get_tabu_neighbours(self, solution):
        neighbours = []
        aux_distance = 0
        for i in range(0, len(solution) - 1):
            neighbour = solution[:]
            neighbour[i], neighbour[i + 1] = neighbour[i + 1], neighbour[i]
            aux_distance = self.total_distance(neighbour)
            neighbours.append([neighbour, aux_distance])
        return neighbours

    def tabu_search(self, max_iterations=1000):

        tabu_list = []
        tabu_size = 10

        solution = self.initial_solution()
        solution_distance = self.total_distance(solution)
        s_best = solution[:]
        d_best = solution_distance
        iterations = 0

        while iterations < max_iterations:
            iterations = iterations + 1
            neighbours = self.get_tabu_neighbours(solution)

            # get best neighbour
            aux = solution_distance
            index = 0
            for i in range(0, len(neighbours)):
                if neighbours[i][1] < aux and i not in tabu_list:
                    aux = neighbours[i][1]
                    index = i

            if len(tabu_list) == tabu_size:
                tabu_list.pop(0)
                tabu_list.append(index)
                solution = neighbours[index][0][:]
                solution_distance = neighbours[index][1]
            else:
                tabu_list.append(index)
                solution = neighbours[index][0][:]
                solution_distance = neighbours[index][1]

            if solution_distance < d_best:
                s_best = solution[:]
                d_best = solution_distance

        return s_best, d_best


def read_cities_from_file(filename):
    cities = []
    with open(filename, "r") as f:
        for line in f:
            parts = line.strip().split()
            x = int(parts[1])
            y = int(parts[2])
            cities.append((x, y))
    return cities
