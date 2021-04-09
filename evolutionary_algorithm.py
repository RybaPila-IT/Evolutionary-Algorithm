import random
import numpy as np

TOURNAMENT_SIZE = 2


def evolve(objective_function, initial_population, mutation_strength, crossover_probability, iterations):
    print('test')


def count_pick_probability(ranked_population):
    population_size = len(ranked_population)
    probabilities = []
    for index, individual in enumerate(ranked_population, start=1):
        individual_probability = (1 / population_size ** TOURNAMENT_SIZE) * \
                                 ((population_size - index + 1) ** TOURNAMENT_SIZE -
                                  (population_size - index) ** TOURNAMENT_SIZE)
        probabilities.append(individual_probability)
    return probabilities


def tournament(population, objective_function):
    population_size = len(population)
    population = sorted(population, key=objective_function, reverse=True)
    new_population = []

    probabilities = count_pick_probability(population)
    for i in range(population_size):
        current_probability = random.random()
        chosen_individuals = [np.random.randint(0, population_size) for _ in range(TOURNAMENT_SIZE)]

        for index, chosen in enumerate(chosen_individuals):
            while probabilities[index] < current_probability:
                chosen = np.random.randint(0, population_size)

        first = chosen_individuals[0]
        second = chosen_individuals[1]

        if objective_function(first) < objective_function(second):
            new_population.append(second)
        else:
            new_population.append(first)

    return new_population


