import random
import numpy as np
from network import Network

TOURNAMENT_SIZE = 2
ELITE_SIZE = 3


def evolve(objective_function, initial_population, mutation_strength, crossover_probability, iterations):
    population = initial_population
    population_size = len(population)
    current_iteration = 0
    current_scores = sorted([objective_function(el) for el in initial_population], key=objective_function, reverse=True)
    current_best_score = max(current_scores)
    current_best_individual = population[np.argmax(population)]
    # elite = [current_scores[i] for i in range(0, ELITE_SIZE)]
    best_individual = current_best_individual
    best_score = current_best_score

    while current_iteration <= iterations:
        new_population = []
        for i in range(population_size):
            parent1 = elite_tournament(population, objective_function)
            parent2 = elite_tournament(population, objective_function)
            probability = random.random()
            if probability < crossover_probability:
                children = [Network.crossover(parent1, parent2) for i in range(0, 2)]
                new_population.append(children)
            else:
                new_population.append([parent1, parent2])

        for individual in range(ELITE_SIZE, population_size):
            Network.mutate(population[individual], mutation_strength)

        current_scores = sorted([objective_function(el) for el in new_population])
        current_best_score = max(current_scores)
        if current_best_score > best_score:
            best_score = current_best_score
            best_individual = new_population[np.argmax(current_scores)]

        for i in current_scores[:-ELITE_SIZE]:
            del population[i]

        iterations += 1

    return best_individual


def initialize(population_size):
    return [Network([5, 1]) for i in range(population_size)]


def count_pick_probability(ranked_population):
    population_size = len(ranked_population)
    probabilities = []
    for index, individual in enumerate(ranked_population, start=1):
        individual_probability = (1 / population_size ** TOURNAMENT_SIZE) * \
                                 ((population_size - index + 1) ** TOURNAMENT_SIZE -
                                  (population_size - index) ** TOURNAMENT_SIZE)
        probabilities.append(individual_probability)
    return probabilities


def elite_tournament(population, objective_function):
    population_size = len(population)
    population = sorted(population, key=objective_function, reverse=True) # TODO: zastanowić się, czy po prostu nie uznać, że przekazujemy posortowane wg wyniku nierosnąco
    probabilities = count_pick_probability(population)

    # for i in range(population_size):
    current_probability = random.random()
    chosen_individuals = [np.random.randint(0, population_size) for _ in range(TOURNAMENT_SIZE)]

    for index, chosen in enumerate(chosen_individuals):
        while probabilities[index] > current_probability:
            current_probability = random.random()
            chosen_individuals[index] = np.random.randint(0, population_size)

    first = chosen_individuals[0]
    second = chosen_individuals[1]
    if objective_function(first) < objective_function(second):
        return second
    else:
        return first


def temp_func(x):
    return x


elite_tournament([2, 3, 4, 5, 6, 7, 8, 2, 1], temp_func)
