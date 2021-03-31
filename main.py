from game import Game
from network import Network

if __name__ == '__main__':
    # Network random machine initialize
    Network.set_seed(1)
    game = Game()

    # Some population testing and evaluation.
    # I found an individual which obtained score equal to 664.
    # On my machine this program calculates in around 45s.
    population = [Network([5, 1]) for i in range(500)]
    best = None
    b_score = 0

    for idx, brain in enumerate(population):

        score = game.play(brain=brain, graphical=False)

        if score > b_score:
            b_score = score
            best = brain

        print('Your score is: {} for brain nr: {}'.format(score, idx + 1))

    game.play(brain=best, graphical=True)
