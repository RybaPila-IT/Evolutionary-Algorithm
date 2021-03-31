import random
import pygame
import numpy as np

# Game constants
FPS = 60
DISPLAY_W = 1200
DISPLAY_H = 600
SPIKES_A = 12
LAMBDA = 1.0
TITLE = 'Geometry-Run'

# Color constants
WHITE = (255, 255, 255)
MAGENTA = (255, 0, 255)
GREY = (122, 122, 122)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Cube constants
CUBE_BEG_X = 100
CUBE_BEG_Y = 511
CUBE_DIM = 70
CUBE_Y_SPEED = 25

# Lines constants
L_BEG_X = 0
L1_BEG_Y = 9
L1_BOUND = 19
L2_BEG_Y = 590
L2_BOUND = 581
L_THICK = 20

# Obstacle constants and coordinates
UPPER_SPIKE = [(DISPLAY_W, L1_BOUND),
               (DISPLAY_W + 20, L1_BOUND + 50),
               (DISPLAY_W + 40, L1_BOUND)]
LOWER_SPIKE = [(DISPLAY_W, L2_BOUND),
               (DISPLAY_W + 20, L2_BOUND - 50),
               (DISPLAY_W + 40, L2_BOUND)]
SPIKE_SPEED = -10


class Game:
    """Class representing model used for evaluation of individuals.

    Game class, as the name suggests, implements a game. It is an easy and boring variation
    of common mobile game called Geometry Dash.
    It`s GI was implemented using pygame module so one should download and install
    it.

    Game class supports non-graphical gameplay for speeding-up the process of judging
    which takes place while evolutionary algorithm is running."""
    class Cube:

        def __init__(self):
            self.x_ = CUBE_BEG_X
            self.y_ = CUBE_BEG_Y
            self.d_ = CUBE_DIM
            self.j_ = False
            self.y_s_ = 0

        def jump(self):
            if not self.j_:
                self.j_ = True
                self.y_s_ = - CUBE_Y_SPEED if self.y_ + self.d_ == L2_BOUND else CUBE_Y_SPEED

        def move(self):
            if self.y_s_ != 0:
                self.y_ += self.y_s_
                self.y_ = min([self.y_, L2_BOUND - self.d_])
                self.y_ = max([self.y_, L1_BOUND])

            if self.y_ == L2_BOUND - self.d_ or self.y_ == L1_BOUND:
                self.j_ = False

        def intersects(self, points):
            if self.x_ >= points[1][0] or self.x_ + self.d_ <= points[0][0]:
                return False
            if self.y_ >= points[0][1] or self.y_ + self.d_ <= points[1][1]:
                return False

            return True

    # --------------------------- END OF CUBE --------------------------- #

    class Spike:

        def __init__(self, points):
            self.p_ = points.copy()
            self.s_ = SPIKE_SPEED

        def move(self):
            for i in range(len(self.p_)):
                lst = list(self.p_[i])
                lst[0] += self.s_
                self.p_[i] = tuple(lst)

        def valid(self):
            return self.p_[len(self.p_) - 1][0] > 0

        def approx_with_rect(self):
            x1 = self.p_[0][0] + 4
            y1 = max([self.p_[0][1], self.p_[1][1]])
            x2 = self.p_[2][0] - 4
            y2 = min([self.p_[2][1], self.p_[1][1]])

            return [(x1, y1), (x2, y2)]

    # --------------------------- END OF SPIKE --------------------------- #

    def __init__(self, seed=1):
        self.running_ = True
        self.cube_ = self.Cube()
        self.spikes_ = []
        self.spikes_a_ = 0
        self.time_ = 0
        self.score_ = 0
        self.seed_ = seed

    def _generate_spikes(self):
        if self.spikes_a_ < SPIKES_A and self.time_ <= 0:
            self.spikes_.append(self.Spike(UPPER_SPIKE) if random.random() >= 0.5 else self.Spike(LOWER_SPIKE))
            self.spikes_a_ += 1
            self.time_ = max([random.expovariate(LAMBDA) * FPS, 4])

    def _check_game_over(self):
        for spike in self.spikes_:
            if self.cube_.intersects(spike.approx_with_rect()):
                self.running_ = False

    def _handle_user_events(self, player):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running_ = False
            if player:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.cube_.jump()

    def _network_decision(self, brain):
        if brain is not None:
            if brain.predict(self._get_game_info()):
                self.cube_.jump()

    def _move_assets(self):
        self.cube_.move()
        for spike in self.spikes_:
            spike.move()
            if not spike.valid():
                self.spikes_.remove(spike)
                self.spikes_a_ -= 1

    def _draw_assets(self, window):
        if window is not None:
            window.fill(WHITE)
            for spike in self.spikes_:
                pygame.draw.polygon(window, RED, spike.p_)
            pygame.draw.rect(window, BLUE, (self.cube_.x_, self.cube_.y_, self.cube_.d_, self.cube_.d_))
            pygame.draw.line(window, GREY, (L_BEG_X, L1_BEG_Y), (DISPLAY_W, L1_BEG_Y), L_THICK)
            pygame.draw.line(window, GREY, (L_BEG_X, L2_BEG_Y), (DISPLAY_W, L2_BEG_Y), L_THICK)
            font = pygame.font.SysFont('arial', 50)
            text = font.render(str(self.score_), True, MAGENTA)
            window.blit(text, (0, L1_BOUND))

    def _update(self, window_clock):
        self.time_ -= 1
        self.score_ += 1
        if window_clock is not None:
            pygame.display.update()
            window_clock.tick(FPS)

    def _get_game_info(self):
        """Function responsible for communication with an individual.

        :returns normalized list of data where:
                [0] - nearest lower spike dist to x1 of the cube;
                [1] - nearest lower spike dist to x2 of the cube;
                [2] - nearest upper spike dist to x1 of the cube;
                [3] - nearest upper spike dist to x2 of the cube;
                [4] - cube y coordinate"""
        info = np.array([1, 1, 1, 1, self.cube_.y_ / DISPLAY_H]).astype(dtype=np.float32)
        cube_x2 = self.cube_.x_ + self.cube_.d_
        cube_x1 = self.cube_.x_

        for spike in self.spikes_:
            if spike.p_[0][0] >= cube_x2:
                if spike.p_[1][1] == UPPER_SPIKE[1][1] and info[3] == 1:
                    info[3] = (spike.p_[0][0] - cube_x2) / DISPLAY_W
                elif info[1] == 1:
                    info[1] = (spike.p_[0][0] - cube_x2) / DISPLAY_W
            if spike.p_[0][0] >= cube_x1:
                if spike.p_[1][1] == UPPER_SPIKE[1][1] and info[2] == 1:
                    info[2] = (spike.p_[0][0] - cube_x1) / DISPLAY_W
                elif info[0] == 1:
                    info[0] = (spike.p_[0][0] - cube_x1) / DISPLAY_W

        return info

    def play(self, brain=None, graphical=True):
        """Main function used for gameplay and model evaluation.

        Function play enables using game 'black-box' evaluating the subject.
        Result of the evaluation is the distance in x-direction travelled by the cube.

        In order to estimate 'brain' in fast-non-graphical-mode one should pass the individual together with
        'graphical' set to False. If one would like to see how individual plays (just because one
        may be curious) 'graphical' parameter should be set to True.

        In order to play a game by oneself 'brain' value should be left as default together
        with 'graphical' set to True (also default value).

        :parameter brain - an individual which will be evaluated on a model (which is a game).
        :parameter graphical - information whether show game graphical interface or not.

        :returns score accomplished by a player or an individual.
         """
        # Pre-gameplay necessary initialization
        random.seed(self.seed_)
        pygame.init()
        pygame.display.set_caption(TITLE)
        window = pygame.display.set_mode((DISPLAY_W, DISPLAY_H)) if graphical else None
        window_clock = pygame.time.Clock() if graphical else None

        # Clearing game insides.
        self.running_ = True
        self.score_ = 0
        self.time_ = 0
        self.spikes_.clear()
        self.spikes_a_ = 0
        self.cube_ = self.Cube()

        # Game loop
        while self.running_:
            self._handle_user_events(player=(brain is None))
            self._network_decision(brain)
            self._generate_spikes()
            self._move_assets()
            self._check_game_over()
            self._draw_assets(window)
            self._update(window_clock)

        pygame.quit()

        return self.score_
