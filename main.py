import sys
from random import randint

import pygame

import assets


class Game(assets.Settings):
    def __init__(self):
        super().__init__()
        pygame.init()

    def new_game(self):
        self.nests.clear()
        self.foods.clear()

        for i in range(2):
            self.nests.append(assets.AntNest(self,
                                             randint(0, self.grid_size),
                                             randint(0, self.grid_size),
                                             1,
                                             (randint(0, 255), randint(0, 255), randint(0, 255))
                                             ))

        for i in range(200):
            self.foods.append(assets.Food(self,
                                          randint(0, self.grid_size),
                                          randint(0, self.grid_size),
                                          ))

    def events(self):
        self.keys = pygame.key.get_pressed()
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

                if event.key == pygame.K_r:
                    self.new_game()

        if self.keys[pygame.K_w]:
            self.FPS += 0.1 * self.dt

        if self.keys[pygame.K_s]:
            self.FPS -= 0.1 * self.dt

    def update(self):
        for nest in self.nests:
            for ant in nest.ants:
                ant.update()
            nest.update()

        for food in self.foods:
            food.update()

        self.dt = self.clock.tick(self.FPS)
        pygame.display.set_caption(f'{self.clock.get_fps():.1f}')

    def draw(self):
        self.screen.fill((235, 235, 235))

        for nest in self.nests:
            for ant in nest.ants:
                ant.draw()
            nest.draw()

        for food in self.foods:
            food.draw()

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
