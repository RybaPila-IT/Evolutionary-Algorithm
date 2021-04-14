import random
import numpy as np
from network import Network

TOURNAMENT_SIZE = 2
ELITE_SIZE = 2


def evolve(objective_function, initial_population, mutation_strength, crossover_probability, iterations):
    population_size = len(initial_population)
    if population_size == 0:
        return initial_population
    population = [(individual, objective_function(brain=individual, graphical=False))
                  for individual in initial_population]
    population = sorted(population, key=lambda el: el[1], reverse=True)
    current_iteration = 0
    current_best_score = population[0][1]
    current_best_individual = population[0][0]
    best_individual = current_best_individual
    best_score = current_best_score

    while current_iteration < iterations:
        print('iteration {}'.format(current_iteration + 1))
        # elite individuals - ELITE_SIZE first individuals
        new_population = [el for el in population[0:ELITE_SIZE]]
        crossed_individuals = []

        for i in range(population_size):
            parent1 = selection_tournament(population)
            parent2 = selection_tournament(population)
            probability = random.random()
            if probability < crossover_probability:
                new_individual = Network.crossover(parent1, parent2)
                crossed_individuals.append(new_individual)
            else:
                crossed_individuals.append(parent1)

        crossed_population_size = len(crossed_individuals)
        for i in range(crossed_population_size):
            new_individual = Network.mutate(crossed_individuals[i], mutation_strength)
            new_population.append((new_individual, objective_function(brain=new_individual,
                                                                      graphical=False)))

        new_population = sorted(new_population, key=lambda el: el[1], reverse=True)
        current_best_score = new_population[0][1]

        if current_best_score > best_score:
            best_score = current_best_score
            best_individual = new_population[0][0]

        new_population = new_population[:len(new_population) - ELITE_SIZE]
        population = new_population
        # debugging purposes
        # new_population_scores = [el[1] for el in new_population]
        # print(new_population_scores)
        best_individual_score = new_population[0][1]
        average_individual = count_average_individual(new_population)
        average_individual_score = objective_function(brain=average_individual, graphical=False)
        # debugging purposes
        print('best: ' + str(best_individual_score))
        print('average: ' + str(average_individual_score))
        current_iteration += 1

    return best_individual


def initialize(population_size):
    return [Network([5, 1]) for _ in range(population_size)]


def count_pick_probability(ranked_population):
    """
    Function counting probability of picking an individual for tournament in tournament selection.

    :parameter ranked_population - population sorted descending by rank according to objective function.

    :returns list of probabilities of getting picked for each individual in the population.
    """
    population_size = len(ranked_population)
    probabilities = []
    for index, individual in enumerate(ranked_population, start=1):
        individual_probability = (1 / population_size ** TOURNAMENT_SIZE) * \
                                 ((population_size - index + 1) ** TOURNAMENT_SIZE -
                                  (population_size - index) ** TOURNAMENT_SIZE)
        probabilities.append(individual_probability)
    return probabilities


def selection_tournament(sorted_population):
    # population is sorted descending by objective function value
    individuals = [individual[0] for individual in sorted_population]
    scores = [individual[1] for individual in sorted_population]
    population_size = len(sorted_population)
    probabilities = count_pick_probability(individuals)

    current_probability = random.random()
    chosen_individuals_indices = [np.random.randint(0, population_size) for _ in range(TOURNAMENT_SIZE)]

    for index, chosen in enumerate(chosen_individuals_indices):
        while probabilities[chosen] < current_probability:
            current_probability = random.random()
            chosen_individuals_indices[index] = np.random.randint(0, population_size)

    first_index = chosen_individuals_indices[0]
    second_index = chosen_individuals_indices[1]
    if scores[first_index] < scores[second_index]:
        return individuals[second_index]
    else:
        return individuals[first_index]


def count_average_individual(new_population):
    """
    Counts the 'average individual' for the population, i. e. an individual with weights and biases averaged
    over the entire population's weights and biases.

    :parameter new_population - list of population's individuals and their scores.

    :returns a Network object representing the 'average individual' for the population.
    """
    population_size = len(new_population)
    # we assume non-empty population
    individuals_sum = new_population[0][0]
    for index in range(1, len(new_population)):
        individuals_sum += new_population[index][0]
    return individuals_sum / population_size
