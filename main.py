from game import Game
from network import Network
import evolutionary_algorithm as evol

if __name__ == '__main__':
    # Network random machine initialize
    Network.set_seed(1)
    game = Game()

    population = evol.initialize(20)

    best_network = evol.evolve(game.play, population, 10, 0.4, 500)

    print('Your score: {}'.format(game.play(brain=best_network, graphical=True)))
