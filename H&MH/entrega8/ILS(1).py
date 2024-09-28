import math
import random
import sys

class TSP:
    def __init__(self, cities):
        self.cities = cities
        self.num_cities = len(cities)
        self.distances = self.calculate_distances()

    def greedy_solution(self):
        solution = []
        visited = []

        i = random.randint(0, len(self.cities))

        for _ in range(0, len(self.cities)):
            min_value = sys.float_info.max
            index = 0
            for j in range(0, len(self.cities)):
                if self.distances[i][j] < min_value and j not in visited:
                    min_value = self.distances[i][j]
                    index = j
            solution.append(index)
            visited.append(index)
            i = index

        return solution

    def calculate_distances(self):
        distances = [[0] * self.num_cities for _ in range(self.num_cities)]
        for i in range(self.num_cities):
            for j in range(self.num_cities):
                if i == j:
                    distances[i][j] = sys.float_info.max
                else:
                    distances[i][j] = self.euclidean_distance(
                        self.cities[i], self.cities[j]
                    )
        return distances

    def euclidean_distance(self, city1, city2):
        return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

    def initial_solution(self):
        return random.sample(range(self.num_cities), self.num_cities)

    def random_neighbour(self, path):
        new_path = path[:]
        index1, index2 = random.sample(range(0, self.num_cities), 2)
        new_path[index1], new_path[index2] = new_path[index2], new_path[index1]
        return new_path

    def total_distance(self, path):
        total = 0
        for i in range(self.num_cities):
            total += self.distances[path[i]][path[(i + 1) % self.num_cities]]
        return total

    def get_neighbours(self, solution):
        neighbours = []
        solution_Cost = self.total_distance(solution)
        aux_distance = 0
        for i in range(0, len(solution) - 1):
            neighbour = solution[:]
            neighbour[i], neighbour[i + 1] = neighbour[i + 1], neighbour[i]
            aux_distance = self.total_distance(neighbour)
            if aux_distance < solution_Cost: neighbours.append([neighbour, aux_distance])
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
        neighbours = self.get_neighbours(solution)

        contador = 0

        while len(neighbours) > 0:

            best_neighbour, best_cost = self.best_neighbour(neighbours)

            if best_cost < solution_cost:
                solution_cost = best_cost
                solution = best_neighbour[:]
                contador = 0

            neighbours = self.get_neighbours(solution)

            contador += 1

        return solution, solution_cost

    def shake(self, solution, d):
        for _ in range(d):
            solution = self.random_neighbour(solution)
        return solution

    def ils(self, max_iteration=20):
        initial_solution = self.greedy_solution()
        current_solution, current_cost = self.local_search(initial_solution)

        d = 3
        iterations = 0

        while iterations < max_iteration:
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


def read_cities_from_file(filename):
    cities = []
    with open(filename, "r") as f:
        for line in f:
            parts = line.strip().split()
            x = int(parts[1])
            y = int(parts[2])
            cities.append((x, y))
    return cities


def main():
    # Example usage with cities read from file
    cities = read_cities_from_file("tsp_51.txt")
    # print(cities)
    tsp = TSP(cities)

    best_path, best_distance = tsp.ils()

    print(f"Best Path: {best_path}")
    print(f"Best Distance: {best_distance}")


if __name__ == "__main__":
    main()
