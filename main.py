# Author: Julia Skoneczna
import tests

if __name__ == '__main__':

    tests.test_iterations(start_iterations=100, iterations_step=200,
                          population_size=50)

    tests.test_mutation_strength(number_of_tests=[0.5, 2.5, 5.0, 7.5, 13.5])
    tests.test_crossover(iterations=400, population_size=20, mutation_strength=2.5,
                         start_crossover_probability=0.1, crossover_probability_step=0.3)
    tests.test_population_size(iterations=400, start_population_size=20, population_size_step=10,
                               mutation_strength=2.5, crossover_probability=0.1)
