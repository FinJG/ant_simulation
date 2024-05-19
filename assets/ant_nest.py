from random import randint, choice

import pygame


class Ant:
    def __init__(self, nest, game, pos):
        self.game = game

        self.nests = [nest]
        self.current_nest = self.nests[0]

        self.in_nest = True
        self.pos = pygame.Vector2(*pos)
        self.walking_direction = pygame.Vector2()

        self.pheromones = []

        self.trail_index = 0
        self.pheromones_to_food = []

        self.total_steps = 0
        self.steps = 0
        self.col = (randint(0, 255), randint(0, 255), randint(0, 255))

        self.has_food = False

    def look_for_food(self):
        """
        looks at the ants adjacent tiles for food
        and returns the food if found, else it returns None
        :returns: Food if food is found, else None
        """
        for ix in range(-1, 2):
            for iy in range(-1, 2):
                if (ix, iy) != (0, 0):
                    jx = (self.pos.x + ix)
                    jy = (self.pos.y + iy)
                    for food in self.game.foods:
                        if food.pos == (jx, jy):
                            return food
        return None

    def move(self) -> None:
        """
        this function controls the "random" movement of the ant
        """
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
                if 0 <= (self.pos.y + self.walking_direction.y) * self.game.tile_size < self.game.SCREEN_HEIGHT:
                    self.pos += self.walking_direction

                    self.total_steps += 1
                    self.steps += 1

                    # check if the ant has landed on a path that leads to food
                    for nest in self.nests:
                        for ant in nest.ants:
                            if ant.pheromones_to_food:
                                # if it has, it will now follow the path
                                if self.pos * self.game.tile_size in ant.pheromones_to_food:
                                    if randint(1, 2) == 1:
                                        self.pheromones_to_food = ant.pheromones_to_food.copy()
                                        self.trail_index = ant.pheromones_to_food.index(
                                            self.pos * self.game.tile_size)
                                        self.pheromones.clear()
                                        return

                    # check to see if the ant has landed on a nest
                    for nest in self.nests:
                        # if it has, the ant will go inside
                        if self.pos == nest.pos:
                            self.in_nest = True
                            self.steps = 0
                            return

                    # will leave a pheromone every N steps (1 by default)
                    if not self.pheromones_to_food:
                        self.pheromones.append((self.pos * self.game.tile_size))
                        self.trail_index = len(self.pheromones)

    def move_on_path(self, direction, path) -> None:
        """
        this function is used to move the ant up and down
        its pheromone path to food

        :param direction: 1 to move up the path and -1 to move down
        :param path: the pheromone path you want the ant to follow
        """
        # chance to move
        if randint(1, 4) == 1:
            self.trail_index += direction
            self.pos = path[self.trail_index] // self.game.tile_size

    def update(self) -> None:
        # if the ant is outside a nest
        if self.in_nest is False:

            # if the ant is following a path to food
            if self.pheromones_to_food:

                # if the ant has no food
                if self.has_food is False:

                    # if ant isn't at the end of the food path
                    if self.trail_index + 1 < len(self.pheromones_to_food):
                        self.move_on_path(1, self.pheromones_to_food)

                    # if ant is at the end of food path
                    else:
                        food = self.look_for_food()

                        # if food is found
                        if food:
                            if food.chunks > 0:
                                # take a piece of food
                                self.has_food = True
                                food.chunks -= 1
                        else:

                            self.pheromones.extend(self.pheromones_to_food.copy())
                            self.pheromones_to_food.clear()

                # if the ant has food
                else:
                    if self.trail_index - 1 >= 0:
                        self.move_on_path(-1, self.pheromones_to_food)

                    else:
                        self.steps = 0
                        self.in_nest = True
                        self.has_food = False
                        self.current_nest.stored_food += 1
                        return

            # if the ant is not following a path to food
            else:
                if self.steps > 40:
                    if self.trail_index == 0:
                        self.in_nest = True
                        self.steps = 0
                        self.pheromones.clear()
                        self.pos = self.current_nest.pos.copy()
                        return

                    self.move_on_path(-1, self.pheromones)
                    return

                if self.look_for_food():
                    # grab food and start following path to food
                    self.has_food = True
                    self.pheromones_to_food.extend(self.pheromones.copy())
                    self.trail_index = len(self.pheromones_to_food)
                    return

                self.move()

        # if the ant is inside the nest
        else:
            # clear pheromones
            if self.pheromones:
                self.pheromones.clear()

            # chance to leave the nest
            if randint(1, 100) == 1:
                self.in_nest = False

    def draw(self):
        if len(self.pheromones) > 1:
            pygame.draw.lines(self.game.screen, self.current_nest.col, False, self.pheromones)

        if len(self.pheromones_to_food) > 1:
            pygame.draw.lines(self.game.screen, self.current_nest.col, False, self.pheromones_to_food)

        if self.in_nest is False:
            pygame.draw.rect(self.game.screen, self.current_nest.col,  # (200, 0, 0)
                             (self.pos.x * self.game.tile_size, self.pos.y * self.game.tile_size,
                              self.game.tile_size, self.game.tile_size))


class AntNest:
    def __init__(self, game, x, y, num_of_ants=10):
        self.game = game
        self.pos = pygame.Vector2(x, y)
        self.ants = set(Ant(self, self.game, self.pos) for _ in range(num_of_ants))
        self.stored_food = 0

        self.col = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.time_passed = 0

        self.ant_cost = 5

    def update(self):
        self.time_passed += 1

        if self.stored_food >= self.ant_cost:
            if randint(1, 60 * 10):
                self.stored_food -= self.ant_cost
                self.ants.add(Ant(self, self.game, self.pos))

    def draw(self):
        pygame.draw.rect(self.game.screen, (139, 69, 19),
                         (self.pos.x * self.game.tile_size, self.pos.y * self.game.tile_size,
                          self.game.tile_size, self.game.tile_size))
