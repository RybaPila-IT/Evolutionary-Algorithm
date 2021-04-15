import matplotlib.pyplot as plt
import os
from game import Game
from network import Network
import evolutionary_algorithm as evol


def test(figure_number, population_size, mutation_strength, crossover_probability, max_iterations,
         chart_name):
    # Network random machine initialize
    Network.set_seed(1)
    game = Game()

    results = []
    population = evol.initialize(population_size)
    best_network = evol.evolve(game.play, population, mutation_strength, crossover_probability,
                               max_iterations, results)
    iterations = [i for i in range(0, max_iterations)]
    plt.clf()
    # print('Your score: {}'.format(game.play(brain=best_network, graphical=True)))
    best_scores = [el[0] for el in results]
    average_scores = [el[1] for el in results]
    best = plt.scatter(iterations, best_scores, s=5, label='najlepszy wynik')
    plt.xlabel('Iteracja')
    plt.ylabel('Osiągnięty wynik')
    average = plt.scatter(iterations, average_scores, s=5, label='średni wynik')
    plt.legend(handles=[best, average], bbox_to_anchor=(0, 1, 1, 0), loc="lower left", mode="expand", ncol=2)
    current_directory = os.path.dirname(__file__)
    filename = chart_name + str(figure_number) + '.png'
    plt.savefig(current_directory + '/charts/' + filename)


def test_iterations(start_iterations=10, iterations_step=2, number_of_tests=3,
                    population_size=10, mutation_strength=5, crossover_probability=0.5):
    current_figure = 1
    current_iterations = start_iterations
    # tests depending on the number of iterations
    for _ in range(0, number_of_tests):
        test(current_figure, population_size, mutation_strength, crossover_probability, current_iterations,
             'iterations_test')
        current_figure += 1
        current_iterations += iterations_step


def test_population_size(iterations=500, number_of_tests=3,
                         start_population_size=10, population_size_step=30,
                         mutation_strength=5, crossover_probability=0.5):
    current_figure = 1
    current_population_size = start_population_size
    # tests depending on the population size
    for _ in range(0, number_of_tests):
        test(current_figure, current_population_size, mutation_strength, crossover_probability,
             iterations, 'population_size_test')
        current_figure += 1
        current_population_size += population_size_step


def test_mutation_strength(iterations=500, number_of_tests=3, population_size=50,
                           start_mutation_strength=5, mutation_strength_step=3,
                           crossover_probability=0.5):
    current_figure = 1
    current_mutation_strength = start_mutation_strength
    # tests depending on the mutation strength
    for _ in range(0, number_of_tests):
        test(current_figure, population_size, current_mutation_strength, crossover_probability,
             iterations, 'mutation_strength_test')
        current_figure += 1
        current_mutation_strength += mutation_strength_step


def test_crossover(iterations=500, number_of_tests=3, population_size=50, mutation_strength=5,
                   start_crossover_probability=0.5, crossover_probability_step=0.1):
    current_figure = 1
    current_crossover_probability = start_crossover_probability
    # tests depending on the crossover probability
    for _ in range(0, number_of_tests):
        test(current_figure, population_size, mutation_strength, current_crossover_probability,
             iterations, 'crossover_test')
        current_figure += 1
        current_crossover_probability += crossover_probability_step
        if current_crossover_probability > 1.0:
            break