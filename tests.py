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
    # print('Your score: {}'.format(game.play(brain=best_network, graphical=True)))
    best_scores = [el[0] for el in results]
    average_scores = [el[1] for el in results]
    plt.scatter(iterations, best_scores, s=20)
    plt.xlabel('Iteracja')
    plt.ylabel('Osiągnięty wynik')

    plt.scatter(iterations, average_scores, s=20)
    plt.legend(['najlepszy wynik', 'średni wynik'], loc='lower right')
    current_directory = os.path.dirname(__file__)
    filename = chart_name + str(figure_number) + '.png'
    plt.savefig(current_directory + '/charts/' + filename)


def test_iterations(start_iterations, iterations_step, number_of_tests,
                    population_size, mutation_strength, crossover_probability):
    current_figure = 1
    current_iterations = start_iterations
    # tests depending on the number of iterations
    for _ in range(0, number_of_tests):
        test(current_figure, population_size, mutation_strength, crossover_probability, current_iterations,
             'iterations_test')
        current_figure += 1
        current_iterations += iterations_step
