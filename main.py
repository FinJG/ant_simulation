import sys
from random import randint

import pygame

# settings
SCREEN_WIDTH = 896
SCREEN_HEIGHT = 896

FPS = 120 #  float("inf")


class Ant:
    def __init__(self, game, x, y):
        self.game = game

        self.pos = pygame.Vector2(x, y)

        self.walking_direction = pygame.Vector2()

        self.pheromones = []
        self.total_steps = 0

        self.col = (randint(0, 255), randint(0, 255), randint(0, 255))

    def update(self):

        # chance to change x direction
        if randint(1, 32) == 1:
            self.walking_direction.x = randint(-1, 1)

        # chance to change y direction
        if randint(1, 32) == 1:
            self.walking_direction.y = randint(-1, 1)

        # chance to move the ant in its facing direction
        if randint(1, 8) == 1:
            if 0 <= (self.pos.x + self.walking_direction.x) * self.game.tile_size < SCREEN_WIDTH:
                if 0 <= (self.pos.y + self.walking_direction.y) * self.game.tile_size < SCREEN_WIDTH:
                    self.pos += self.walking_direction

                    self.total_steps += 1

                    # will leave a pheromone every N steps (1 by default)
                    if self.total_steps % 1 == 0:
                        # if self.pos * self.game.tile_size not in self.pheromones:
                            self.pheromones.append((self.pos * self.game.tile_size))

    def draw(self):
        if len(self.pheromones) > 1:
            pygame.draw.lines(self.game.screen, self.col, False, self.pheromones)


        pygame.draw.rect(self.game.screen, (200, 0, 0),
                         (self.pos.x * self.game.tile_size, self.pos.y * self.game.tile_size,
                          self.game.tile_size, self.game.tile_size))


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.clock = pygame.time.Clock()
        self.dt = 1

        # map settings
        self.grid_size = 128
        self.tile_size = SCREEN_HEIGHT / self.grid_size

        self.ants = [Ant(self, 64, 64) for _ in range(50)]

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

        for ant in self.ants:
            ant.update()

        self.dt = self.clock.tick(FPS)
        pygame.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.screen.fill((235, 235, 235))

        for ant in self.ants:
            ant.draw()

        pygame.display.update()
        pass

    def run(self):
        while True:
            self.events()
            if self.running:
                self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
