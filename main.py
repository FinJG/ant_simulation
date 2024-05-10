import sys

import pygame

import assets


class Game:
    def __init__(self):
        pygame.init()

        self.FPS = 60
        self.SCREEN_WIDTH = 896
        self.SCREEN_HEIGHT = 896
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.clock = pygame.time.Clock()
        self.dt = 1

        # map settings
        self.grid_size = 128
        self.tile_size = self.SCREEN_HEIGHT / self.grid_size

        # self.ants = [Ant(self, 64, 64) for _ in range(50)]
        self.ant_nest = assets.AntNest(self, 64, 64)

        self.running = False

    def new_game(self):
        pass

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_SPACE:
                    self.running = not self.running

    def update(self):

        for ant in self.ant_nest.ants:
            ant.update()

        self.ant_nest.update()

        self.dt = self.clock.tick(self.FPS)
        pygame.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.screen.fill((235, 235, 235))

        for ant in self.ant_nest.ants:
            ant.draw()

        self.ant_nest.draw()

        pygame.display.update()

    def run(self):
        while True:
            self.events()
            if self.running:
                self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
