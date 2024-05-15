from random import randint, choice

import pygame


class Ant:
    def __init__(self, nest, game, pos):
        self.game = game
        self.nest = nest

        self.in_nest = True
        self.pos = pygame.Vector2(*pos)
        self.walking_direction = pygame.Vector2()

        self.pheromones = []

        self.trail_index = 0
        self.pheromones_to_food = []

        self.total_steps = 0
        self.col = (randint(0, 255), randint(0, 255), randint(0, 255))

        self.has_food = False


    def look_for_food(self):
        for ix in range(-1, 2):
            for iy in range(-1, 2):
                if (ix, iy) != (0, 0):
                    jx = (self.pos.x + ix)
                    jy = (self.pos.y + iy)
                    for food in self.game.foods:
                        if food.pos == (jx, jy):
                            return food
        return None


    def update(self):
        if self.in_nest is False:
            if self.pheromones_to_food:
                if self.has_food is False:
                    food = self.look_for_food()
                    if food:
                        if food.chunks > 0:
                            self.has_food = True
                            food.chunks -= 1

                    else:
                        if randint(1, 4) == 1:
                            if self.trail_index + 1 < len(self.pheromones_to_food):
                                self.trail_index += 1
                                self.pos = self.pheromones_to_food[self.trail_index] // self.game.tile_size
                            else:
                                self.pheromones.extend(self.pheromones_to_food)
                                self.pheromones_to_food.clear()

                else:
                    for ix in range(-1, 2):
                        for iy in range(-1, 2):
                            if (ix, iy) != (0, 0):
                                jx = (self.pos.x + ix)
                                jy = (self.pos.y + iy)
                                if (jx, jy) == self.nest.pos:
                                    self.in_nest = True
                                    self.has_food = False

                    else:
                        # reversed_pheromones = self.pheromones_to_food[::-1]
                        if randint(1, 4) == 1:
                            if self.trail_index - 1 >= 0:
                                self.trail_index -= 1
                                self.pos = self.pheromones_to_food[self.trail_index] // self.game.tile_size


            else:
                if self.look_for_food():
                    if self.has_food is False:
                        self.has_food = True
                        self.pheromones_to_food.extend(self.pheromones)
                        self.trail_index = len(self.pheromones_to_food)


                # chance to change x direction
                if randint(1, 32) == 1:
                    if self.walking_direction.x == 0:
                        self.walking_direction.x = choice((-1, 1))
                    else:
                        self.walking_direction.x = 0

                # chance to change y direction
                if randint(1, 32) == 1:
                    if self.walking_direction.y == 0:
                        self.walking_direction.y = choice((-1, 1))
                    else:
                        self.walking_direction.y = 0

                # chance to move the ant in its facing direction
                if randint(1, 8) == 1:
                    if 0 <= (self.pos.x + self.walking_direction.x) * self.game.tile_size < self.game.SCREEN_WIDTH:
                        if 0 <= (self.pos.y + self.walking_direction.y) * self.game.tile_size < self.game.SCREEN_WIDTH:
                            self.pos += self.walking_direction

                            self.total_steps += 1

                            if self.pos == self.nest.pos:
                                self.in_nest = True

                            # will leave a pheromone every N steps (1 by default)
                            if not self.pheromones_to_food:
                                if self.total_steps % 1 == 0:
                                    self.pheromones.append((self.pos * self.game.tile_size))

        else:
            if self.pheromones:
                self.pheromones.clear()
            if randint(1, 100) == 1:
                self.in_nest = False

    def draw(self):
        if len(self.pheromones) > 1:
            pygame.draw.lines(self.game.screen, self.col, False, self.pheromones)

        if self.pheromones_to_food:
            pygame.draw.lines(self.game.screen, self.col, False, self.pheromones_to_food)

        if self.in_nest is False:
            pygame.draw.rect(self.game.screen, (200, 0, 0),
                             (self.pos.x * self.game.tile_size, self.pos.y * self.game.tile_size,
                              self.game.tile_size, self.game.tile_size))


class AntNest:
    def __init__(self, game, x, y, num_of_ants=1):
        self.game = game
        self.pos = pygame.Vector2(x, y)
        self.ants = set(Ant(self, self.game, self.pos) for _ in range(num_of_ants))

        self.time_passed = 0

    def update(self):
        # if self.time_passed % 60 == 0:
        #     self.ants.add(Ant(self, self.game, self.pos))

        self.time_passed += 1

    def draw(self):
        pygame.draw.rect(self.game.screen, (139, 69, 19),
                         (self.pos.x * self.game.tile_size, self.pos.y * self.game.tile_size,
                          self.game.tile_size, self.game.tile_size))
