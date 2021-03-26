from game import Game, DISPLAY_W, DISPLAY_H


if __name__ == '__main__':
    game = Game(DISPLAY_W, DISPLAY_H)
    print('Your score is: {}'.format(game.play()))
