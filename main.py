# Author: Julia Skoneczna
# from game import Game
# from network import Network
# import evolutionary_algorithm as evol
import tests

if __name__ == '__main__':

    tests.test_iterations(start_iterations=10, iterations_step=20,
                          population_size=10)

    # tests.test_population_size(iterations=500, start_population_size=50)
    #
    # tests.test_mutation_strength(population_size=80)
    #
    # tests.test_crossover()
