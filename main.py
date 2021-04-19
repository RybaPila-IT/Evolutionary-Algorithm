# Author: Julia Skoneczna
import tests

if __name__ == '__main__':
    # Section responsible for algorithm parameters estimation (really time-consuming)
    tests.test_iterations(start_iterations=100, iterations_step=200,
                          population_size=20)

    tests.test_mutation_strength(number_of_tests=[0.5, 2.5, 5.0, 7.5, 13.5])
    tests.test_crossover(iterations=400, population_size=20, mutation_strength=2.5,
                         start_crossover_probability=0.1, crossover_probability_step=0.3)
    tests.test_population_size(iterations=400, start_population_size=20, population_size_step=10,
                               mutation_strength=2.5, crossover_probability=0.1)
    # Section responsible for single individual training
    from game import Game
    from network import Network, load_network
    from evolutionary_algorithm import initialize, evolve

    game = Game(seed=1)
    Network.set_seed(1)
    population = initialize(30, [5, 10, 1])
    results = []
    best_individual = evolve(game.play, population, 3.5, 0.1, 400, results, verbose=True)
    best_individual.save_network('Net.json')
    best_individual = load_network('Net.json')
    game.play(brain=best_individual, graphical=True)
