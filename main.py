from game import Game
from network import Network

if __name__ == '__main__':
    # Network random machine initialize
    Network.set_seed(1)
    game = Game()
    brain = Network([5, 1])
    brain1 = Network([5, 1])
    print('Your score is: {}'.format(game.play(brain=brain, graphical=True)))
    print('Your score is: {}'.format(game.play(brain=brain, graphical=False)))
    print('Your score is: {}'.format(game.play(brain=brain1, graphical=True)))
    print('Your score is: {}'.format(game.play(brain=brain1, graphical=False)))
