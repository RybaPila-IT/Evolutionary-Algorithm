# Author: Julia Skoneczna
import matplotlib.pyplot as plt
import os
from game import Game
from network import Network
import evolutionary_algorithm as evol


def test(figure_number, population_size, mutation_strength, crossover_probability, max_iterations,
         chart_name):
    best_score_averages = []
    average_individual_averages = []
    for seed in range(1, 26):
        # Network random machine initialize
        Network.set_seed(seed)
        print('Seed: ' + str(seed))
        game = Game()

        results = []
        population = evol.initialize(population_size)
        best_network = evol.evolve(game.play, population, mutation_strength, crossover_probability,
                                   max_iterations, results)
        best_scores = [el[0] for el in results]
        average_scores = [el[1] for el in results]
        best_scores_average = sum(best_scores) / max_iterations
        average_individual_average = sum(average_scores) / max_iterations
        # print('Result: ' + str(best_scores_average))
        best_score_averages.append(best_scores_average)
        average_individual_averages.append(average_individual_average)
    result = sum(best_score_averages) / 25
    average_individual_result = sum(average_individual_averages) / 25
    final_result = (result, average_individual_result)
    print('Result: ' + str(final_result))
    return final_result


def test_iterations(start_iterations=10, iterations_step=2, number_of_tests=3,
                    population_size=10, mutation_strength=5, crossover_probability=0.5):
    current_figure = 1
    current_iterations = start_iterations
    results = []
    # tests depending on the number of iterations
    for _ in range(0, number_of_tests):
        results.append(test(current_figure, population_size, mutation_strength,
                            crossover_probability, current_iterations, 'iterations_test'))
        current_figure += 1
        current_iterations += iterations_step
    print('Results for iteration number test: ' + str(results))


def test_population_size(iterations=500, number_of_tests=3,
                         start_population_size=10, population_size_step=30,
                         mutation_strength=5, crossover_probability=0.5):
    current_figure = 1
    current_population_size = start_population_size
    results = []
    # tests depending on population size
    for _ in range(0, number_of_tests):
        results.append(test(current_figure, current_population_size, mutation_strength, crossover_probability,
                            iterations, 'population_size_test'))
        current_figure += 1
        current_population_size += population_size_step
    print('Results for population size test: ' + str(results))


def test_mutation_strength(number_of_tests, iterations=400, population_size=20,
                           crossover_probability=0.5):
    current_figure = 1
    results = []
    # tests depending on mutation strength
    for t in number_of_tests:
        results.append(test(current_figure, population_size, t, crossover_probability,
                            iterations, 'mutation_strength_test'))
        current_figure += 1

    print('Results for mutation strength test: ' + str(results))


def test_crossover(iterations=500, number_of_tests=3, population_size=50, mutation_strength=5,
                   start_crossover_probability=0.5, crossover_probability_step=0.1):
    current_figure = 1
    current_crossover_probability = start_crossover_probability
    results = []
    # tests depending on crossover probability
    for _ in range(0, number_of_tests):
        results.append(test(current_figure, population_size, mutation_strength, current_crossover_probability,
                            iterations, 'crossover_test'))
        current_figure += 1
        current_crossover_probability += crossover_probability_step
        if current_crossover_probability > 1.0:
            break
    print('Results for crossover probability test: ' + str(results))
