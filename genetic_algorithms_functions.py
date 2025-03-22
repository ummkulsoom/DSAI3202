import numpy as np

def calculate_fitness(route, distance_matrix):
    """
    Calculates the total distance traveled by the car.

    Parameters:
        - route (list): Order of nodes visited in the route.
        - distance_matrix (numpy.ndarray): Matrix of distances between nodes.

    Returns:
        - float: Negative total distance traveled (negative because we minimize distance).
        - Returns a scaled penalty if the route is infeasible.
    """
    total_distance = 0

    for i in range(len(route) - 1):
        node1, node2 = route[i], route[i + 1]
        distance = distance_matrix[node1][node2]

        # Adaptive penalty for infeasible routes
        if distance == 100000:
            total_distance += np.median(distance_matrix[distance_matrix < 100000]) * 2  # Softer penalty
        else:
            total_distance += distance

    return -total_distance  # Return negative value for GA optimization


def select_in_tournament(population, scores, number_tournaments=12, tournament_size=8):
    selected = []
    for _ in range(number_tournaments):
        tournament_size = min(tournament_size, len(population))  # Ensure valid size
        idx = np.random.choice(len(population), tournament_size, replace=False)

        best_idx = idx[np.argmin(scores[idx])]  # Select the best based on fitness
        selected.append(population[best_idx])
    return selected



def order_crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(np.random.choice(range(size), 2, replace=False))

    offspring = [-1] * size
    offspring[start:end] = parent1[start:end]

    remaining_values = [x for x in parent2 if x not in offspring]
    
    # Ensure all missing values are added correctly
    missing_nodes = list(set(range(size)) - set(offspring))
    np.random.shuffle(missing_nodes)
    
    idx = 0
    for i in range(size):
        if offspring[i] == -1:
            offspring[i] = missing_nodes[idx]
            idx += 1
    
    return offspring


def mutate(route, mutation_rate=0.2):
    """
    Mutation operator: swaps two cities instead of introducing duplicates.
    """
    if np.random.rand() < mutation_rate:
        i, j = np.random.choice(len(route), 2, replace=False)
        route[i], route[j] = route[j], route[i]  # Swap instead of replacing
    
    return route



def generate_unique_population(population_size, num_nodes):
    """
    Generate a unique population of individuals for a genetic algorithm.

    Each individual in the population represents a route in a graph, where the first node is fixed (0) and the 
    remaining nodes are a permutation of the other nodes in the graph. This function ensures that all individuals
    in the population are unique.

    Parameters:
        - population_size (int): The desired size of the population.
        - num_nodes (int): The number of nodes in the graph, including the starting node.

    Returns:
        - list of lists: A list of unique individuals, where each individual is represented as a list of node indices.
    """
    population = set()
    while len(population) < population_size:
        individual = [0] + list(np.random.permutation(np.arange(1, num_nodes)))
        population.add(tuple(individual))
    return [list(ind) for ind in population]