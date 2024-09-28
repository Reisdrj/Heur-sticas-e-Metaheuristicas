import math
import random
import itertools
import sys
from copy import deepcopy

def has_duplicates(lst):
    return any(lst.count(item) > 1 for item in lst)

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
    
    def get_neighbours(self, solution):
        neighbours = []
        aux_distance = 0
        for i in range(0, len(solution) - 1):
            neighbour = solution[:]
            neighbour[i], neighbour[i + 1] = neighbour[i + 1], neighbour[i]
            aux_distance = self.total_distance(neighbour)
            neighbours.append([neighbour, aux_distance])
        return neighbours

    def greedy_construct(self):
        solution = []
        solution_cost = 0
        visited = []
        index = 0
        distances = deepcopy(self.distances[:])
        for _ in range(0, len(self.cities)):
            lc = []
            lrc = []
            choice = 0

            # Build LRC (List of Restricted Candidates)
            aux = distances[index][:]

            # Determine the size of the LRC
            size = int(math.ceil(len(distances[index]) * 0.2))
            if size < 1: size = 1

            # Create LC for the actual possibilities
            for j in range(0, len(distances[index])):
                position = distances[index].index(distances[index][j])
                if position not in visited:
                    lc.append(distances[index][j])

            # Create the LRC with the closest candidates
            lrc = sorted(lc)[:size]

            # Randomly select a city from the LRC
            if len(lrc) != 0: random_pos = random.randint(0, (len(lrc) - 1))
            else: 
                for item in solution:
                    if item not in self.cities:
                        solution.append(item)
                        return solution
            choice = lrc[random_pos]
            index = aux.index(choice)

            # Add the selected city to the solution
            solution.append(index)
            visited.append(index)

        return solution

    def grasp(self, max_iterations):
        best_path = []
        best_distance = sys.float_info.max

        iterations = 0
        while iterations < max_iterations:
            solution = self.greedy_construct()
            solution_distance = self.total_distance(solution)

            neighbours = self.get_neighbours(solution)

            # get best neighbour
            aux = solution_distance
            index = 0
            for i in range(0, len(neighbours)):
                if neighbours[i][1] < aux:
                    aux = neighbours[i][1]
                    index = i

            best_neighbour = deepcopy(neighbours[index][0])
            best_neighbour_distance = neighbours[index][1]

            if best_neighbour_distance < solution_distance:
                solution_distance = best_neighbour_distance
                solution = deepcopy(best_neighbour)

            if solution_distance < best_distance:
                best_distance = solution_distance
                best_path = deepcopy(solution)

            iterations += 1

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
    best_path, best_distance = tsp.grasp(10)

    print(f'Best Path: {len(best_path)}')
    print(f'Best Distance: {best_distance}')

    import collections
    print([item for item, count in collections.Counter(best_path).items() if count > 1])


if __name__ == '__main__':
    main()
