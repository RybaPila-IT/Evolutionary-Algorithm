from game import Game
from network import Network
import evolutionary_algorithm as evol

if __name__ == '__main__':
    # Network random machine initialize
    Network.set_seed(1)
    game = Game()

    # Some population testing and evaluation.
    # I found an individual which obtained score equal to 664.
    # On my machine this program calculates in around 45s.
    # population = [Network([5, 1]) for i in range(500)]
    # best = None
    # b_score = 0
    #
    # for idx, brain in enumerate(population):
    #
    #     score = game.play(brain=brain, graphical=False)
    #
    #     if score > b_score:
    #         b_score = score
    #         best = brain
    # population = 50,mut = 0.1, cross = 0.2, rounds= 100, elite = 5
    population = evol.initialize(50)

    best_network = evol.evolve(game.play, population, 1.0, 0.4, 500)
    # print('Your score is: {} for brain nr: {}'.format(score, idx + 1))
    #game.play()
    print('Your score: {}'.format(game.play(brain=best_network, graphical=True)))
