import math
import random
import itertools

class TSP:
    def __init__(self, cities):
        self.cities = cities
        self.num_cities = len(cities)
        self.distances = self.calculate_distances()

    def calculate_distances(self):
        distances = [[0] * self.num_cities for _ in range(self.num_cities)]
        for i in range(self.num_cities):
            for j in range(self.num_cities):
                distances[i][j] = self.euclidean_distance(self.cities[i], self.cities[j])
        return distances

    def euclidean_distance(self, city1, city2):
        return math.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)
    
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
        #print(f'{total}\n')
        return total

    def acceptance_probability(self, current_distance, new_distance, temperature):
        if new_distance < current_distance:
            return 1.0
        return math.exp((current_distance - new_distance) / temperature)

    def simulated_annealing(self, initial_temperature=1000, cooling_rate=0.99, stopping_temperature=0.001, max_iterations=100):
        current_path = self.initial_solution()
        best_path = current_path[:]
        current_distance = self.total_distance(current_path)
        best_distance = current_distance

        temperature = initial_temperature
        iteration = 0

        while temperature > stopping_temperature and iteration < max_iterations:
            neighbour_path = self.random_neighbour(current_path)
            neighbour_distance = self.total_distance(neighbour_path)

            if self.acceptance_probability(current_distance, neighbour_distance, temperature) > random.random():
                current_path = neighbour_path
                current_distance = neighbour_distance

                if current_distance < best_distance:
                    best_path = current_path[:]
                    best_distance = current_distance

            temperature *= cooling_rate
            iteration += 1

        return best_path, best_distance


def read_cities_from_file(filename):
    cities = []
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split()
            x = int(parts[1])
            y = int(parts[2])
            cities.append((x, y))
    return cities


def main():
    # Example usage with cities read from file
    cities = read_cities_from_file('tsp_51.txt')
    #print(cities)
    tsp = TSP(cities)

    # Solve TSP using simulated annealing
    best_path, best_distance = tsp.simulated_annealing()

    print(f'Best Path: {best_path}')
    print(f'Best Distance: {best_distance}')


if __name__ == '__main__':
    main()
