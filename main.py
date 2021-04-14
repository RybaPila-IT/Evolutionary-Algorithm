# from game import Game
# from network import Network
# import evolutionary_algorithm as evol
import tests

if __name__ == '__main__':

    tests.test_iterations(start_iterations=100, iterations_step=200, number_of_tests=3,
                          population_size=50, mutation_strength=5, crossover_probability=0.5)

    # print('Your score: {}'.format(game.play(brain=best_network, graphical=True)))
