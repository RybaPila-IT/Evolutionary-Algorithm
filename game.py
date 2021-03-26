import random
import pygame

# Game constants
FPS = 60
DISPLAY_W = 1200
DISPLAY_H = 600
SPIKES_A = 12
LAMBDA = 1.0
TITLE = 'Geometry-Run'

# Color constants
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREY = (122, 122, 122)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Cube constants
CUBE_BEG_X = 100
CUBE_BEG_Y = 511
CUBE_DIM = 70
CUBE_Y_SPEED = 20

# Lines constants
L_BEG_X = 0
L1_BEG_Y = 9
L1_BOUND = 19
L2_BEG_Y = 590
L2_BOUND = 581
L_THICK = 20

# Obstacle constants and coordinates
UPPER_SPIKE = [(DISPLAY_W, L1_BOUND), (DISPLAY_W + 20, L1_BOUND + 50), (DISPLAY_W + 40, L1_BOUND)]
LOWER_SPIKE = [(DISPLAY_W, L2_BOUND), (DISPLAY_W + 20, L2_BOUND - 50), (DISPLAY_W + 40, L2_BOUND)]
SPIKE_SPEED = -11


class Game:
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

    # -------------- END OF CUBE -------------- #

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

    # -------------- END OF SPIKE -------------- #

    def __init__(self, width, height, brain=None, seed=1):
        self.dw = width
        self.dh = height
        self.running = True
        self.cube = self.Cube()
        self.spikes = []
        self.spikes_a = 0
        self.time_ = 0
        self.brain = brain
        self.seed = seed

    def __generate_spikes(self):
        if self.spikes_a < SPIKES_A and self.time_ <= 0:
            self.spikes.append(self.Spike(UPPER_SPIKE) if random.random() >= 0.5 else self.Spike(LOWER_SPIKE))
            self.spikes_a += 1
            self.time_ = random.expovariate(LAMBDA) * FPS

    def __check_game_over(self):
        pass

    def __handle_events(self):
        for event in pygame.event.get():
            if self.brain is None:
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.cube.jump()

    def __move_assets(self):
        self.cube.move()
        for spike in self.spikes:
            spike.move()
            if not spike.valid():
                self.spikes.remove(spike)
                self.spikes_a -= 1

    def __draw_assets(self, window):

        window.fill(WHITE)
        for spike in self.spikes:
            pygame.draw.polygon(window, RED, spike.p_)
        pygame.draw.rect(window, BLUE, (self.cube.x_, self.cube.y_, self.cube.d_, self.cube.d_))
        pygame.draw.line(window, GREY, (L_BEG_X, L1_BEG_Y), (DISPLAY_W, L1_BEG_Y), L_THICK)
        pygame.draw.line(window, GREY, (L_BEG_X, L2_BEG_Y), (DISPLAY_W, L2_BEG_Y), L_THICK)

    def __update(self, window_clock):
        self.time_ -= 1
        pygame.display.update()
        window_clock.tick(FPS)

    def play(self):

        # Pre-gameplay necessary initialization
        pygame.init()
        random.seed(self.seed)

        pygame.display.set_caption(TITLE)
        window = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
        window_clock = pygame.time.Clock()

        self.running = True

        # Game loop
        while self.running:
            self.__handle_events()
            self.__generate_spikes()
            self.__move_assets()
            self.__draw_assets(window)
            self.__update(window_clock)

        pygame.quit()


if __name__ == '__main__':
    game = Game(DISPLAY_W, DISPLAY_H)
    game.play()
