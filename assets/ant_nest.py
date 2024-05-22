from random import randint, choice
from math import dist

import pygame


class AntNest:
    def __init__(self, game, x, y, num_of_ants=10, col=(randint(0, 255), randint(0, 255), randint(0, 255))):
        self.game = game
        self.pos = pygame.Vector2(x, y)
        self.ants = set(self.game.Ant(self, self.game, self.pos) for _ in range(num_of_ants))
        self.stored_food = 0

        self.col = col
        self.time_passed = 0

        self.ant_cost = 5
        self.unclaimed = False

        self.unclaim_timer_max = 60 * 30
        self.unclaim_timer = self.unclaim_timer_max

    def update(self):
        self.time_passed += 1

        if all([not ant.in_nest for ant in self.ants]):
            self.unclaim_timer -= 1

        else:
            self.unclaim_timer = self.unclaim_timer_max

        if self.unclaim_timer == 0:
            self.unclaimed = True
            self.game.unclaimed_nests.append(self)

            for ant in self.ants:
                if self in ant.nests:
                    ant.nests.remove(self)
                    break

        if self.stored_food >= self.ant_cost:
            if randint(1, 60 * 10) == 1:
                self.stored_food -= self.ant_cost

                if len(self.ants) <= 10:
                    self.ants.add(self.game.Ant(self, self.game, self.pos))

    def draw(self):
        pygame.draw.rect(self.game.screen, (139, 69, 19),
                         (self.pos.x * self.game.tile_size, self.pos.y * self.game.tile_size,
                          self.game.tile_size, self.game.tile_size))
