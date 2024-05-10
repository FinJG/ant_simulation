from random import randint

import pygame


class Ant:
    def __init__(self, nest, game, pos):
        self.game = game
        self.nest = nest

        self.in_nest = True
        self.pos = pygame.Vector2(*pos)
        self.walking_direction = pygame.Vector2()
        self.pheromones = []
        self.total_steps = 0
        self.col = (randint(0, 255), randint(0, 255), randint(0, 255))

    def update(self):
        if self.in_nest is False:

            # chance to change x direction
            if randint(1, 32) == 1:
                self.walking_direction.x = randint(-1, 1)

            # chance to change y direction
            if randint(1, 32) == 1:
                self.walking_direction.y = randint(-1, 1)

            # chance to move the ant in its facing direction
            if randint(1, 8) == 1:
                if 0 <= (self.pos.x + self.walking_direction.x) * self.game.tile_size < self.game.SCREEN_WIDTH:
                    if 0 <= (self.pos.y + self.walking_direction.y) * self.game.tile_size < self.game.SCREEN_WIDTH:
                        self.pos += self.walking_direction

                        self.total_steps += 1

                        if self.pos == self.nest.pos:
                            self.in_nest = True

                        # will leave a pheromone every N steps (1 by default)
                        if self.total_steps % 1 == 0:
                            self.pheromones.append((self.pos * self.game.tile_size))

        else:
            if randint(1, 100) == 1:
                self.in_nest = False

    def draw(self):
        if len(self.pheromones) > 1:
            pygame.draw.lines(self.game.screen, self.col, False, self.pheromones)

        if self.in_nest is False:
            pygame.draw.rect(self.game.screen, (200, 0, 0),
                             (self.pos.x * self.game.tile_size, self.pos.y * self.game.tile_size,
                              self.game.tile_size, self.game.tile_size))


class AntNest:
    def __init__(self, game, x, y):
        self.game = game
        self.pos = pygame.Vector2(x, y)
        self.ants = set(Ant(self, self.game, self.pos) for _ in range(10))

        self.time_passed = 0

    def update(self):
        # if self.time_passed % 60 == 0:
        #     self.ants.add(Ant(self, self.game, self.pos))

        self.time_passed += 1

    def draw(self):
        pygame.draw.rect(self.game.screen, (139, 69, 19),
                         (self.pos.x * self.game.tile_size, self.pos.y * self.game.tile_size,
                          self.game.tile_size, self.game.tile_size))
