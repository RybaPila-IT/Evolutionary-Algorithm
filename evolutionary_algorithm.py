import random
import numpy as np
from network import Network

TOURNAMENT_SIZE = 2
ELITE_SIZE = 3


def evolve(objective_function, initial_population, mutation_strength, crossover_probability, iterations):
    population_size = len(initial_population)
    if population_size == 0:
        return initial_population
    population = [(individual, objective_function(brain=individual, graphical=False))
                  for individual in initial_population]
    population = sorted(population, key=lambda el: el[1], reverse=True)
    current_iteration = 0
    print('hi')
    current_best_score = population[0][1]
    current_best_individual = population[0][0]
    best_individual = current_best_individual
    best_score = current_best_score

    while current_iteration <= iterations:
        print('iteration {}'.format(current_iteration))
        new_population = [el for el in population[0:ELITE_SIZE]]  # elite individuals - ELITE_BEST first individuals
        for i in range(population_size):
            parent1 = elite_tournament(population, objective_function)
            parent2 = elite_tournament(population, objective_function)
            probability = random.random()
            crossed_population = []
            if probability < crossover_probability:
                new_individual = Network.crossover(parent1, parent2)
                crossed_population.append(new_individual)
            else:
                crossed_population.append(parent1)

        crossed_population_size = len(crossed_population)
        for i in range(crossed_population_size):
            Network.mutate(crossed_population[i], mutation_strength)
            new_population.append((crossed_population[i], objective_function(brain=crossed_population[i],
                                                                             graphical=False)))

        new_population = sorted(new_population, key=lambda el: el[1], reverse=True)
        current_best_score = new_population[0][1]
        if current_best_score > best_score:
            best_score = current_best_score
            best_individual = new_population[0][0]

        for index, el in enumerate(new_population[1:-ELITE_SIZE]):
            print(index)
            del new_population[index]

        population = new_population
        current_iteration += 1

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


def elite_tournament(sorted_population, objective_function):
    # population is sorted descending by objective function value
    individuals = [individual[0] for individual in sorted_population]
    scores = [individual[1] for individual in sorted_population]
    population_size = len(sorted_population)
    probabilities = count_pick_probability(individuals)
    print(scores)

    current_probability = random.random()
    chosen_individuals = [np.random.randint(0, population_size) for _ in range(TOURNAMENT_SIZE)]

    for index, chosen in enumerate(chosen_individuals):
        while probabilities[index] > current_probability:
            current_probability = random.random()
            chosen_individuals[index] = np.random.randint(0, population_size)

    first_index = chosen_individuals[0]
    second_index = chosen_individuals[1]
    if scores[first_index] < scores[second_index]:
        # print('second')
        return individuals[second_index]
    else:
        # print('first')
        return individuals[first_index]
