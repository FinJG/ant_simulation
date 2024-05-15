import pygame
from random import randint


class Food:
    def __init__(self, game, x, y):
        self.game = game

        self.pos = pygame.Vector2(x, y)
        self.chunks = 10
        self.col = (randint(50, 100), randint(200, 255), randint(50, 100))

    def update(self):
        if self.chunks == 0:
            self.game.foods.remove(self)

    def draw(self):
        pygame.draw.rect(self.game.screen, (200, 0, 0),
                         (self.pos.x * self.game.tile_size, self.pos.y * self.game.tile_size,
                          self.game.tile_size, self.game.tile_size))

